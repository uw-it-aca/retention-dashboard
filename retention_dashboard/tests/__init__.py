# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from retention_dashboard.models import Week, DataPoint, Upload, Advisor, \
    Sport


def create_initial_data():
    w1 = Week.objects.create(quarter=1, number=1, year=2020)
    w2 = Week.objects.create(quarter=1, number=2, year=2020)
    w3 = Week.objects.create(quarter=2, number=1, year=2020)
    a1 = Advisor.objects.create(advisor_name="John Doe",
                                advisor_netid="jdoe123",
                                advisor_type=1)
    a2 = Advisor.objects.create(advisor_name="Jane Doe",
                                advisor_netid="janed456",
                                advisor_type=2)
    a3 = Advisor.objects.create(advisor_name="Sam Smith",
                                advisor_netid="samsmith",
                                advisor_type=2)
    a4 = Advisor.objects.create(advisor_name="Sam Smith",
                                advisor_netid="samsmith",
                                advisor_type=3)
    a5 = Advisor.objects.create(advisor_name="Sarah Smith",
                                advisor_netid="sarah42",
                                advisor_type=1)
    a6 = Advisor.objects.create(advisor_name="James Brown",
                                advisor_netid="jbrown",
                                advisor_type=4)
    a7 = Advisor.objects.create(advisor_name="John Prine",
                                advisor_netid="jprine",
                                advisor_type=5)

    sport1 = Sport.objects.create(sport_code=1)
    sport2 = Sport.objects.create(sport_code=2)
    sport3 = Sport.objects.create(sport_code=3)
    sport4 = Sport.objects.create(sport_code=4)
    sport5 = Sport.objects.create(sport_code=5)
    sport6 = Sport.objects.create(sport_code=6)
    sport7 = Sport.objects.create(sport_code=7)
    sport8 = Sport.objects.create(sport_code=8)
    sport9 = Sport.objects.create(sport_code=9)
    sport10 = Sport.objects.create(sport_code=10)
    sport11 = Sport.objects.create(sport_code=11)

    upload = Upload.objects.create(file="foo.txt",
                                   type=1,
                                   uploaded_by="javerage",
                                   week=w1)

    dp1 = DataPoint.objects.create(
        type=1,
        week=w1,
        student_name="J1",
        student_number=3456,
        netid="asddw",
        premajor=True,
        priority_score=-4,
        activity_score=-4,
        assignment_score=-4,
        grade_score=-4,
        upload=upload,
        advisor=a1,
        is_stem=False,
        signin_score=2.1,
        class_code="1")
    dp1.sports.set([sport1, sport3])
    dp1.save()

    dp2 = DataPoint.objects.create(
        type=1,
        week=w1,
        student_name="J2",
        student_number=74635,
        netid="fghjtydf",
        premajor=False,
        priority_score=-1,
        activity_score=-1,
        assignment_score=-1,
        grade_score=-1,
        upload=upload,
        advisor=a2,
        is_stem=True,
        signin_score=-2.,
        class_code="1")
    dp2.sports.set([sport2])
    dp2.save()

    dp3 = DataPoint.objects.create(
        type=1,
        week=w1,
        student_name="L1",
        student_number=485465,
        netid="dfgrsfg",
        premajor=True,
        priority_score=4,
        activity_score=4,
        assignment_score=4,
        grade_score=4,
        upload=upload,
        advisor=a2,
        is_stem=False,
        signin_score=3.1,
        class_code="1")
    dp3.sports.set([sport3])

    dp4 = DataPoint.objects.create(
        type=1,
        week=w1,
        student_name="J3",
        student_number=75464,
        netid="sdfgdsfg",
        premajor=True,
        priority_score=-3,
        activity_score=-3,
        assignment_score=-3,
        grade_score=-3,
        upload=upload,
        is_stem=False,
        signin_score=2.1,
        class_code="2")
    dp4.sports.set([sport4])
    dp4.save()

    dp5 = DataPoint.objects.create(
        type=1,
        week=w1,
        student_name="K1",
        student_number=854684,
        netid="sdfgdsfg",
        premajor=False,
        priority_score=0,
        activity_score=0,
        assignment_score=0,
        grade_score=0,
        upload=upload,
        advisor=a2,
        is_stem=False,
        signin_score=-4.1,
        class_code="3")
    dp5.sports.set([sport5])
    dp5.save()

    dp6 = DataPoint.objects.create(
        type=1,
        week=w2,
        student_name="K2",
        student_number=146575,
        netid="sdfgasdft4",
        premajor=True,
        priority_score=1,
        activity_score=1,
        assignment_score=1,
        grade_score=1,
        upload=upload,
        advisor=a2,
        is_stem=False,
        signin_score=-4.1,
        class_code="3")
    dp6.sports.set([sport6])
    dp6.save()

    dp7 = DataPoint.objects.create(
        type=2,
        week=w1,
        student_name="K3",
        student_number=5877,
        netid="GDFhjedsry",
        premajor=False,
        priority_score=3,
        activity_score=3,
        assignment_score=3,
        grade_score=3,
        upload=upload,
        advisor=a2,
        is_stem=False,
        signin_score=-4.1,
        class_code="4")
    dp7.sports.set([sport7])
    dp7.save()

    dp8 = DataPoint.objects.create(
        type=3,
        week=w1,
        student_name="R3",
        student_number=3242,
        netid="asd3a",
        premajor=False,
        priority_score=3,
        activity_score=3,
        assignment_score=3,
        grade_score=3,
        upload=upload,
        advisor=a3,
        is_stem=False,
        signin_score=2.1,
        class_code="4")
    dp8.sports.set([sport8])
    dp8.save()

    dp9 = DataPoint.objects.create(
        type=4,
        week=w1,
        student_name="I1",
        student_number=2356,
        netid="iss1",
        premajor=False,
        priority_score=3,
        activity_score=3,
        assignment_score=3,
        grade_score=3,
        upload=upload,
        advisor=a6,
        is_stem=False,
        signin_score=3.2,
        class_code="4")
    dp9.sports.set([sport9])
    dp9.save()

    dp10 = DataPoint.objects.create(
        type=4,
        week=w1,
        student_name="I2",
        student_number=7629,
        netid="iss2",
        premajor=False,
        priority_score=4,
        activity_score=2,
        assignment_score=2,
        grade_score=3,
        upload=upload,
        advisor=a6,
        is_stem=False,
        signin_score=3.8,
        class_code="8")
    dp10.sports.set([sport10])
    dp10.save()

    dp11 = DataPoint.objects.create(
        type=5,
        week=w1,
        student_name="T1",
        student_number=7629,
        netid="tac1",
        premajor=False,
        priority_score=4,
        activity_score=4,
        assignment_score=5,
        grade_score=5,
        upload=upload,
        advisor=a7,
        is_stem=False,
        signin_score=4.5,
        class_code="8")
    dp11.sports.set([sport11])
    dp11.save()
