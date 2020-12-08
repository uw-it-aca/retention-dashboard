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
                advisor_name = advisor_name.strip()
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
        if upload.type:
            dp.type = upload.type
        if upload.week:
            dp.week = upload.week
        if upload:
            dp.upload = upload
        if row.get("student_name_lowc"):
            dp.student_name = row.get("student_name_lowc")
        if row.get("student_no"):
            dp.student_number = row.get("student_no")
        if row.get("uw_netid"):
            dp.netid = row.get("uw_netid")
        if row.get("premajor"):
            dp.premajor = row.get("premajor")
        if row.get("stem"):
            dp.is_stem = row.get("stem")
        if row.get("incoming_freshman"):
            dp.is_freshman = row.get("incoming_freshman")
        if row.get("activity"):
            dp.activity_score = row.get("activity")
        if row.get("assignments"):
            dp.assignment_score = row.get("assignments")
        if row.get("grades"):
            dp.grade_score = row.get("grades")
        if row.get("pred"):
            dp.priority_score = row.get("pred")
        if row.get("sign_in"):
            dp.signin_score = row.get("sign_in")
        if advisor:
            dp.advisor = advisor
        if has_a:
            dp.has_a_term = has_a
        if has_b:
            dp.has_b_term = has_b
        if has_full:
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
