# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import unittest
from django.test import TestCase
from retention_dashboard.models import DataPoint


class TestDataPoint(TestCase):

    def test_get_data_type_by_text(self):
        self.assertEqual(DataPoint.get_data_type_by_text("Premajor"), 1)
        self.assertEqual(DataPoint.get_data_type_by_text("EOP"), 2)
        self.assertEqual(DataPoint.get_data_type_by_text("International"), 3)
        self.assertEqual(DataPoint.get_data_type_by_text("ISS"), 4)
        with self.assertRaises(ValueError):
            DataPoint.get_data_type_by_text("UNKNOWN TYPE")


if __name__ == "__main__":
    unittest.main()
