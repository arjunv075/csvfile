import csv
import os
import requests


def read_csv(file_path):
    data = []
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data


def generate_vcard_template(fname, lname, title, email, phone):
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


def generate_qr_code(data, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for entry in data:
        first_name, last_name, title, email, phone = entry
        vcard = generate_vcard_template(first_name, last_name, title, email, phone)

        qr_code_url = f"https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl={vcard}"

        response = requests.get(qr_code_url)
        qr_code_image_path = os.path.join(output_directory, f"{email.lower()}_qr_code.png")

        with open(qr_code_image_path, "wb") as qr_code_file:
            qr_code_file.write(response.content)


def generate_vcard(data, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for entry in data:
        first_name, last_name, title, email, phone = entry
        vcard = generate_vcard_template(first_name, last_name, title, email, phone)

        file_name = f"{email.lower()}_card.vcf"
        file_path = os.path.join(output_directory, file_name)

        with open(file_path, "w") as vcard_file:
            vcard_file.write(vcard)

    print("created vcard files")


def main():
    csv_file_path = "names.csv"
    output_directory = "./vcf_files"

    data = read_csv(csv_file_path)

    generate_vcard(data, output_directory)

    generate_qr_code(data, output_directory)


if __name__ == "__main__":
    main()
