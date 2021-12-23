# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from retention_dashboard.models import DataPoint, Week


class FilterDataDao():

    def get_weeks_with_data(self):
        unique_weeks = DataPoint.objects.values('week').distinct().order_by(
                        'week__year', 'week__quarter', 'week__number'
                    )
        week_objects = []
        for week in unique_weeks:
            week_obj = Week.objects.get(id=week['week'])
            week_objects.append(week_obj)
        return week_objects

    def get_filtered_data(self, type, week, grade_filters=None,
                          activity_filters=None, assignment_filters=None,
                          priority_filters=None, premajor_filter=None,
                          text_filter=None, advisor_filter=None,
                          summer_filters=None, stem_filter=None,
                          signins_filters=None, sport_filter=None,
                          class_standing_filter=None):
        dataset = DataPoint.get_data_by_type_week(type, week)
        if grade_filters:
            dataset = DataPoint.filter_by_ranges(dataset,
                                                 grade_filters,
                                                 "grade_score")
        if activity_filters:
            dataset = DataPoint.filter_by_ranges(dataset,
                                                 activity_filters,
                                                 "activity_score")
        if assignment_filters:
            dataset = DataPoint.filter_by_ranges(dataset,
                                                 assignment_filters,
                                                 "assignment_score")
        if priority_filters:
            dataset = DataPoint.filter_by_ranges(dataset,
                                                 priority_filters,
                                                 "priority_score")
        if signins_filters:
            dataset = DataPoint.filter_by_ranges(dataset,
                                                 signins_filters,
                                                 "signin_score")
        if premajor_filter:
            dataset = DataPoint.filter_by_premajor(dataset, premajor_filter)
        if stem_filter:
            dataset = DataPoint.filter_by_stem(dataset, stem_filter)

        if text_filter:
            dataset = DataPoint.filter_by_text(dataset, text_filter)

        if (advisor_filter is not None and type is not None and
                advisor_filter != "all"):
            if advisor_filter == "no_assigned_adviser":
                advisor_filter = ""  # query using empty string
            dataset = DataPoint.filter_by_advisor(dataset,
                                                  advisor_filter,
                                                  type)

        if class_standing_filter and class_standing_filter != "all":
            dataset = DataPoint.filter_by_class_standing(
                dataset, class_standing_filter)

        if sport_filter and sport_filter != "all":
            dataset = DataPoint.filter_by_sports(dataset, sport_filter)

        if summer_filters:
            dataset = DataPoint.filter_by_summer(dataset, summer_filters)

        return dataset
