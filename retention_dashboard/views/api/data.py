import os
from django.conf import settings
from django.utils.decorators import method_decorator
from uw_saml.decorators import group_required
from retention_dashboard.views.api import RESTDispatch
from retention_dashboard.dao.data import get_weeks_with_data, get_filtered_data
from retention_dashboard.dao.auth import get_type_authorizations
from retention_dashboard.models import DataPoint


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


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class WeekView(RESTDispatch):
    def get(self, request):
        weeks = get_weeks_with_data()
        json_data = []
        for week in weeks:
            json_data.append(week.json_data())
        return self.json_response(content=json_data)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class DataAuthView(RESTDispatch):
    def get(self, request):
        return self.json_response(content=get_type_authorizations(request))


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class FilteredDataView(RESTDispatch):
    def get(self, request):
        week = request.GET.get("week", None)
        type = request.GET.get("type", None)
        text_filter = request.GET.get("text_filter", None)
        grade_filters = request.GET.getlist("grade_filters", None)
        assignment_filters = request.GET.getlist("assignment_filters", None)
        priority_filters = request.GET.getlist("priority_filters", None)
        activity_filters = request.GET.getlist("activity_filters", None)
        premajor_filter = request.GET.get("premajor_filter", None)

        if week is None or type is None:
            return self.error_response(status=4//00)
        auth_list = get_type_authorizations(request)
        if type not in auth_list:
            err_msg = "Not authorized for type " + type
            return self.error_response(403, content={"msg": err_msg})
        data_points = get_filtered_data(type, week,
                                        text_filter=text_filter,
                                        grade_filters=grade_filters,
                                        assignment_filters=assignment_filters,
                                        priority_filters=priority_filters,
                                        activity_filters=activity_filters,
                                        premajor_filter=premajor_filter)

        response_data = []
        for point in data_points:
            response_data.append(point.json_data())
        return self.json_response(content={"count": len(data_points),
                                           "rows": response_data})