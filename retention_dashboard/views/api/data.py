import os
from django.conf import settings
from django.utils.decorators import method_decorator
from uw_saml.decorators import group_required
from retention_dashboard.views.api import RESTDispatch
from retention_dashboard.dao.data import get_weeks_with_data


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


class WeekView(RESTDispatch):
    def get(self, request):
        weeks = get_weeks_with_data()
        json_data = []
        for week in weeks:
            json_data.append(week.json_data())
        return self.json_response(content=json_data)
