# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import logging
from io import StringIO
from retention_dashboard.models import (
    Week, DataPoint, Advisor, Upload, UploadTypes, Sport)
from django.conf import settings
from django.db import transaction
from django.core.files.storage import default_storage


def get_term_and_week_from_filename(rad_file_name):
    """
    Extracts term and week from RAD data file name

    For example:

    "rad_data/2021-spring-week-10-rad-data.csv" -> "2021-spring", 10
    """
    try:
        if rad_file_name.startswith("rad_data/"):
            rad_file_name = rad_file_name.split("/")[1]
        parts = rad_file_name.split("-")
        term = f"{parts[0]}-{parts[1]}"
        week = int(parts[3])
    except IndexError:
        raise ValueError(f"Unable to parse rad file name: {rad_file_name}")
    return term, week


class StorageDao():
    def get_files_list(self, path="rad_data/"):
        """
        Returns list of file names at the given path.

        :param path: Path to list files at
        :type path: str
        """
        dirs, files = default_storage.listdir(path)

        filenames = []
        for filename in files:
            if filename.endswith('csv'):
                filenames.append(filename)

        logging.debug(f"Found the following bucket files: "
                      f"{','.join(filenames)}")
        return filenames

    def get_latest_file(self):
        """
        Return latest RAD file in bucket
        """
        files = []
        for filename in self.get_files_list():
            sis_term_id, week_num = get_term_and_week_from_filename(filename)
            year = sis_term_id.split("-")[0]
            quarter_num = Week.sis_term_to_quarter_number(sis_term_id)
            data = {"year": year, "quarter_num": quarter_num,
                    "week_num": week_num, "gcs_file": filename}
            files.append(data)
        files.sort(
               key=lambda i: f"{i['year']}{i['quarter_num']}{i['week_num']}",
               reverse=True)
        return files[0]["gcs_file"]

    def download_from_bucket(self, url_key):
        """
        Downloads file a given url_key path from the configured bucket.

        :param url_key: Path of the content to upload
        :type url_key: str
        """
        with default_storage.open(url_key, mode='r') as f:
            content = f.read()
            return content.decode('utf-8')


