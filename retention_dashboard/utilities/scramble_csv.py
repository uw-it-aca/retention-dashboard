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
            clean_rows.append(get_row(row))

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


advisors = [("Fred Johnson", "fj123"),
            ("Emily Santos-Bacca", "esb99"),
            ("Basia Murton", "bm8567"),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid()),
            (names.get_full_name(), gen_netid())]


def get_row(row):
    stu_num = gen_stu_num()
    netid = gen_netid()
    name = names.get_full_name()
    premajor = row['premajor']
    acti = row['activity']
    assi = row['assignments']
    grade = row['grades']
    pred = row['pred']

    advisor_name, advisor_netid = random.choice(advisors)


    return [netid, stu_num, name, premajor, acti, assi, grade, pred, advisor_name, advisor_netid]
