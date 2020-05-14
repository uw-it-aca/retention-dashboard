from django.conf import settings
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.core.management import call_command
from uw_saml.decorators import group_required
from retention_dashboard.models import Week, Upload
from retention_dashboard.utilities.upload import process_upload
from userservice.user import get_original_user
from retention_dashboard.views.api import RESTDispatch


@method_decorator(group_required(settings.ADMIN_USERS_GROUP),
                  name='dispatch')
class WeekAdmin(RESTDispatch):
    def post(self, request):
        year = request.POST.get("year")
        quarter = request.POST.get("quarter")
        week = request.POST.get("week")
        week, created = Week.objects.get_or_create(year=year,
                                                   quarter=quarter,
                                                   number=week)
        return self.json_response({"created": created})


@method_decorator(group_required(settings.ADMIN_USERS_GROUP),
                  name='dispatch')
class DataAdmin(RESTDispatch):
    def post(self, request):
        week_id = request.POST.get('week')
        type = request.POST.get('type')

        uploaded_file = request.FILES.get('file')
        document = None
        file = uploaded_file.read()
        try:
            document = file.decode('utf-8')
        except UnicodeDecodeError as ex:
            document = file.decode('utf-16')

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
        except IntegrityError:
            return self.error_response(400)
        return self.json_response({"created": True})

    def delete(self, request, upload_id):
        try:
            upload = Upload.objects.get(id=upload_id)
            upload.delete()
            return self.json_response({"deleted": True})
        except Exception:
            return self.error_response(400)


class MockDataAdmin(RESTDispatch):
    def put(self, request):
        if settings.DEBUG:
            call_command('loaddata', 'mock_data.json')
            return self.json_response({"loaded": True})
        return self.error_response(status=400)
