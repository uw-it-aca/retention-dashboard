from retention_dashboard.models import DataPoint, Week


def get_weeks_with_data():
    unique_weeks = DataPoint.objects.values('week').distinct().order_by(
                    'week__year', 'week__quarter', 'week__number'
                   )
    week_objects = []
    for week in unique_weeks:
        week_obj = Week.objects.get(id=week['week'])
        week_objects.append(week_obj)
    return week_objects


def get_filtered_data(type, week,
                      grade_filters=None,
                      activity_filters=None,
                      assignment_filters=None,
                      priority_filters=None,
                      premajor_filter=None,
                      text_filter=None,
                      advisor_filter=None,
                      summer_filters=None,
                      stem_filter=None,
                      freshman_filter=None,
                      signins_filters=None
                      ):
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
    if freshman_filter:
        dataset = DataPoint.filter_by_freshman(dataset, freshman_filter)

    if text_filter:
        dataset = DataPoint.filter_by_text(dataset, text_filter)
    if advisor_filter:
        if advisor_filter == "no_assigned_adviser":
            advisor_filter = ""  # query using empty string
        dataset = DataPoint.filter_by_advisor(dataset, advisor_filter)
    if summer_filters:
        dataset = DataPoint.filter_by_summer(dataset, summer_filters)

    return dataset
