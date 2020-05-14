from retention_dashboard.models import Week, DataPoint, Upload


def create_initial_data():
    w1 = Week.objects.create(quarter=1, number=1, year=2020)
    w2 = Week.objects.create(quarter=1, number=2, year=2020)
    w3 = Week.objects.create(quarter=2, number=1, year=2020)
    upload = Upload.objects.create(file="foo.txt",
                                   type=1,
                                   uploaded_by="javerage",
                                   week=w1)

    DataPoint.objects.create(type=1,
                             week=w1,
                             student_name="J1",
                             student_number=3456,
                             netid="asddw",
                             premajor=True,
                             priority_score=-4,
                             activity_score=-4,
                             assignment_score=-4,
                             grade_score=-4,
                             upload=upload
                             )
    DataPoint.objects.create(type=1,
                             week=w1,
                             student_name="J2",
                             student_number=74635,
                             netid="fghjtydf",
                             premajor=False,
                             priority_score=-1,
                             activity_score=-1,
                             assignment_score=-1,
                             grade_score=-1,
                             upload=upload
                             )

    DataPoint.objects.create(type=1,
                             week=w1,
                             student_name="L1",
                             student_number=485465,
                             netid="dfgrsfg",
                             premajor=True,
                             priority_score=4,
                             activity_score=4,
                             assignment_score=4,
                             grade_score=4,
                             upload=upload
                             )
    DataPoint.objects.create(type=1,
                             week=w1,
                             student_name="J3",
                             student_number=75464,
                             netid="sdfgdsfg",
                             premajor=True,
                             priority_score=-3,
                             activity_score=-3,
                             assignment_score=-3,
                             grade_score=-3,
                             upload=upload
                             )
    DataPoint.objects.create(type=1,
                             week=w1,
                             student_name="K1",
                             student_number=854684,
                             netid="sdfgdsfg",
                             premajor=False,
                             priority_score=0,
                             activity_score=0,
                             assignment_score=0,
                             grade_score=0,
                             upload=upload
                             )
    DataPoint.objects.create(type=1,
                             week=w2,
                             student_name="K2",
                             student_number=146575,
                             netid="sdfgasdft4",
                             premajor=True,
                             priority_score=1,
                             activity_score=1,
                             assignment_score=1,
                             grade_score=1,
                             upload=upload
                             )
    DataPoint.objects.create(type=2,
                             week=w1,
                             student_name="K3",
                             student_number=5877,
                             netid="GDFhjedsry",
                             premajor=False,
                             priority_score=3,
                             activity_score=3,
                             assignment_score=3,
                             grade_score=3,
                             upload=upload
                             )
