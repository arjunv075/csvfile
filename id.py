import argparse
import logging
import csv
import os
import requests

logger = None

def parse_args():
    parser = argparse.ArgumentParser(prog="id.py", description="Generates log files of generated vcards and QR codes")
    parser.add_argument("opfile", help="Name of input CSV file")
    parser.add_argument("-v", "--verbose", help="Print detailed logging", action='store_true', default=False)
    args = parser.parse_args()
    return args

def setup_logging(log_level):
    global logger
    logger = logging.getLogger("SheetGen")
    handler = logging.StreamHandler()
    fhandler = logging.FileHandler("run.log")
    fhandler.setLevel(logging.DEBUG)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s | %(filename)s:%(lineno)d | %(message)s"))
    fhandler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s | %(filename)s:%(lineno)d | %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(fhandler)

def read_csv(csv_file_path):
    data = []
    with open(csv_file_path, "r") as csvfile:
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

def generate_qr_code(data):
    os.makedirs("./vcf_files", exist_ok=True)
    global count
    count = 1

    for entry in data:
        logger.debug("writing row %d", count)
        count += 1
        first_name, last_name, title, email, phone = entry
        vcard = generate_vcard_template(first_name, last_name, title, email, phone)

        qr_code_url = f"https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl={vcard}"

        response = requests.get(qr_code_url)
        qr_code_image_path = os.path.join("./vcf_files", f"{email.lower()}_qr_code.png")

        with open(qr_code_image_path, "wb") as qr_code_file:
            qr_code_file.write(response.content)
    logger.info("done")

def generate_vcard(csv_file_path):
    os.makedirs("./vcf_files", exist_ok=True)
    global count
    count = 1

    data = read_csv(csv_file_path)

    for entry in data:
        logger.debug("writing row %d", count)
        count += 1
        first_name, last_name, title, email, phone = entry
        vcard = generate_vcard_template(first_name, last_name, title, email, phone)

        file_name = f"{email.lower()}_card.vcf"
        file_path = os.path.join("./vcf_files", file_name)

        with open(file_path, "w") as vcard_file:
            vcard_file.write(vcard)

    logger.info("created vcard files")

def main():
    args = parse_args()

    if args.verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)

    generate_vcard(args.opfile)
    generate_qr_code(read_csv(args.opfile))

if __name__ == "__main__":
    main()
