import csv

import os


def generate_vcard(fname, lname, title, email, phone):
    vcard_template = f"""
BEGIN:VCARD
VERSION:2.1
N:{lname};{fname}
FN:{fname} {lname}
ORG:Authors, Inc.
TITLE:{title}
TEL;WORK;VOICE:{phone}
ADR;WORK:;;100 Flat Grape Dr.;Fresno;CA;95555;United States of America
EMAIL;PREF;INTERNET:{email}
REV:20150922T195243Z
END:VCARD
"""
    return vcard_template.strip()


with open("names.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    data = [tuple(row) for row in reader]

output_directory = "/home/arjun/gensheet/vcf_files"

for entry in data:
    first_name, last_name, title, email, phone = entry
    vcard = generate_vcard(first_name, last_name, title, email, phone)
    os.chdir(output_directory)
    file_name = f"{email.lower()}_card.vcf"
    with open(file_name, "w") as vcard_file:
        vcard_file.write(vcard)

    print(f"Generated {file_name}")
