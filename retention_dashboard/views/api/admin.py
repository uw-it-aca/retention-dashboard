# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import traceback
import zipfile
from django.conf import settings
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from uw_saml.decorators import group_required
from retention_dashboard.models import Week, Upload
from retention_dashboard.utilities.upload import process_upload, \
    process_rad_upload
from userservice.user import get_original_user
from retention_dashboard.views.api import RESTDispatch
from retention_dashboard.views.api.forms import GCSForm
from retention_dashboard.dao.admin import GCSDataDao


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
            # get post data
            week_id = request.POST.get('week')
            type = request.POST.get('type')
            uploaded_file = request.FILES.get('file')

            # read uploaded file
            if uploaded_file is None:
                return self.error_response(status=400,
                                           message="No file specified")
            file = uploaded_file.read()

            # decode file document
            document = None
            try:
                document = file.decode('utf-8')
            except UnicodeDecodeError:
                document = file.decode('utf-16')
            if document is None:
                return self.error_response(status=400,
                                           message="Invalid document")

            # process upload
            week = Week.objects.get(id=week_id)
            user = get_original_user(request)
            process_upload(document, type, week, user)
        except Exception as ex:
            return self.error_response(status=500, message=ex)
        except IntegrityError as ex:
            return self.error_response(400, message=ex)

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
class GCSDataAdmin(RESTDispatch):

     def post(self, request):
        form = GCSForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                rad_file_name = request.POST.get("file")
                dao = GCSDataDao()
                rad_document = dao.download_from_gcs_bucket(rad_file_name)
                user = get_original_user(request)
                process_rad_upload(rad_file_name, rad_document, user)
            except ValueError as err:
                return self.error_response(
                    status=400,
                    message=err)
            except Exception:
                tb = traceback.format_exc()
                return self.error_response(
                    status=500,
                    message=tb)
        else:
            return self.error_response(
                status=400,
                message=form.errors)
        return self.json_response({"created": True})


@method_decorator(group_required(settings.ADMIN_USERS_GROUP),
                  name='dispatch')
class MockDataAdmin(RESTDispatch):
    def put(self, request):
        if settings.DEBUG:
            call_command('loaddata', 'mock_data.json')
            return self.json_response({"loaded": True})
        return self.error_response(status=400)
