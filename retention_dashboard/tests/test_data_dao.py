import json
from django.test import TestCase, Client
from retention_dashboard.dao.data import get_filtered_data, get_weeks_with_data
from retention_dashboard.tests import create_initial_data
from retention_dashboard.models import Week, DataPoint, Upload


class WeekTest(TestCase):
    def setUp(self):
        create_initial_data()

    def test_get_weeks(self):
        weeks = get_weeks_with_data()
        self.assertEqual(len(weeks), 2)
        week_nums = []
        for week in weeks:
            week_nums.append(week.number)
        self.assertFalse(3 in week_nums)


class DataTest(TestCase):
    week = None

    def setUp(self):
        create_initial_data()
        self.week = Week.objects.get(id=1)

    def test_basic_data(self):
        data = get_filtered_data("OMAD", self.week)
        self.assertEqual(len(data), 5)

        data = get_filtered_data("EOP", self.week)
        self.assertEqual(len(data), 1)

    def test_range_filter(self):
        data = get_filtered_data("OMAD", self.week, grade_filters=["low"])
        self.assertEqual(len(data), 2)

        data = get_filtered_data("OMAD", self.week, grade_filters=["low",
                                                                   "avg"])
        self.assertEqual(len(data), 4)

        data = get_filtered_data("OMAD", self.week, grade_filters=["low",
                                                                   "avg",
                                                                   "high"])
        self.assertEqual(len(data), 5)

        data = get_filtered_data("OMAD",
                                 self.week,
                                 grade_filters=["low"],
                                 activity_filters=["low"],
                                 assignment_filters=["low"],
                                 priority_filters=["low"])
        self.assertEqual(len(data), 2)

    def test_premajor_filter(self):
        data = get_filtered_data("OMAD", self.week, premajor_filter=True)
        self.assertEqual(len(data), 3)

    def test_text_filter(self):
        data = get_filtered_data("OMAD", self.week, text_filter="J")
        self.assertEqual(len(data), 3)