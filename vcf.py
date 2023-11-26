import csv
import logging
import argparse
import os
import psycopg2 as pg
import requests
import sys

logger = None


def parse_args():
    parser = argparse.ArgumentParser(
        prog="vcf.py", description="Generates sample employee database as csv"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print detailed logging",
        action="store_true",
        default=False,              
    )   
    parser.add_argument(
        "-n",
        "--number",
        help="Number of records to generate",
        action="store",
        type=int,
        default=100,
    )
    subparser = parser.add_subparsers(dest="subcommand", help="sub-command help")

    parser_initdb = subparser.add_parser(
        "initdb", help="Initialize creation of database and username"
    )
    parser_initdb.add_argument(
        "-u",
        "--user",
        help="Adding user name of database",
        action="store",
        type=str,
        default="arjun",
    )
    parser_initdb.add_argument(
        "-d",
        "--dbname",
        help="Adding database name",
        action="store",
        type=str,
        default="employee",
    )

    parser_load = subparser.add_parser(
        "load", help="Load data to database from csvfile"
    )
    parser_load.add_argument(
        "-c",
        "--csv",
        help="Providing name of csv file",
        action="store",
        type=str,
        default="names.csv",
    )
    parser_load.add_argument(
        "-u",
        "--user",
        help="Adding user name of database",
        action="store",
        type=str,
        default="arjun",
    )
    parser_load.add_argument(
        "-d",
        "--dbname",
        help="Adding database name",
        action="store",
        type=str,
        default="employee",
    )
    parser_load.add_argument(
        "-n",
        "--number",
        help="Number of records to generate",
        action="store",
        type=int,
        default=100,
    )

    parser_load = subparser.add_parser("rtr", help="retrieve data from database")
    parser_load.add_argument(
        "-u",
        "--user",
        help="Adding user name of database",
        action="store",
        type=str,
        default="arjun",
    )
    parser_load.add_argument(
        "-d",
        "--dbname",
        help="Adding database name",
        action="store",
        type=str,
        default="employee",
    )
    parser_load.add_argument(
        "-n",
        "--number",
        help="Number of records to generate",
        action="store",
        type=int,
        default=100,
    )
    parser_load.add_argument(
        "-s",
        "--sizeqr",
        help="Size of qr code png",
        action="store",
        type=int,
        default=500,
    )
    parser_load.add_argument(
        "-q",
        "--qrcode",
        help="Generate both qrcode and vcard files",
        action="store_true",
        default=False,
    )
    parser_load.add_argument(
        "-a",
        "--address",
        help="Provide an address other than default address",
        action="store",
        default="100 Flat Grape Dr.;Fresno;CA;95555;United States of America",
    )

    args = parser.parse_args()
    return args


