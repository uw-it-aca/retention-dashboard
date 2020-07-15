from retention_dashboard.models import DataPoint, Advisor
import csv
from io import StringIO


def process_upload(upload):
    data_points = []
    reader = csv.DictReader(StringIO(upload.file),
                            delimiter=',')

    advisor_dict = {}

    for idx, row in enumerate(reader):
        advisor_netid = row.get("staff_id")
        advisor_name = row.get("adviser_name")
        advisor = None
        if advisor_netid is not None and advisor_name is not None:
            if advisor_netid not in advisor_dict:
                advisor, created = Advisor.objects.\
                    get_or_create(advisor_netid=advisor_netid,
                                  advisor_type=upload.type,
                                  defaults={'advisor_name': advisor_name})
                advisor_dict[advisor_netid] = advisor
            else:
                advisor = advisor_dict[advisor_netid]
        has_a, has_b, has_full = \
            _get_summer_terms_from_string(row.get('summer'))

        dp = DataPoint()
        dp.type = upload.type
        dp.week = upload.week
        dp.upload = upload
        dp.student_name = row.get("student_name_lowc")
        dp.student_number = row.get("student_no")
        dp.netid = row.get("uw_netid")
        dp.premajor = row.get("premajor")
        dp.activity_score = row.get("activity")
        dp.assignment_score = row.get("assignments")
        dp.grade_score = row.get("grades")
        dp.priority_score = row.get("pred")
        dp.advisor = advisor
        dp.has_a_term = has_a
        dp.has_b_term = has_b
        dp.has_full_term = has_full
        data_points.append(dp)
    DataPoint.objects.bulk_create(data_points)


def _get_summer_terms_from_string(term_string):
    has_a = False
    has_b = False
    has_full = False
    if term_string is not None:
        if "A" in term_string:
            has_a = True
        if "B" in term_string:
            has_b = True
        if "Full" in term_string:
            has_full = True
    return has_a, has_b, has_full
