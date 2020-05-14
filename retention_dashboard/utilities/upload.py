from retention_dashboard.models import DataPoint
import csv
from io import StringIO


def process_upload(upload):
    data_points = []
    reader = csv.DictReader(StringIO(upload.file),
                            delimiter=',')

    for idx, row in enumerate(reader):
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
        data_points.append(dp)
    DataPoint.objects.bulk_create(data_points)
