# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import json
from django.conf import settings
from django.utils.decorators import method_decorator
from uw_saml.decorators import group_required
from retention_dashboard.views.api import RESTDispatch
from retention_dashboard.dao.data import FilterDataDao
from retention_dashboard.dao.auth import get_type_authorizations
from retention_dashboard.models import Advisor, Week, Sport, DataPoint
from logging import getLogger

logger = getLogger(__name__)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class DataView(RESTDispatch):
    def get(self, request, week, file, *args, **kwargs):
        logger.info('load dataset, type: %s, week: %s' % (file, week))
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
        dao = FilterDataDao()
        weeks = dao.get_weeks_with_data()
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
        current_page = request.GET.get("current_page", None)
        per_page = request.GET.get("per_page", None)
        sort_by = request.GET.get("sort_by", None)
        sort_desc = request.GET.get("sort_desc", None)
        week = request.GET.get("week", None)
        type = request.GET.get("type", None)
        text_filter = request.GET.get("text_filter", None)
        grade_filters = request.GET.getlist("grade_filters", None)
        assignment_filters = request.GET.getlist("assignment_filters", None)
        priority_filters = request.GET.getlist("priority_filters", None)
        activity_filters = request.GET.getlist("activity_filters", None)
        signins_filters = request.GET.getlist("signins_filters", None)
        advisor_filter = request.GET.get("advisor_filter", None)
        summer_filters = request.GET.getlist("summer_filters", None)
        premajor_filter = request.GET.get("premajor_filter", None)
        stem_filter = request.GET.get("stem_filter", None)
        sport_filter = request.GET.get("sport_filter", None)
        class_standing_filter = request.GET.get("class_standing_filter", None)
        if premajor_filter == "true":
            premajor_filter = True
        if stem_filter == "true":
            stem_filter = True
        if sort_desc == "true":
            sort_desc = True

        logger.info('load filtered dataset, type: %s, week: %s' % (type, week))

        if week is None or type is None:
            return self.error_response(status=400)

        week_obj = Week.objects.get(id=week)
        is_summer = week_obj.quarter == 3

        auth_list = get_type_authorizations(request)
        if type not in auth_list:
            err_msg = "Not authorized for type " + type
            return self.error_response(403, content={"msg": err_msg})

        dao = FilterDataDao()
        data_points = dao.get_filtered_data(
                                type, week,
                                text_filter=text_filter,
                                grade_filters=grade_filters,
                                assignment_filters=assignment_filters,
                                priority_filters=priority_filters,
                                activity_filters=activity_filters,
                                signins_filters=signins_filters,
                                premajor_filter=premajor_filter,
                                advisor_filter=advisor_filter,
                                summer_filters=summer_filters,
                                stem_filter=stem_filter,
                                sport_filter=sport_filter,
                                class_standing_filter=class_standing_filter)

        row_count = len(data_points)

        # sort in code since the django doesn't support sorting by properties
        if sort_by and sort_desc:
            sort_column = f"-{sort_by}" if sort_desc is True else sort_by
            data_points = data_points.order_by(sort_column)

        # paginate
        if per_page and current_page:
            per_page = int(per_page)
            current_page = int(current_page)
            page_start = per_page * (current_page - 1)
            page_end = page_start + per_page
            data_points = data_points[page_start:page_end]

        response_data = []
        for point in data_points:
            response_data.append(point.json_data())

        try:
            return self.json_response(content={"count": row_count,
                                               "is_summer": is_summer,
                                               "rows": response_data})
        except TypeError:
            return self.error_response(status=404)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class AdvisorListView(RESTDispatch):
    def get(self, request):
        advisors = Advisor.get_all_advisors()
        return self.json_response(content=advisors)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class SportListView(RESTDispatch):
    def get(self, request):
        week_dict = json.loads(request.GET.get("week"))
        week_number = week_dict["number"]
        quarter = week_dict["quarter"]
        year = week_dict["year"]
        sports = Sport.get_all_sports(week_number, quarter, year)
        return self.json_response(content=sports)


@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class ClassStandingListView(RESTDispatch):
    def get(self, request):
        week_dict = json.loads(request.GET.get("week"))
        week_number = week_dict["number"]
        quarter = week_dict["quarter"]
        year = week_dict["year"]
        class_standings = DataPoint.get_all_class_standings(
            week_number, quarter, year)
        return self.json_response(content=class_standings)
