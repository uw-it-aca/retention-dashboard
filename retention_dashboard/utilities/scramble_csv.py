# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import random
import string
import names


"""
Deidentifies data in analytics csv
"""


def scramble(in_path, out_path):
    clean_rows = []
    headers = []
    with open(in_path, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if len(headers) == 0:
                headers = [i for i in row]
            clean_rows.append(get_row(row, headers))

    with open(out_path, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        writer.writerows(clean_rows)


def gen_netid():
    alpha = ''.join(random.choice(string.ascii_lowercase) for x in range(6))
    numeric = ''.join(random.choice(string.digits) for x in range(2))
    return alpha+numeric


def gen_stu_num():
    return ''.join(random.choice(string.digits) for x in range(7))


advisors = [("Fred Johnson", "eop"),
            ("Emily Santos-Bacca", "eop"),
            (names.get_full_name(), "eop"),
            (names.get_full_name(), "eop"),
            (names.get_full_name(), "eop"),
            (names.get_full_name(), "eop"),
            (names.get_full_name(), "eop"),
            (names.get_full_name(), "eop"),
            ("Basia Murton", "iss"),
            (names.get_full_name(), "iss"),
            (names.get_full_name(), "iss"),
            (names.get_full_name(), "iss"),
            (names.get_full_name(), "iss"),
            (names.get_full_name(), "iss"),
            (names.get_full_name(), "iss")]


def get_row(row, headers):
    uw_netid = gen_netid()
    student_no = gen_stu_num()
    student_name_lowc = names.get_full_name()
    advisor_name, _ = random.choice(advisors)
    activity = row['activity']
    assignments = row['assignments']
    grades = row['grades']
    pred = row['pred']
    adviser_name = advisor_name
    adviser_type = row['adviser_type']
    staff_id = row['staff_id']
    sign_in = row['sign_in']
    stem = row['stem']
    incoming_freshman = row['incoming_freshman']
    premajor = row['premajor']
    eop = row['eop']
    international = row['international']
    isso = row['isso']
    campus_code = row['campus_code']
    summer = row['summer']
    class_code = row['class_code']
    sport_code = row['sport_code']

    return [
        uw_netid, student_no, student_name_lowc, activity,
        assignments, grades, pred, adviser_name, adviser_type, staff_id,
        sign_in, stem, incoming_freshman, premajor, eop, international, isso,
        campus_code, summer, class_code, sport_code
    ]
