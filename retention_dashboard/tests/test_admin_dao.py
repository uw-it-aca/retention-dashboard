# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import unittest
from collections import OrderedDict
from django.test import TestCase
from mock import MagicMock
from retention_dashboard.dao.admin import GCSDataDao, UploadDataDao


class TestGCSDataDao(TestCase):

    def get_test_gcs_dao(self):
        dao = GCSDataDao()
        # mock gcs blob
        mock_gcs_blob = MagicMock()
        mock_gcs_blob.upload_from_file = MagicMock(return_value=True)
        mock_gcs_blob.download_as_string = \
            MagicMock(return_value=b"test-return-value")
        # mock gcs bucket
        mock_gcs_bucket = MagicMock()
        mock_gcs_bucket.get_blob = MagicMock(return_value=mock_gcs_blob)
        # mock gcs client
        mock_gcs_client = MagicMock()
        mock_gcs_client.get_bucket = MagicMock(return_value=mock_gcs_bucket)
        f1 = MagicMock()
        f1.name = "rad_data/"
        f2 = MagicMock()
        f2.name = "rad_data/2020-autumn-week-10-rad-data.csv"
        f3 = MagicMock()
        f3.name = "rad_data/2021-summer-week-1-rad-data.csv"
        f4 = MagicMock()
        f4.name = "rad_data/2021-spring-week-11-rad-data.csv"
        mock_gcs_client.list_blobs = MagicMock(
            return_value=[f1, f2, f3, f4])
        mock_gcs_client.get_bucket = MagicMock(return_value=mock_gcs_bucket)
        # mock dao
        dao.get_gcs_client = MagicMock(return_value=mock_gcs_client)
        dao.get_gcs_bucket_name = MagicMock(return_value="test_gcs_bucket")
        return dao

    def test_download_from_gcs_bucket(self):
        dao = self.get_test_gcs_dao()
        content = dao.download_from_gcs_bucket("test_url_key")
        self.assertEqual(content, "test-return-value")

    def test_get_files_list(self):
        dao = self.get_test_gcs_dao()
        self.assertEqual(dao.get_files_list(),
                         ["rad_data/2020-autumn-week-10-rad-data.csv",
                          "rad_data/2021-summer-week-1-rad-data.csv",
                          "rad_data/2021-spring-week-11-rad-data.csv"])

    def test_get_latest_gcs_file(self):
        dao = GCSDataDao()
        dao.get_files_list = \
            MagicMock(
                return_value=["rad_data/2020-autumn-week-10-rad-data.csv",
                              "rad_data/2021-summer-week-1-rad-data.csv",
                              "rad_data/2020-winter-week-12-rad-data.csv",
                              "rad_data/2021-spring-week-10-rad-data.csv",
                              "rad_data/2021-spring-week-11-rad-data.csv",
                              "rad_data/2021-spring-week-12-rad-data.csv"])
        latest_file = dao.get_latest_gcs_file()
        self.assertEqual(latest_file,
                         "rad_data/2021-summer-week-1-rad-data.csv")

    def test_get_term_and_week_from_filename(self):
        dao = GCSDataDao()

        term, week = dao.get_term_and_week_from_filename(
                                "rad_data/2020-autumn-week-10-rad-data.csv")
        self.assertEqual(term, "2020-autumn")
        self.assertEqual(week, 10)

        term, week = dao.get_term_and_week_from_filename(
                                "rad_data/2021-summer-week-1-rad-data.csv")
        self.assertEqual(term, "2021-summer")
        self.assertEqual(week, 1)

        term, week = dao.get_term_and_week_from_filename(
                                "2021-winter-week-11-rad-data.csv")
        self.assertEqual(term, "2021-winter")
        self.assertEqual(week, 11)

        with self.assertRaises(ValueError):
            dao.get_term_and_week_from_filename(
                                "2021_winter_week_11_rad_data.csv")


class TestUploadDataDao(TestCase):

    def test_get_upload_types(self):
        dao = UploadDataDao()
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('staff_id', 'osureb'),
             ('sign_in', '-0.3887894787550641'), ('stem', '1'),
             ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '0'), ('isso', '0'),
             ('campus_code', '0'), ('summer', 'A-B')])
        self.assertEqual(dao.get_upload_types(row), [1])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('staff_id', 'osureb'),
             ('sign_in', '-0.3887894787550641'), ('stem', '1'),
             ('incoming_freshman', '0'), ('premajor', '0'),
             ('eop', '1'), ('international', '0'), ('isso', '0'),
             ('campus_code', '0'), ('summer', 'A-B')])
        self.assertEqual(dao.get_upload_types(row), [2])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('staff_id', 'osureb'),
             ('sign_in', '-0.3887894787550641'), ('stem', '1'),
             ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '1'), ('international', '0'), ('isso', '0'),
             ('campus_code', '0'), ('summer', 'A-B')])
        self.assertEqual(dao.get_upload_types(row), [2])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('staff_id', 'osureb'),
             ('sign_in', '-0.3887894787550641'), ('stem', '1'),
             ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '1'), ('isso', '0'),
             ('campus_code', '2'), ('summer', 'A-B')])
        self.assertEqual(dao.get_upload_types(row), [3, 5])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('staff_id', 'osureb'),
             ('sign_in', '-0.3887894787550641'), ('stem', '1'),
             ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '1'), ('isso', '1'),
             ('campus_code', '2'), ('summer', 'A-B')])
        self.assertEqual(dao.get_upload_types(row), [3, 4, 5])


if __name__ == "__main__":
    unittest.main()