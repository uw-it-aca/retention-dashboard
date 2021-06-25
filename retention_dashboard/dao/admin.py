# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from retention_dashboard.models import Week
from django.conf import settings
from google.cloud import storage
from google.cloud.exceptions import NotFound


class GCSDataDao():

    def __init__(self):
        pass

    def get_gcs_client(self):
        return storage.Client()

    def get_gcs_timeout(self):
        return getattr(settings, "GCS_TIMEOUT", 60)

    def get_gcs_bucket_name(self):
        return getattr(settings, "RAD_DATA_BUCKET_NAME", "")

    def get_files_list(self, path="rad_data/"):
        """
        Returns list of file names in a GCS bucket at the given path.

        :param path: Path to list files at
        :type path: str
        """
        gcs_client = self.get_gcs_client()
        gcs_bucket_name = self.get_gcs_bucket_name()
        bucket = gcs_client.get_bucket(gcs_bucket_name)
        files = []
        for blob in gcs_client.list_blobs(bucket, prefix=path):
            if blob.name.endswith("csv"):
                files.append(blob.name)
        return files

    def get_latest_gcs_file(self):
        """
        Return latest RAD file in GCS bucket
        """
        gcs_files = self.get_files_list()
        files = []
        for gcs_file in gcs_files:
            sis_term_id, week_num = \
                self.get_term_and_week_from_filename(gcs_file)
            year = sis_term_id.split("-")[0]
            quarter_num = Week.sis_term_to_quarter_number(sis_term_id)
            file = {"year": year, "quarter_num": quarter_num,
                    "week_num": week_num, "gcs_file": gcs_file}
            files.append(file)
        sorted(files,
               key=lambda i: (i['year'], i["quarter_num"], i["week_num"]),
               reverse=True)
        return files[0]["gcs_file"]

    def download_from_gcs_bucket(self, url_key):
        """
        Downloads file a given url_key path from the configured GCS bucket.

        :param url_key: Path of the content to upload
        :type url_key: str
        :param content: Content to upload
        :type content: str or file object
        """
        gcs_client = self.get_gcs_client()
        gcs_bucket_name = self.get_gcs_bucket_name()
        bucket = gcs_client.get_bucket(gcs_bucket_name)
        try:
            blob = bucket.get_blob(
                url_key,
                timeout=self.get_gcs_timeout())
            content = blob.download_as_string(
                timeout=self.get_gcs_timeout())
            if content:
                return content.decode('utf-8')
        except NotFound as ex:
            logging.error(f"gcp {url_key}: {ex}")
            raise

    def get_term_and_week_from_filename(self, rad_file_name):
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
