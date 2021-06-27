# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import unittest
from django.test import TestCase
from retention_dashboard.models import DataPoint, Week


class TestDataPoint(TestCase):

    def test_get_data_type_by_text(self):
        self.assertEqual(DataPoint.get_data_type_by_text("Premajor"), 1)
        self.assertEqual(DataPoint.get_data_type_by_text("EOP"), 2)
        self.assertEqual(DataPoint.get_data_type_by_text("International"), 3)
        self.assertEqual(DataPoint.get_data_type_by_text("ISS"), 4)
        with self.assertRaises(ValueError):
            DataPoint.get_data_type_by_text("UNKNOWN TYPE")


class TestWeek(TestCase):

    def test_sis_term_to_quarter_number(self):
        quarter_num = Week.sis_term_to_quarter_number("2021-winter")
        self.assertEqual(quarter_num, 1)
        quarter_num = Week.sis_term_to_quarter_number("2020-spring")
        self.assertEqual(quarter_num, 2)
        quarter_num = Week.sis_term_to_quarter_number("2013-summer")
        self.assertEqual(quarter_num, 3)
        quarter_num = Week.sis_term_to_quarter_number("2021-autumn")
        self.assertEqual(quarter_num, 4)
        with self.assertRaises(ValueError):
            Week.sis_term_to_quarter_number("2021autumn")


if __name__ == "__main__":
    unittest.main()
