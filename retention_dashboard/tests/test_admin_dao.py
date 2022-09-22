# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from collections import OrderedDict
from django.test import TestCase
from mock import MagicMock, patch
from retention_dashboard.dao.admin import (
    StorageDao, UploadDataDao, get_term_and_week_from_filename)


class TestStorageDao(TestCase):

    @patch('retention_dashboard.dao.admin.default_storage.open')
    def test_download_from_bucket(self, mock_open):
        dao = StorageDao()
        dao.download_from_bucket("test_url_key")
        mock_open.assert_called_with("test_url_key", mode="rb")

    @patch('retention_dashboard.dao.admin.default_storage.listdir')
    def test_get_files_list(self, mock_listdir):
        mock_listdir.return_value = ([], [
            "rad_data/2020-autumn-week-10-rad-data.csv",
            "rad_data/2021-summer-week-1-rad-data.csv",
            "rad_data/2021-spring-week-11-rad-data.csv"])
        dao = StorageDao()
        self.assertEqual(dao.get_files_list(), [
            "rad_data/2020-autumn-week-10-rad-data.csv",
            "rad_data/2021-summer-week-1-rad-data.csv",
            "rad_data/2021-spring-week-11-rad-data.csv"])

    @patch('retention_dashboard.dao.admin.default_storage.listdir')
    def test_get_latest_file(self, mock_listdir):
        mock_listdir.return_value = ([], [
            "rad_data/2020-autumn-week-10-rad-data.csv",
            "rad_data/2021-summer-week-1-rad-data.csv",
            "rad_data/2020-winter-week-12-rad-data.csv",
            "rad_data/2021-spring-week-10-rad-data.csv",
            "rad_data/2021-spring-week-11-rad-data.csv",
            "rad_data/2021-spring-week-12-rad-data.csv"])
        dao = StorageDao()
        self.assertEqual(dao.get_latest_file(),
                         "rad_data/2021-summer-week-1-rad-data.csv")

        mock_listdir.return_value = ([], [
            "rad_data/2020-autumn-week-10-rad-data.csv",
            "rad_data/2022-spring-week-10-rad-data.csv",
            "rad_data/2022-spring-week-11-rad-data.csv",
            "rad_data/2022-spring-week-12-rad-data.csv",
            "rad_data/2022-spring-week-1-rad-data.csv",
            "rad_data/2022-spring-week-2-rad-data.csv",
            "rad_data/2022-spring-week-3-rad-data.csv",
            "rad_data/2022-spring-week-4-rad-data.csv",
            "rad_data/2022-spring-week-5-rad-data.csv",
            "rad_data/2022-spring-week-6-rad-data.csv",
            "rad_data/2022-spring-week-7-rad-data.csv",
            "rad_data/2022-spring-week-8-rad-data.csv",
            "rad_data/2022-spring-week-9-rad-data.csv"
            ])
        dao = StorageDao()
        self.assertEqual(dao.get_latest_file(),
                         "rad_data/2022-spring-week-12-rad-data.csv")

    def test_get_term_and_week_from_filename(self):
        term, week = get_term_and_week_from_filename(
            "rad_data/2020-autumn-week-10-rad-data.csv")
        self.assertEqual(term, "2020-autumn")
        self.assertEqual(week, 10)

        term, week = get_term_and_week_from_filename(
            "rad_data/2021-summer-week-1-rad-data.csv")
        self.assertEqual(term, "2021-summer")
        self.assertEqual(week, 1)

        term, week = get_term_and_week_from_filename(
            "2021-winter-week-11-rad-data.csv")
        self.assertEqual(term, "2021-winter")
        self.assertEqual(week, 11)

        with self.assertRaises(ValueError):
            get_term_and_week_from_filename("2021_winter_week_11_rad_data.csv")


