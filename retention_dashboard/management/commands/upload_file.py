# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from retention_dashboard.dao.admin import StorageDao, UploadDataDao
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Upload latest RAD data file'

    def handle(self, *args, **options):
        dao = StorageDao()
        rad_file_name = dao.get_latest_file()
        rad_document = dao.download_from_bucket(rad_file_name)
        UploadDataDao().process_rad_upload(rad_file_name, rad_document, "auto")
