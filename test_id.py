import os
from id import read_csv, generate_vcard_template, generate_vcard

def test_read_csv(tmpdir):
    csv_file = tmpdir.join("test_names.csv")
    csv_file.write("noel,john,Developer,noel@example.com,123-4")
    assert read_csv(csv_file) == [["noel", "john", "Developer", "noel@example.com", "123-4"]]

def test_generate_vcard_template():
    assert generate_vcard_template("noel", "john", "Developer", "noel@example.com", "123-4")

def test_generate_vcard(tmpdir):
    output_directory = tmpdir.join("test_vcf_files")
    generate_vcard([["noel", "john", "Developer", "noel@example.com", "123-4"]], output_directory)
    assert len(os.listdir(output_directory)) == 1
