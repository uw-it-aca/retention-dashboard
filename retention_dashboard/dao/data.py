from retention_dashboard.models import DataPoint, Week


def get_weeks_with_data():
    unique_weeks = DataPoint.objects.values('week').distinct()
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
                      advisor_filter=None
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
    if premajor_filter:
        dataset = DataPoint.filter_by_premajor(dataset, premajor_filter)

    if text_filter:
        dataset = DataPoint.filter_by_text(dataset, text_filter)
    if advisor_filter:
        dataset = DataPoint.filter_by_advisor(dataset, advisor_filter)

    return dataset
