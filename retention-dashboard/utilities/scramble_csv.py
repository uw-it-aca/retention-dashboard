import csv
import random
import string
import names


"""
Deidentifies data in analytics csv
"""
def scramble(in_path, out_path):
    headers = []
    clean_rows = []
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


def get_row(row):
    stu_num = gen_stu_num()
    netid = gen_netid()
    name = names.get_full_name()
    premajor = row['premajor']
    inter = row['international']
    omad = row['omad']
    acti = row['activity']
    assi = row['assignments']
    grade = row['grades']

    return [stu_num, netid, name, premajor, inter, omad, acti, assi, grade]


def gen_netid():
    alpha = ''.join(random.choice(string.ascii_lowercase) for x in range(6))
    numeric = ''.join(random.choice(string.digits) for x in range(2))
    return alpha+numeric


def gen_stu_num():
    return ''.join(random.choice(string.digits) for x in range(7))


scramble("/home/devights/Downloads/example-data.csv", "clean-data.csv")
