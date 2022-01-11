# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from retention_dashboard.dao.admin import GCSDataDao, UploadDataDao
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Upload latest RAD data file from GCS'

    def handle(self, *args, **options):
        dao = GCSDataDao()
        rad_file_name = dao.get_latest_gcs_file()
        rad_document = dao.download_from_gcs_bucket(rad_file_name)
        UploadDataDao().process_rad_upload(rad_file_name, rad_document, "auto")