class TestUploadDataDao(TestCase):

    def test_get_upload_types(self):
        dao = UploadDataDao()
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', ''),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '0'), ('isso', '0'),
             ('campus_code', '0'), ('summer', 'A-B'), ('sport_code', None)])
        self.assertEqual(dao.get_upload_types(row), [1])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', ''),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '0'),
             ('eop', '1'), ('international', '0'), ('isso', '0'),
             ('campus_code', '0'), ('summer', 'A-B'), ('sport_code', None)])
        self.assertEqual(dao.get_upload_types(row), [2])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', ''),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '1'), ('international', '0'), ('isso', '0'),
             ('campus_code', '0'), ('summer', 'A-B'), ('sport_code', None)])
        self.assertEqual(dao.get_upload_types(row), [2])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', ''),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '1'), ('isso', '0'),
             ('campus_code', '2'), ('summer', 'A-B'), ('sport_code', None)])
        self.assertEqual(dao.get_upload_types(row), [3, 5])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', ''),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '1'), ('isso', '1'),
             ('campus_code', '2'), ('summer', 'A-B'), ('sport_code', None)])
        self.assertEqual(dao.get_upload_types(row), [3, 4, 5])
        # test for when adviser_type is set
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', 'eop'),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '1'), ('isso', '1'),
             ('campus_code', '2'), ('summer', 'A-B'), ('sport_code', None)])
        self.assertEqual(dao.get_upload_types(row), [2])
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', 'iss'),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '1'), ('isso', '1'),
             ('campus_code', '2'), ('summer', 'A-B'), ('sport_code', None)])
        self.assertEqual(dao.get_upload_types(row), [4])
        # case where sport_code is set and campus is seattle
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', 'foobar'),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '0'),
             ('eop', '0'), ('international', '0'), ('isso', '0'),
             ('campus_code', '1'), ('summer', 'A-B'), ('sport_code', '7,2')])
        self.assertEqual(dao.get_upload_types(row), [6])
        # case where sport_code is set and campus is tacoma
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', 'foobar'),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '0'),
             ('eop', '0'), ('international', '0'), ('isso', '0'),
             ('campus_code', '2'), ('summer', 'A-B'), ('sport_code', '70')])
        self.assertEqual(dao.get_upload_types(row), [5, 6])
        # premajor, tacoma and athlete
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', 'foobar'),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '0'), ('isso', '0'),
             ('campus_code', '1'), ('summer', 'A-B'), ('sport_code', '70')])
        self.assertEqual(dao.get_upload_types(row), [1, 6])
        # case where adviser type was unknown
        row = OrderedDict(
            [('uw_netid', 'fairsp'), ('student_no', '1864017'),
             ('student_name_lowc', 'fairservice,peyton scott'),
             ('activity', '-4.00000000000000000000'),
             ('assignments', '-2.50000000000000000000'),
             ('grades', '0E-20'), ('pred', '4.699061188134724'),
             ('adviser_name', 'Osure Brown'), ('adviser_type', 'foobar'),
             ('staff_id', 'osureb'), ('sign_in', '-0.3887894787550641'),
             ('stem', '1'), ('incoming_freshman', '0'), ('premajor', '1'),
             ('eop', '0'), ('international', '1'), ('isso', '1'),
             ('campus_code', '2'), ('summer', 'A-B'), ('sport_code', None)])
        self.assertEqual(dao.get_upload_types(row), [3, 4, 5])

    @patch('retention_dashboard.dao.admin.Advisor')
    @patch('retention_dashboard.dao.admin.DataPoint')
    @patch('retention_dashboard.dao.admin.csv.DictReader')
    def test_parse_rad_document(self, mock_dict_reader_cls,
                                mock_datapoint_cls, mock_advisor_cls):
        mock_row_1 = {
            'uw_netid': 'scole12', 'student_no': '2101446',
            'student_name_lowc': 'Cole,Shayla',
            'activity': '-2.0',
            'assignments': '-1.3',
            'grades': '-2.35',
            'pred': '', 'adviser_name': '', 'adviser_type': '', 'staff_id': '',
            'sign_in': '-3.4', 'stem': '0',
            'incoming_freshman': '0', 'premajor': '0', 'eop': '0',
            'international': '0', 'isso': '0', 'campus_code': '2',
            'summer': 'Full', 'class_code': '2', 'sport_code': '7'}
        mock_row_2 = {
            'uw_netid': 'javerage', 'student_no': '12435463',
            'student_name_lowc': 'Average,Joe',
            'activity': '-2.0',
            'assignments': '-1.3',
            'grades': '-2.35',
            'pred': '', 'adviser_name': '', 'adviser_type': '', 'staff_id': '',
            'sign_in': '-3.4', 'stem': '0',
            'incoming_freshman': '0', 'premajor': '0', 'eop': '1',
            'international': '0', 'isso': '0', 'campus_code': '2',
            'summer': 'Full', 'class_code': '8', 'sport_code': '7'}
        mock_dict_reader_cls.return_value = [
            mock_row_1,
            mock_row_2
        ]
        dao = UploadDataDao()
        mock_rad_document = ""
        mock_adviser = MagicMock()
        mock_advisor_cls.objects.get = MagicMock(return_value=mock_adviser)
        record_by_upload = dao.parse_rad_document(mock_rad_document)
        # assertions
        self.assertEqual(mock_datapoint_cls.call_count, 3)
        self.assertEqual(mock_advisor_cls.objects.get.call_count, 2)
        self.assertEqual(
            record_by_upload,
            {5: [{'datapoint': mock_datapoint_cls.return_value,
                  'row': mock_row_1}],
             6: [{'datapoint': mock_datapoint_cls.return_value,
                  'row': mock_row_1},
                 {'datapoint': mock_datapoint_cls.return_value,
                  'row': mock_row_2}]}
        )