class UploadDataDao():

    def get_summer_terms_from_string(self, term_string):
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

    def get_upload_types(self, row):
        """
        Return upload type to associate a row with
        """
        upload_types = []
        # if an adviser type is specified, use that as the upload type
        if row.get("adviser_type") == "eop":
            return [UploadTypes.eop]
        elif row.get("adviser_type") == "iss":
            return [UploadTypes.iss]
        # if no adviser type is specified, derive the upload types from the
        # eop, international, isso, and campus_code columns
        if bool(int(row.get("eop", 0))) is True or \
                bool(int(row.get("eop_student", 0))) is True:
            upload_types.append(UploadTypes.eop)
        if bool(int(row.get("international", 0))) is True or \
                bool(int(row.get("international_student", 0))) is True:
            upload_types.append(UploadTypes.international)
        if bool(int(row.get("isso", 0))) is True:
            upload_types.append(UploadTypes.iss)
        if int(row.get("campus_code", 0)) == 2:
            upload_types.append(UploadTypes.tacoma)

        # premajor only if not any other classification, excluding athletics
        if len(upload_types) == 0 and \
                bool(int(row.get("premajor", 0))) is True:
            upload_types.append(UploadTypes.premajor)

        if row.get("sport_code", None):
            upload_types.append(UploadTypes.athletic)

        if not upload_types:
            raise ValueError(f"Unknown upload type for row: {row}")
        return upload_types

    def parse_rad_document(self, rad_document):
        reader = csv.DictReader(StringIO(rad_document),
                                delimiter=',')

        advisor_dict = {}
        record_by_upload = {}
        for _, row in enumerate(reader):
            try:
                upload_types = self.get_upload_types(row)
            except ValueError as err:
                logging.error(err)
                continue
            for upload_type in upload_types:
                if (upload_type != UploadTypes.athletic and
                        row.get("class_code") is not None and
                        row.get("class_code") not in
                        ["0", "1", "2", "3", "4"]):
                    # only include non-undergrads for athletics
                    continue
                advisor_netid = row.get("staff_id")
                advisor_name = row.get("adviser_name")
                advisor = None
                if advisor_netid is not None and advisor_name is not None:
                    advisor_key = "{}_{}".format(advisor_netid,
                                                 upload_type)
                    if advisor_key not in advisor_dict:
                        try:
                            advisor = Advisor.objects.get(
                                                advisor_netid=advisor_netid,
                                                advisor_type=upload_type)
                        except Advisor.DoesNotExist:
                            advisor_name = advisor_name.strip()
                            advisor = Advisor.objects.create(
                                                advisor_netid=advisor_netid,
                                                advisor_type=upload_type,
                                                advisor_name=advisor_name)
                        advisor_dict[advisor_key] = advisor
                    else:
                        advisor = advisor_dict[advisor_key]
                has_a, has_b, has_full = \
                    self.get_summer_terms_from_string(row.get('summer'))
                dp = DataPoint()
                dp.student_name = row.get("student_name_lowc")
                dp.student_number = row.get("student_no")
                dp.netid = row.get("uw_netid")
                dp.class_code = row.get("class_code")
                dp.campus_code = row.get("campus_code")
                dp.is_stem = row.get("stem")
                dp.is_freshman = row.get("incoming_freshman")
                upload_types = self.get_upload_types(row)
                dp.premajor = bool(UploadTypes.premajor in upload_types)
                dp.eop = bool(UploadTypes.eop in upload_types)
                dp.iss = bool(UploadTypes.iss in upload_types)
                dp.international = bool(
                    UploadTypes.international in upload_types)
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
                record = {'datapoint': dp, 'row': row}
                if record_by_upload.get(upload_type):
                    record_by_upload[upload_type].append(record)
                else:
                    record_by_upload[upload_type] = [record]
        return record_by_upload

    def process_rad_upload(self, rad_file_name, rad_document, user, week=None):

        if not week:
            # gcs upload
            sis_term_id, week_num = get_term_and_week_from_filename(
                rad_file_name)
            year = int(sis_term_id.split("-")[0])
            quarter = Week.sis_term_to_quarter_number(sis_term_id)
            week, _ = Week.objects.get_or_create(
                number=week_num,
                quarter=quarter,
                year=year
            )

        record_by_upload = self.parse_rad_document(rad_document)

        for upload_type, records in record_by_upload.items():
            try:
                (Upload.objects.filter(week=week)
                               .filter(type=upload_type)
                               .get())
                logging.warning(f"Upload already exists for "
                                f"term={week.quarter}, "
                                f"week={week.number}, "
                                f"type={upload_type}")
                continue
            except Upload.DoesNotExist:
                with transaction.atomic():
                    upload = Upload.objects.create(file=rad_document,
                                                   type=upload_type,
                                                   week=week,
                                                   uploaded_by=user)
                    for record in records:
                        dp = record['datapoint']
                        if upload.type:
                            dp.type = upload.type
                        if upload.week:
                            dp.week = upload.week
                        if upload:
                            dp.upload = upload
                        dp.upload = upload
                        dp.save()
                        # update sport affiliations after ids have been created
                        row = record["row"]
                        sport_code_str = row.get("sport_code")
                        sport_codes = (sport_code_str.split(",")
                                       if sport_code_str else [])
                        for code in sport_codes:
                            sport_code, _ = Sport.objects.get_or_create(
                                sport_code=code)
                            dp.sports.add(sport_code)
                        dp.save()
                logging.info(f"Upload {len(records)} datapoints for "
                             f"term={week.quarter}, week={week.number}, "
                             f"type={upload_type}")
