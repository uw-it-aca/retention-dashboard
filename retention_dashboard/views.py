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
        file_path = os.path.join(settings.BASE_DIR, "retention_dashboard/data", week, file)
        with open(file_path, 'r') as content_file:
            content = content_file.read()
        return self.json_response(content={"data": content})