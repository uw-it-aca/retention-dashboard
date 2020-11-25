import os
import unittest
from retention_dashboard.management.commands.bulk_upload import Command
from unittest import mock


class TestBulkUpload(unittest.TestCase):

    def test_parse_directories_and_files(self):

        def mock_listdir_fullpath(d):
            root = "retention_dashboard/data/"
            if (d.endswith(root)):
                # mock the root directory
                yield root, "su20"
            else:
                yield root, "2"
                yield root, "week-3"

        data_dir = os.path.join(os.path.dirname(__file__),
                                "retention_dashboard/data/")
        command = Command()
        command.listdir_fullpath = \
            mock.Mock(side_effect=mock_listdir_fullpath)
        os.listdir = mock.MagicMock(
            return_value=["eop-students.csv", "international-students.csv",
                          "premajor-students.csv"])
        result = command.parse_directories_and_files(data_dir)

        # make paths relative for test reproducability
        for d in result:
            for wk in d["weeks"]:
                for f in wk["files"]:
                    f["path"] = os.path.relpath(f["path"])

        result0 = result[0]
        self.assertEqual(result0["quarter"], 2)
        self.assertEqual(result0["quarter_name"], "Summer")
        self.assertEqual(result0["year"], "2020")

        weeks = sorted(result0["weeks"], key=lambda x: x["number"])
        week2 = weeks[0]
        self.assertEqual(week2["number"], 2)
        week2files = sorted(week2["files"], key=lambda x: x["type"])
        week2file0 = week2files[0]
        self.assertEqual(week2file0["type"], 1)
        self.assertEqual(week2file0["path"],
                         "retention_dashboard/data/premajor-students.csv")
        week2file1 = week2files[1]
        self.assertEqual(week2file1["type"], 2)
        self.assertEqual(week2file1["path"],
                         "retention_dashboard/data/eop-students.csv")
        week2file2 = week2files[2]
        self.assertEqual(week2file2["type"], 3)
        self.assertEqual(week2file2["path"],
                         "retention_dashboard/data/international-students.csv")

        week3 = weeks[1]
        self.assertEqual(week3["number"], 3)
        week3files = sorted(week3["files"], key=lambda x: x["type"])
        week3file0 = week3files[0]
        self.assertEqual(week3file0["type"], 1)
        self.assertEqual(week3file0["path"],
                         "retention_dashboard/data/premajor-students.csv")
        week3file1 = week3files[1]
        self.assertEqual(week3file1["type"], 2)
        self.assertEqual(week3file1["path"],
                         "retention_dashboard/data/eop-students.csv")
        week3file2 = week3files[2]
        self.assertEqual(week3file2["type"], 3)
        self.assertEqual(week3file2["path"],
                         "retention_dashboard/data/international-students.csv")


if __name__ == "__main__":
    unittest.main()
