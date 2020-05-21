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
        data_points.append(dp)
    DataPoint.objects.bulk_create(data_points)
