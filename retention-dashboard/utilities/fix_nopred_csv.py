import csv


"""
Deidentifies data in analytics csv
"""
def fix(in_path, out_path):
    headers = []
    fixed = []
    with open(in_path, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if len(headers) == 0:
                headers = [i for i in row]
            fixed.append(get_row(row))
    headers.append("pred")

    with open(out_path, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        writer.writerows(fixed)
    #

def get_row(row):
    stu_num = row['student_no']
    netid = row['uw_netid']
    name = row['student_name_lowc']
    premajor = row['premajor']
    acti = row['activity']
    assi = row['assignments']
    grade = row['grades']
    pred = "-99"

    return [netid, stu_num, name, premajor, acti, assi, grade, pred]
