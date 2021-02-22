import fnmatch
import os
import re
from copy import copy
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from retention_dashboard.models import Upload, Week, DataPoint, Advisor
from retention_dashboard.utilities.upload import process_upload
from retention_dashboard.utilities.logger import RetentionLogger


class InvalidUploadException(Exception):
    """
    Exception thrown when there is an error parsing the upload.
    """

    def __init__(self, message="Upload invalid"):
        self.message = message
        super().__init__(self.message)


class InvalidFileException(Exception):
    """
    Exception thrown when there is an error reading a file.
    """

    def __init__(self, message="File invalid"):
        self.message = message
        super().__init__(self.message)


class Command(BaseCommand):
    help = "Upload a directory of data files in bulk."

    def add_arguments(self, parser):
        parser.add_argument("--path",
                            type=str,
                            help="Directory or file path for files to upload",
                            required=True)
        parser.add_argument("--user",
                            type=str,
                            help="Username label for upload",
                            required=True)
        parser.add_argument("--log_file",
                            type=str,
                            help=("Path of log file. If no log path is "
                                  "supplied then stdout is used"),
                            required=False)
        parser.add_argument("--delete_existing_data",
                            help=("Delete all Advisor, Week, Datapoint, and "
                                  "Upload entries before the bulk upload"),
                            action="store_true")
        group = parser.add_argument_group(
            """
            The year, quarter, and week arguments for this utility are by
            default extracted from the directory structure. For example:

            * spr20/ --> spr (quarter=Spring) 20 (year=2020)
              * 1/ or week-01/ --> week=1
              * 2/ or week-02/ --> week=2
            * su20/ --> su (quarter=Summer) 20 (year=2020)
              * 1/ or week-01/ --> week=1
              * 2/ or week-02/ --> week=2
            * au20/ --> au (quarter=Autumn) 20 (year=2020)
              * 1/ or week-01/ --> week=1
              * 2/ or week-02/ --> week=2
            * wtr20/ --> wtr (quarter=Winter) 20 (year=2020)
              * 1/ or week-01/ --> week=1
              * 2/ or week-02/ --> week=2

            Use filters to exclude certain directories.
            """)
        group.add_argument("--year_filter", type=str, default="*",
                           help=("Year of upload. By default uses the year "
                                 "defined in the first directory name "
                                 "following the convention au20/ --> 20 "
                                 "--> year=2020. Supports glob style "
                                 "epression (*,? wildcards)."))
        group.add_argument("--quarter_filter", type=str, default="*",
                           help=("Quarter of upload. By default uses the "
                                 "quarter from the first directory name "
                                 "following the convention au20/ --> au "
                                 "--> quarter=autumn. Options include "
                                 "SPR (Spring), SU (Summer), AU (Autumn), "
                                 "and WTR (Winter). Supports glob style "
                                 "epression (*,? wildcards)."))
        group.add_argument("--week_filter", type=str, default="*",
                           help=("Week of upload. By default uses "
                                 "the week defined in the second "
                                 "directory name following the "
                                 "convention 2/ --> week=2. "
                                 "Supports glob style epression "
                                 "(*,? wildcards)."))

    def handle(self, *args, **options):
        """
        The handle method is the main management command. It runs the following
        steps:

        1.) Walks directory structure to produce a list of dictionaries
        representing the standard directory / file structure.
        2.) Filters the  abstracted directory structure to remove any undesired
        directories.
        3.) Parses and uploads all filtered files to the database.
        """
        self.logger = RetentionLogger(logpath=options["log_file"])
        path = options["path"]
        user = options["user"]
        delete_existing_data = options["delete_existing_data"]
        if delete_existing_data:
            self.delete_existing_data()
        dir_and_files = \
            self.parse_directories_and_files(path)
        filtered = self.filter_dir_and_files(dir_and_files,
                                             options["year_filter"],
                                             options["quarter_filter"],
                                             options["week_filter"])
        if filtered:
            uploaded_files_count = 0
            attempted_file_uploads = 0
            # files with an unrecognized name
            invalid_files_count = 0
            # files that attempt to load but results in an IntegrityError
            integrity_errors_count = 0
            for params in filtered:
                for wk in params["weeks"]:
                    for f in wk["files"]:
                        fd = open(f["path"], "r")
                        try:
                            document = fd.read()
                        except UnicodeDecodeError as ex:
                            invalid_files_count += 1
                            raise InvalidFileException(
                                message=("Error reading: {}. {}"
                                         .format(f["relative_path"], ex))
                            )
                        attempted_file_uploads += 1
                        try:
                            week_obj, _ = \
                                Week.objects.get_or_create(
                                                    year=params["year"],
                                                    quarter=params["quarter"],
                                                    number=wk["number"])
                            upload, created = Upload.objects.get_or_create(
                                                            file=document,
                                                            type=f["type"],
                                                            week=week_obj,
                                                            uploaded_by=user)
                            process_upload(upload)
                            uploaded_files_count += 1
                        except IntegrityError as ex:
                            # continue if unique constraint is violated
                            self.logger.warning(
                                "IntegrityError File: {}"
                                .format(f["relative_path"]))
                            self.logger.warning("IntegrityError: {}"
                                                .format(ex))
                            integrity_errors_count += 1
                            pass
                        fd.close()
            self.logger.info("Skipped {} files that had an error when reading."
                             .format(invalid_files_count))
            self.logger.info("Skipped {} files that resulted in an "
                             "IntegrityError."
                             .format(integrity_errors_count))
            self.logger.info("Successfully loaded {} of {} files."
                             .format(uploaded_files_count,
                                     attempted_file_uploads))
        else:
            raise Exception("No files under {} matching quarter_filter={}, "
                            "week_filter={}, year_filter={}"
                            .format(path,
                                    options["year"],
                                    options["quarter"],
                                    options["week"]))

    def delete_existing_data(self):
        self.logger.info("Deleting all existing entries before upload.")
        Upload.objects.all().delete()
        self.logger.info("Deleted all Upload entries.")
        Week.objects.all().delete()
        self.logger.info("Deleted all Week entries.")
        DataPoint.objects.all().delete()
        self.logger.info("Deleted all DataPoint entries.")
        Advisor.objects.all().delete()
        self.logger.info("Deleted all Advisor entries.")

    def split_alpha_numeric(self, value):
        """
        Splits a string into alpha and numeric substrings.

        For example: "au20" --> ["au", "20"]

        :param value: String to split
        :type value: str
        :return: List containing alpha and numeric substrings
        :rtype: list
        """
        return re.findall(r"[^\W\d_]+|\d+", value)

    def listdir_fullpath(self, dir_name):
        """
        Returns a list of tuples (directory name, file name) of files in the
        supplied directory.

        :param dir_name: name of diretory to list
        :type value: str
        """
        return [(dir_name, file_name) for file_name in os.listdir(dir_name)]

    def get_file_type(self, file_name):
        """
        Returns file type (number) based on file name.

        :param file_name: name of file
        :type value: str
        """
        file_type = None
        file_name = file_name.upper()
        if (file_name == "PREMAJOR-STUDENTS.CSV"):
            file_type = 1
        elif (file_name == "EOP-STUDENTS.CSV"):
            file_type = 2
        elif (file_name == "INTERNATIONAL-STUDENTS.CSV"):
            file_type = 3
        elif (file_name == "ISS-STUDENTS.CSV"):
            file_type = 4
        else:
            raise ValueError("File type for {} is unknown."
                             .format(file_name))
        return file_type

    def get_quarter_info(self, quarter_code):
        """
        Returns quarter info for the specified code.

        :param quarter_code: code name of the quarter
        :type value: str
        """
        quarter_definitions = {
            "WTR": {"quarter_name": "Winter", "quarter": 1},
            "SPR": {"quarter_name": "Spring", "quarter": 2},
            "SU": {"quarter_name": "Summer", "quarter": 3},
            "AU": {"quarter_name": "Autumn", "quarter": 4},
        }
        try:
            return quarter_definitions[quarter_code.upper()]
        except KeyError:
            raise ValueError("Quarter code {} is undefined. Options are "
                             "WTR, SPR, SU, and AU."
                             .format(quarter_code))

    def get_week_from_dir_name(self, dir_name):
        """
        Parses week from directory name based on the standard
        convention (week-## or #).

        :param dir_name: name of the week directory to parse
        :type value: str
        """
        # Parse week from second directory name
        dn = dir_name.upper()
        week = None
        try:
            if dn.startswith("WEEK"):
                week = int(dn.split("-")[-1])
            else:
                week = int(dn)
        except ValueError:
            raise ValueError("Skipping week directory. Unable to parse the "
                             "week number from the directory {}. The "
                             "directory name be either numeric or follow the "
                             "pattern week-##.".format(dir_name))
        if week < 1 or week > 52:
            raise ValueError("Skipping week directory {}. Week {} is out of "
                             "range. Weeks must be from 1-52."
                             .format(dir_name, week))
        return week

    def is_quarater_dir(self, dir_name):
        """
        Check if a directory represents a quarter based on the standard
        convention (<quarter code><two number year> e.g. au20).

        :param dir_name: name of the directory to check
        :type value: str
        """
        dn = dir_name.upper()
        if(dn.startswith("SPR") or
           dn.startswith("SU") or
           dn.startswith("AU") or
           dn.startswith("WTR")):
            return True
        else:
            return False

    def is_week_dir(self, dir_name):
        """
        Check if a directory represents a week based on the standard
        convention (week-## or #).

        :param dir_name: name of the directory to check
        :type value: str
        """
        dn = dir_name.upper()
        if dn.startswith("WEEK") or dn.isnumeric():
            return True
        else:
            return False

    def parse_directories_and_files(self, path):
        """
        Iterates over a standard directory structure to produce a list
        of dictionaries representing the data to upload.

        The year, quarter, and week arguments for this utility are
        extracted from the directory structure. For example:

        * spr20/ --> spr (quarter=Spring) 20 (year=2020)
            * 1/ or week-01/ --> week=1
              * premajor-students.csv
              * eop-students.csv
              * international-students.csv
            * 2/ or week-02/ --> week=2
        * su20/ --> su (quarter=Summer) 20 (year=2020)
            * 1/ or week-01/ --> week=1
            * 2/ or week-02/ --> week=2
        * au20/ --> au (quarter=Autumn) 20 (year=2020)
            * 1/ or week-01/ --> week=1
            * 2/ or week-02/ --> week=2
        * wtr20/ --> wtr (quarter=Winter) 20 (year=2020)
            * 1/ or week-01/ --> week=1
            * 2/ or week-02/ --> week=2

        :param path: Path to root directory of files to process
        :type value: str
        :return: List of dictionaries representing the data to upload.

        For example:
        {
            "quarter":2,
            "year":"2020",
            "weeks":[{
                    "number":"8",
                    "files":[{
                        "path":"data/su20/week-08/premajor-students.csv",
                        "type":1
                        }, {
                        "path":"data/su20/week-08/eop-students.csv",
                        "type":2
                        }, {
                        "path":"data/su20/week-08/international-students.csv",
                        "type":3
                        }, {
                        "path":"data/su20/week-08/iss-students.csv",
                        "type":4
                        }]
                }]
        }
        :rtype: list
        """
        params_list = []
        params = None
        skipped_files_count = 0
        for root_path, qtr_dir_name in self.listdir_fullpath(path):
            params = {"quarter": None, "quarter_name": None, "year": None,
                      "weeks": []}
            if self.is_quarater_dir(qtr_dir_name):
                # Parse quarter and year values from first directory name
                qtr_dir = os.path.join(root_path, qtr_dir_name)
                qtr, year = self.split_alpha_numeric(qtr_dir_name)
                try:
                    qtr_info = self.get_quarter_info(qtr)
                except ValueError as ex:
                    raise InvalidUploadException(message=ex)
                params["quarter"] = qtr_info["quarter"]
                params["quarter_name"] = qtr_info["quarter_name"]
                params["year"] = "20" + year
                for _, week_dir_name in self.listdir_fullpath(qtr_dir):
                    if self.is_week_dir(week_dir_name):
                        try:
                            # Parse week from second directory name
                            week = self.get_week_from_dir_name(week_dir_name)
                        except ValueError as ex:
                            self.logger.warning(ex)
                            continue
                        # Process files
                        wk = {"number": week, "files": []}
                        week_dir = os.path.join(qtr_dir, week_dir_name)
                        for f in os.listdir(week_dir):
                            relative_path = \
                                ("{}/{}/{}"
                                 .format(qtr_dir_name, week_dir_name, f))
                            try:
                                file_type = self.get_file_type(f)
                            except ValueError:
                                skipped_files_count += 1
                                self.logger.warning(
                                    "Skipping {}. File type is unknown."
                                    .format(relative_path))
                                continue
                            wk["files"].append({"path":
                                                os.path.join(week_dir, f),
                                                "relative_path":
                                                relative_path,
                                                "type": file_type})
                        if wk.get("files") is not None:
                            params["weeks"].append(wk)
                        else:
                            # skip any week containing no files
                            continue
                if not params["weeks"]:
                    # skip any quarter containing no weeks
                    continue
                else:
                    # only add params containing a quarter, weeks, and files
                    params_list.append(params)
        if not params_list:
            raise InvalidUploadException(
                  message=("No files to process. Are you using the correct "
                           "directory structure. See the example on the "
                           "example in the docs."))
        self.logger.info("Skipped {} unrecognized files."
                         .format(skipped_files_count))
        return params_list

    def filter_dir_and_files(self, dir_and_files, year_filter,
                             quarter_filter, week_filter):
        """
        Given a list of dictionaries from the
        parse_directories_and_files method, retuns a new filtered list
        using the glob expressions provided by the year_filter, quarter_filter,
        and week filter parameters.

        :param dir_and_files: List of dictionaries representing the
            data to upload.
        :type dir_and_files: list
        :param year_filter: Glob expression for year filter. For example,
            "2*" allows all years on and after 2000.
        :type year_filter: str
        :param quarter_filter: Glob expression for quarter filter. For
            example, "S*" allows all quarters starting with "S".
        :type quarter_filter: str
        :param week_filter: Glob expression for week filter. For
            example, "1*" allows all weeks starting with "1" (i.e. 1, 11, 12).
        :type week_filter: str
        :return: List containing alpha and numeric substrings
        :rtype: list
        """
        filtered = []
        for params in dir_and_files:
            if (not fnmatch.fnmatch(str(params["year"]), year_filter)):
                continue
            if (not fnmatch.fnmatch(str(params["quarter"]), quarter_filter)):
                continue
            new_params = copy(params)
            new_params["weeks"] = []
            for week in params["weeks"]:
                if (fnmatch.fnmatch(str(week["number"]), week_filter)):
                    new_params["weeks"].append(week)
            if new_params["weeks"]:
                filtered.append(new_params)
        return filtered
