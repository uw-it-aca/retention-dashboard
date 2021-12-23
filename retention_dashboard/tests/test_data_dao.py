# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import unittest
from django.test import TestCase
from retention_dashboard.dao.data import FilterDataDao
from retention_dashboard.tests import create_initial_data
from retention_dashboard.models import Week, Advisor


class TestFilterDataDao(TestCase):

    def setUp(self):
        create_initial_data()
        self.week = Week.objects.get(id=1)

    def test_get_weeks(self):
        dao = FilterDataDao()
        weeks = dao.get_weeks_with_data()
        self.assertEqual(len(weeks), 2)
        week_nums = []
        for week in weeks:
            week_nums.append(week.number)
        self.assertFalse(3 in week_nums)

    def test_basic_data(self):
        dao = FilterDataDao()
        data = dao.get_filtered_data("Premajor", self.week)
        self.assertEqual(len(data), 5)

        data = dao.get_filtered_data("EOP", self.week)
        self.assertEqual(len(data), 1)

    def test_range_filter(self):
        dao = FilterDataDao()
        data = dao.get_filtered_data("Premajor", self.week,
                                     grade_filters=["low"])
        self.assertEqual(len(data), 2)

        data = dao.get_filtered_data("Premajor", self.week,
                                     grade_filters=["low", "avg"])
        self.assertEqual(len(data), 4)

        data = dao.get_filtered_data("Premajor", self.week,
                                     grade_filters=["low", "avg", "high"])
        self.assertEqual(len(data), 5)

        data = dao.get_filtered_data("Premajor",
                                     self.week,
                                     grade_filters=["low"],
                                     activity_filters=["low"],
                                     assignment_filters=["low"],
                                     priority_filters=["low"])
        self.assertEqual(len(data), 2)

    def test_premajor_filter(self):
        dao = FilterDataDao()
        data = dao.get_filtered_data("Premajor", self.week,
                                     premajor_filter=True)
        self.assertEqual(len(data), 3)

    def test_text_filter(self):
        dao = FilterDataDao()
        data = dao.get_filtered_data("Premajor", self.week, text_filter="J")
        self.assertEqual(len(data), 3)

    def test_stem_filter(self):
        dao = FilterDataDao()
        data = dao.get_filtered_data("Premajor", self.week, stem_filter=True)
        self.assertEqual(len(data), 1)

    def test_signins_filter(self):
        dao = FilterDataDao()
        data = dao.get_filtered_data("Premajor", self.week,
                                     signins_filters=["low"])
        self.assertEqual(len(data), 1)
        data = dao.get_filtered_data("Premajor", self.week,
                                     signins_filters=["avg"])
        self.assertEqual(len(data), 3)

    def test_class_standing_filter(self):
        dao = FilterDataDao()
        data = dao.get_filtered_data("Premajor", self.week,
                                     class_standing_filter="1")
        self.assertEqual(len(data), 3)
        data = dao.get_filtered_data("Premajor", self.week,
                                     class_standing_filter="2")
        self.assertEqual(len(data), 1)
        data = dao.get_filtered_data("Premajor", self.week,
                                     class_standing_filter="3")
        self.assertEqual(len(data), 1)
        data = dao.get_filtered_data("Premajor", self.week,
                                     class_standing_filter="4")
        self.assertEqual(len(data), 0)
        data = dao.get_filtered_data("EOP", self.week,
                                     class_standing_filter="4")
        self.assertEqual(len(data), 1)
        data = dao.get_filtered_data("International", self.week,
                                     class_standing_filter="4")
        self.assertEqual(len(data), 1)
        data = dao.get_filtered_data("ISS", self.week,
                                     class_standing_filter="4")
        self.assertEqual(len(data), 1)
        data = dao.get_filtered_data("ISS", self.week,
                                     class_standing_filter="8")
        self.assertEqual(len(data), 1)
        data = dao.get_filtered_data("Tacoma", self.week,
                                     class_standing_filter="8")
        self.assertEqual(len(data), 1)
        data = dao.get_filtered_data("Athletics", self.week,
                                     class_standing_filter="8")
        self.assertEqual(len(data), 0)

    def test_get_advisors(self):
        advisors = Advisor.get_all_advisors()
        self.assertEqual(len(advisors['Premajor']), 2)
        self.assertEqual(len(advisors['EOP']), 2)
        self.assertEqual(len(advisors['International']), 1)
        self.assertEqual(len(advisors['ISS']), 1)
        self.assertEqual(len(advisors['Tacoma']), 1)


if __name__ == "__main__":
    unittest.main()
