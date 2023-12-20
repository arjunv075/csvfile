# HR Management System

This is a simple HR Management System implemented in Python using PostgreSQL for data storage. The system allows you to perform various HR-related tasks, such as initializing the database, importing employee data from a CSV file, retrieving employee information, generating vCards, managing leaves, and more.

## Getting Started

To get started with the HR Management System, follow the instructions below:

### Prerequisites

- Python 3.x
- PostgreSQL database

### Installation

1. Clone the repository:

   ```bash
   https://github.com/arjunv075/csvfile.git

    Install the required dependencies:

    bash

    pip install -r requirements.txt

    Set up the PostgreSQL database and configure the config.ini file with your database details.

####	Usage
	Initialization

	Initialize the database tables:

	bash

	python vcf.py initdb

	Import Employee Data

	Import employee data from a CSV file:

	bash

	python vcf.py import names.csv

	Retrieve Employee Information

	Retrieve information for a specific employee:

	bash

	python vcf.py retrieve <employee-id>

	Generate vCards

	Generate vCards for employees:

	bash

	python vcf.py genvcard -n <number-of-records>

	Manage Leaves

	Input data into the leaves table:

	bash

	python vcf.py initleave <date> <employee-id> <reason>

	Retrieve leave information for an employee:

	bash

	python vcf.py retrieve_leave <employee-id>

	Generate a CSV file with details of employees' leaves:

	bash.

	python vcf.py retrieve_csv -f <filename>
	