def implement_log(log_level):
    global logger
    logger = logging.getLogger("genvcf_log")
    handler = logging.StreamHandler()
    fhandler = logging.FileHandler("run.log")
    fhandler.setLevel(logging.DEBUG)
    handler.setLevel(log_level)
    handler.setFormatter(
        logging.Formatter(
            "[%(levelname)s] %(asctime)s | %(filename)s:%(lineno)d | %(message)s"
        )
    )
    fhandler.setFormatter(
        logging.Formatter(
            "[%(levelname)s] %(asctime)s | %(filename)s:%(lineno)d | %(message)s"
        )
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(fhandler)


def details_from_csv(csvfile):
    data = []
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        for item in reader:
            data.append(item)
    return data


def data_from_details(details, number):
    data = []
    for i in range(0, number):
        data.append(details[i])
    return data


def create_database(user, dbase):
    conn = pg.connect(database="postgres", user=user)
    cursor = conn.cursor()
    conn.autocommit = True
    create_database = f"CREATE DATABASE {dbase}"
    cursor.execute(create_database)
    print("Creation of database is successful")
    conn.close()


def create_table(us, db):
    create_database(us, db)
    conn = pg.connect(f"dbname={db} user={us}")
    cursor = conn.cursor()
    create_table = """
                CREATE TABLE details (serial_number SERIAL PRIMARY KEY,
                lastname VARCHAR(50),
                firstname VARCHAR(50),
                title VARCHAR(50),
                email VARCHAR(50),
                phone_number VARCHAR(50))"""
    cursor.execute(create_table)
    print("Table created successfully")
    conn.commit()
    conn.close()


def truncate_table(user, dbname):
    conn = pg.connect(f"dbname={dbname} user={user}")
    cursor = conn.cursor()
    truncate_table = "TRUNCATE TABLE details RESTART IDENTITY CASCADE"
    cursor.execute(truncate_table)
    conn.commit()
    conn.close()


def add_data_to_database(data, user, dbname):
    truncate_table(user, dbname)
    conn = pg.connect(f"dbname={dbname} user={user}")
    cursor = conn.cursor()
    for last_name, first_name, title, email, ph_no in data:
        insert_info = f"""INSERT INTO details (lastname,firstname,title,email,phone_number) VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(insert_info, (last_name, first_name, title, email, ph_no))
        conn.commit()
    print("data inserted")
    conn.close()


def retriving_data_from_database(user, dbname, num):
    data = []
    conn = pg.connect(f"dbname={dbname} user={user}")
    cursor = conn.cursor()
    cursor.execute("SELECT lastname,firstname,title,email,phone_number FROM details")
    conn.commit()
    x = cursor.fetchall()
    for i in range(0, num):
        data.append(x[i])
    conn.close()
    return data


def implement_vcf(first_name, last_name, job, email, ph_no, address):
    return f"""
BEGIN:VCARD
VERSION:2.1
N:{last_name};{first_name}
FN:{first_name} {last_name}
ORG:Authors, Inc.
TITLE:{job}
TEL;WORK;VOICE:{ph_no}
ADR;WORK:;;{address}
EMAIL;PREF;INTERNET:{email}
REV:20150922T195243Z
END:VCARD
"""


def generate_vcf(details, address):
    if not os.path.exists("vcf_files"):
        os.mkdir("vcf_files")
    count = 1
    for first_name, last_name, job, email, ph_no in details:
        imp_vcard = implement_vcf(first_name, last_name, job, email, ph_no, address)
        logger.debug("Writing row %d", count)
        count += 1
        with open(f"vcf_files/{email}.vcf", "w") as j:
            j.write(imp_vcard)
    logger.info("created vcard files")


def implement_qrcode(first_name, last_name, job, email, ph_no, size, address):
    reqs = requests.get(
        f"""https://chart.googleapis.com/chart?cht=qr&chs={size}x{size}&chl=BEGIN:VCARD
VERSION:2.1
N:{last_name};{first_name}
FN:{first_name} {last_name}
ORG:Authors, Inc.
TITLE:{job}
TEL;WORK;VOICE:{ph_no}
ADR;WORK:;;{address}
EMAIL;PREF;INTERNET:{email}
REV:20150922T195243Z
END:VCARD"""
    )
    return reqs.content


def generate_qrcode(details, size, address):
    if not os.path.exists("vcf_files"):
        os.mkdir("vcf_files")
    count = 1
    for first_name, last_name, job, email, ph_no in details:
        imp_qrcode = implement_qrcode(
            first_name, last_name, job, email, ph_no, size, address
        )
        logger.debug("Writing row %d", count)
        count += 1
        with open(f"vcf_files/{email}.qr.png", "wb") as f:
            f.write(imp_qrcode)
    logger.info("created qr code files")


def main():
    args = parse_args()
    if args.verbose:
        implement_log(logging.DEBUG)
    else:
        implement_log(logging.INFO)
    if args.subcommand == "initdb":
        create_table(args.user, args.dbname)
    if args.subcommand == "load":
        details = details_from_csv(args.csv)
        data = data_from_details(details, args.number)
        add_data_to_database(data, args.user, args.dbname)
    if args.subcommand == "rtr":
        details = retriving_data_from_database(args.user, args.dbname, args.number)
        generate_vcf(details, args.address)
        if args.qrcode:
            generate_qrcode(details, args.sizeqr, args.address)


if __name__ == "__main__":
    main()
