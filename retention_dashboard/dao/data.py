from retention_dashboard.models import DataPoint, Week


def get_weeks_with_data():
    unique_weeks = DataPoint.objects.values('week').distinct()
    week_objects = []
    for week in unique_weeks:
        print(week)
        week_obj = Week.objects.get(id=week['week'])
        week_objects.append(week_obj)
    return week_objects
