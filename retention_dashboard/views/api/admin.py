# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import zipfile
from django.conf import settings
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from uw_saml.decorators import group_required
from retention_dashboard.models import Week, Upload
from retention_dashboard.management.commands.bulk_upload import \
    InvalidFileException, InvalidUploadException
from retention_dashboard.utilities.upload import process_upload
from userservice.user import get_original_user
from retention_dashboard.views.api import RESTDispatch
from retention_dashboard.views.api.forms import BulkDataForm


@method_decorator(group_required(settings.ADMIN_USERS_GROUP),
                  name='dispatch')
class WeekAdmin(RESTDispatch):
    def post(self, request):
        try:
            year = request.POST.get("year")
            quarter = request.POST.get("quarter")
            week = request.POST.get("week")
            week, created = Week.objects.get_or_create(year=year,
                                                       quarter=quarter,
                                                       number=week)
        except ValueError as ex:
            return self.error_response(status=400, message=ex)
        except Exception as ex:
            return self.error_response(status=500, message=ex)
        return self.json_response({"created": created})


@method_decorator(group_required(settings.ADMIN_USERS_GROUP),
                  name='dispatch')
class DataAdmin(RESTDispatch):
    def post(self, request):
        try:
            week_id = request.POST.get('week')
            type = request.POST.get('type')

            uploaded_file = request.FILES.get('file')
            file = uploaded_file.read()
            document = None
            try:
                document = file.decode('utf-8')
            except UnicodeDecodeError:
                document = file.decode('utf-16')
        except Exception as ex:
            return self.error_response(status=500, message=ex)

        if document is None:
            return self.error_response(status=400,
                                       message="Invalid document")

        week = Week.objects.get(id=week_id)
        user = get_original_user(request)
        try:
            upload = Upload.objects.create(file=document,
                                           type=type,
                                           week=week,
                                           uploaded_by=user)
            process_upload(upload)
        except IntegrityError as ex:
            return self.error_response(400, message=ex)
        except Exception as ex:
            return self.error_response(status=500, message=ex)
        return self.json_response({"created": True})

    def delete(self, request, upload_id):
        try:
            upload = Upload.objects.get(id=upload_id)
            upload.delete()
            return self.json_response({"deleted": True})
        except Exception:
            return self.error_response(400)


@method_decorator(group_required(settings.ADMIN_USERS_GROUP),
                  name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class BulkDataAdmin(RESTDispatch):

    def setup(self, request, *args, **kwargs):
        request.upload_handlers = [TemporaryFileUploadHandler(request)]
        super(BulkDataAdmin, self).setup(request, *args, **kwargs)

    def post(self, request):
        form = BulkDataForm(request.POST, request.FILES)
        if form.is_valid():
            delete_existing_data = request.POST.get("delete_existing_data")
            uploaded_file = request.FILES.get("upload")
            uploaded_file_path = uploaded_file.file.name
            if zipfile.is_zipfile(uploaded_file) is False:
                return self.error_response(
                    status=400, message="Document isn't a zip file.")
            else:
                try:
                    with zipfile.ZipFile(uploaded_file_path, 'r') as zip_file:
                        tmp_path = os.path.dirname(uploaded_file_path)
                        zip_file.extractall(tmp_path)
                        extracted = zip_file.namelist()
                        extracted_data_dir, _ = \
                            os.path.split(os.path.join(tmp_path, extracted[0]))
                        command_args = \
                            ["--path={}".format(extracted_data_dir),
                             "--user={}".format(request.user.username)]
                        if delete_existing_data == "true":
                            command_args.append("--delete_existing_data")

                        call_command("bulk_upload",
                                     *command_args)

                except InvalidFileException as ex:
                    return self.error_response(status=400, message=ex)
                except InvalidUploadException as ex:
                    return self.error_response(status=400, message=ex)
                except Exception as ex:
                    return self.error_response(status=500, message=ex)
                return self.json_response({"created": True})
        else:
            return self.error_response(
                status=400,
                message=(form.errors))


@method_decorator(group_required(settings.ADMIN_USERS_GROUP),
                  name='dispatch')
class MockDataAdmin(RESTDispatch):
    def put(self, request):
        if settings.DEBUG:
            call_command('loaddata', 'mock_data.json')
            return self.json_response({"loaded": True})
        return self.error_response(status=400)
