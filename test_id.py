import os
import csv
import pytest
from id import generate_vcard


@pytest.fixture
def sample_data():
    return [
        ("noel", "john", "accountant", "noel.john@example.com", "1234"),
    ]


def test_generate_vcard(tmp_path, sample_data):
    output_directory = tmp_path / "vcf_files"
    output_directory.mkdir()

    for entry in sample_data:
        first_name, last_name, title, email, phone = entry
        vcard = generate_vcard(first_name, last_name, title, email, phone)
        file_name = f"{email.lower()}_card.vcf"
        file_path = output_directory / file_name

        with open(file_path, "w") as vcard_file:
            vcard_file.write(vcard)

        assert file_path.is_file()
