from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from uw_saml.utils import get_user
from uw_saml.decorators import group_required
from django.conf import settings
from retention_dashboard.models import Week, Upload
from django.utils.decorators import method_decorator


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
        context['weeks'] = Week.objects.all().order_by('year',
                                                       'quarter',
                                                       'number')
        context['uploads'] = Upload.objects.all().order_by('week', 'type')
        return context