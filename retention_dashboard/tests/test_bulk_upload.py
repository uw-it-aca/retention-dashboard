# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import unittest
from retention_dashboard.management.commands.bulk_upload import Command
from retention_dashboard.utilities.logger import RetentionLogger
from unittest.mock import MagicMock


class TestBulkUpload(unittest.TestCase):

    def test_parse_directories_and_files(self):

        def mock_listdir_fullpath(d):
            root = "retention_dashboard/tests/data/"
            if (d.endswith(root)):
                # mock the root directory
                yield root, "su20"
            else:
                yield root, "2"
                yield root, "week-3"

        data_dir = os.path.join(os.path.dirname(__file__),
                                "retention_dashboard/tests/data/")
        command = Command()
        command.logger = RetentionLogger()
        command.listdir_fullpath = \
            MagicMock(side_effect=mock_listdir_fullpath)
        os.listdir = MagicMock(
            return_value=["eop-students.csv", "international-students.csv",
                          "premajor-students.csv", "iss-students.csv",
                          "tacoma-students.csv"])
        result = command.parse_directories_and_files(data_dir)

        # make paths relative for test reproducability
        for d in result:
            for wk in d["weeks"]:
                for f in wk["files"]:
                    f["path"] = os.path.relpath(f["path"])

        result0 = result[0]
        self.assertEqual(result0["quarter"], 3)
        self.assertEqual(result0["quarter_name"], "Summer")
        self.assertEqual(result0["year"], "2020")

        weeks = sorted(result0["weeks"], key=lambda x: x["number"])
        week2 = weeks[0]
        self.assertEqual(week2["number"], 2)
        week2files = sorted(week2["files"], key=lambda x: x["type"])
        week2file0 = week2files[0]
        self.assertEqual(week2file0["type"], 1)
        self.assertEqual(
            week2file0["path"],
            "retention_dashboard/tests/data/su20/2/premajor-students.csv")
        week2file1 = week2files[1]
        self.assertEqual(week2file1["type"], 2)
        self.assertEqual(
            week2file1["path"],
            "retention_dashboard/tests/data/su20/2/eop-students.csv")
        week2file2 = week2files[2]
        self.assertEqual(week2file2["type"], 3)
        self.assertEqual(
            week2file2["path"],
            "retention_dashboard/tests/data/su20/2/international-students.csv")
        week2file3 = week2files[3]
        self.assertEqual(week2file3["type"], 4)
        self.assertEqual(
            week2file3["path"],
            "retention_dashboard/tests/data/su20/2/iss-students.csv")
        week2file4 = week2files[4]
        self.assertEqual(week2file4["type"], 5)
        self.assertEqual(
            week2file4["path"],
            "retention_dashboard/tests/data/su20/2/tacoma-students.csv")

        week3 = weeks[1]
        self.assertEqual(week3["number"], 3)
        week3files = sorted(week3["files"], key=lambda x: x["type"])
        week3file0 = week3files[0]
        self.assertEqual(week3file0["type"], 1)
        self.assertEqual(
            week3file0["path"],
            "retention_dashboard/tests/data/su20/week-3/premajor-students.csv")
        week3file1 = week3files[1]
        self.assertEqual(week3file1["type"], 2)
        self.assertEqual(
            week3file1["path"],
            "retention_dashboard/tests/data/su20/week-3/eop-students.csv")
        week3file2 = week3files[2]
        self.assertEqual(week3file2["type"], 3)
        self.assertEqual(
            week3file2["path"],
            "retention_dashboard/tests/data/su20/week-3/"
            "international-students.csv")
        week3file3 = week3files[3]
        self.assertEqual(week3file3["type"], 4)
        self.assertEqual(
            week3file3["path"],
            "retention_dashboard/tests/data/su20/week-3/iss-students.csv")
        week3file4 = week3files[4]
        self.assertEqual(week3file4["type"], 5)
        self.assertEqual(
            week3file4["path"],
            "retention_dashboard/tests/data/su20/week-3/tacoma-students.csv")


if __name__ == "__main__":
    unittest.main()
