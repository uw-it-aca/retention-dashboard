# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import logging

from django.db.models.expressions import Value
from retention_dashboard.models import DataPoint, Advisor, Upload, Week
from io import StringIO
from django.db import transaction
from django.db.utils import IntegrityError


def get_upload_types(row):
    """
    Return upload type to associate a row with
    """
    upload_types = []
    if bool(int(row.get("premajor", 0))) is True:
        upload_types.append(1)
    elif bool(int(row.get("eop_student", 0))) is True:
        upload_types.append(2)
    elif bool(int(row.get("international_student", 0))) is True:
        upload_types.append(3)
    elif bool(int(row.get("isso", 0))) is True:
        upload_types.append(4)
    elif bool(int(row.get("tacoma_student", 0))) is True:
        upload_types.append(5)
    else:
        raise ValueError(f"Unknown upload type for row: {row}")
    return upload_types


def get_term_and_week_from_filename(rad_file_name):
    """
    Extracts term and week from RAD data file name

    For example:

    "rad_data/2021-spring-week-10-rad-data.csv" -> "2021-spring", 10
    """
    try:
        parts = rad_file_name.split("/")[1].split("-")
    except KeyError:
        raise ValueError(f"Unable to parse rad file name: {rad_file_name}")
    term = f"{parts[0]}-{parts[1]}"
    week = int(parts[3])
    return term, week


@transaction.atomic
def process_rad_upload(rad_file_name, rad_document, user):

    sis_term_id, week_num = get_term_and_week_from_filename(rad_file_name)
    year = int(sis_term_id.split("-")[0])
    quarter = Week.sis_term_to_quarter_number(sis_term_id)
    week, _ = Week.objects.get_or_create(
        number=week_num,
        quarter=quarter,
        year=year
    )

    data_points = []
    reader = csv.DictReader(StringIO(rad_document),
                            delimiter=',')

    advisor_dict = {}
    for _, row in enumerate(reader):
        dp = DataPoint()
        try:
            upload_types = get_upload_types(row)
        except ValueError as err:
            logging.error(err)
            continue
        for upload_type in upload_types:
            upload, _ = Upload.objects.get_or_create(file=rad_document,
                                                     type=upload_type,
                                                     week=week,
                                                     uploaded_by=user)
            advisor_netid = row.get("staff_id")
            advisor_name = row.get("adviser_name")
            advisor = None
            if advisor_netid is not None and advisor_name is not None:
                if advisor_netid not in advisor_dict:
                    advisor_name = advisor_name.strip()
                    advisor, _ = Advisor.objects.\
                        get_or_create(advisor_netid=advisor_netid,
                                    advisor_type=upload.type,
                                    defaults={'advisor_name': advisor_name})
                    advisor_dict[advisor_netid] = advisor
                else:
                    advisor = advisor_dict[advisor_netid]
            has_a, has_b, has_full = \
                _get_summer_terms_from_string(row.get('summer'))

            if upload.type:
                dp.type = upload.type
            if upload.week:
                dp.week = upload.week
            if upload:
                dp.upload = upload
            dp.student_name = row.get("student_name_lowc")
            dp.student_number = row.get("student_no")
            dp.netid = row.get("uw_netid")
            dp.premajor = row.get("premajor")
            dp.is_stem = row.get("stem")
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
            dp.advisor = advisor
            dp.has_a_term = has_a
            dp.has_b_term = has_b
            dp.has_full_term = has_full
            if not (dp.activity_score and dp.assignment_score and dp.grade_score):
                logging.info(f"Skipping student {dp.student_name} "
                            f"({dp.student_number}. Either a )")
                continue
            data_points.append(dp)

    DataPoint.objects.bulk_create(data_points)


@transaction.atomic
def process_upload(document, type, week, user):
    upload, created = Upload.objects.get_or_create(file=document,
                                                   type=type,
                                                   week=week,
                                                   uploaded_by=user)
    if not created:
        raise IntegrityError("An upload already exists for the specified "
                             "week and type.")

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
