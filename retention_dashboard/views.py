from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from uw_saml.utils import get_user
import json
import os
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
from uw_saml.decorators import group_required
from retention_dashboard.models import Week, DataPoint, Upload


class PageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['netid'] = get_user(self.request)
        return context


@method_decorator(login_required(),
                  name='dispatch')
@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class LandingView(PageView):
    template_name = "landing.html"

class AdminView(PageView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = {}
        context['weeks'] = Week.objects.all().order_by('year', 'quarter', 'number')
        return context

class RESTDispatch(View):
    @staticmethod
    def json_response(content={}, status=200):
        try:
            data = json.dumps(content,
                              sort_keys=True,
                              cls=DjangoJSONEncoder)
            return HttpResponse(data,
                                status=status,
                                content_type='application/json')
        except TypeError:
            return RESTDispatch().error_response(400)

    @staticmethod
    def error_response(status, message='', content={}):
        content['error'] = str(message)
        return HttpResponse(json.dumps(content),
                            status=status,
                            content_type='application/json',
                            )


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class DataView(RESTDispatch):
    def get(self, request, week, file, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "retention_dashboard/data",
                                 week,
                                 file)
        with open(file_path, 'r') as content_file:
            content = content_file.read()
        return self.json_response(content={"data": content})


class WeekAdmin(RESTDispatch):
    def post(self, request):
        year = request.POST.get("year")
        quarter = request.POST.get("quarter")
        week = request.POST.get("week")
        week, created = Week.objects.get_or_create(year=year,
                                                   quarter=quarter,
                                                   number=week)
        return self.json_response({"created": created})

class DataAdmin(RESTDispatch):
    def post(self, request):
        week_id = request.POST.get('week')
        type = request.POST.get('type')

        uploaded_file = request.FILES.get('file')
        document = None
        file = uploaded_file.read()
        try:
            document = file.decode('utf-16')
        except UnicodeDecodeError as ex:
            document = file.decode('utf-8')

        if document is None:
            return self.error_response(status=400,
                                       message="Invalid document")

        week = Week.objects.get(id=week_id)
        #TODO: Wire up user netid
        upload = Upload.objects.create(file=document,
                                       type=type,
                                       week=week,
                                       uploaded_by="javerage")
        return self.json_response({"created": True})
