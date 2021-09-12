# online-pajak-test
An online-pajak technical test as part of the hiring process.

## Objectives
To design and build a Django application that will serve the following API endpoints:
- verification of third-parties: this endpoint will be used to verified if a third-party company is a user of our platforms using solely its name. 
- scoring of commercial relationship between companies: this endpoint will be used to assess how frequent 2 companies can be confirmed to be transacting with one another

## Usage

Clone the project

    git clone git@github.com:viirak/online-pajak-test.git

Setup VENV

    python3 -m venv .venv

Activate VENV

    source .venv/bin/activate

Install required packages

    pip install -r requirements.txt

Migrate database

    python manage.py migrate

Run server

    python manage.py runserver

The development server should be started at http://127.0.0.1:8000/

## API Doc

To view the API doc, simply just visit http://localhost:8000/docs/ after the development server has started.
    http://localhost:8000/docs/

## Endpoints

This application provides 2 endpoints, (1) for the company validation -- to verify if it is a user within the system, and (2) is for getting the relationship scoring between two companies.

### Validation

    GET [host:port]/invoices/companies/validate/<company_name>

**company_name**: is string of company's full name. It can include whitespaces in between words.


### Relationship

    GET [host:port]/invoices/companies/relationship/<company_names>

**company_names**: is string of both company's full name, separated by comma. It can include whitespaces in between words.

## Application Design

### Model

The application uses the [provided] test invoice data file which also included in this repo too -- it can be found in the data folder. The file is in the Apache Parquet file format.

To access the invoice data, the application use the InvoiceData class in the models.py file. This class use pandas library to read the content and load it as DataFrame which provides access to rows and columns of the invoice data.

the InvoiceData class provides two methods for looking up invoice records that contains company's name or vendor's name.

1. get_invoices_by_company_name(company_name)

Get the company_name in lower case, then compare with each of the InvoiceData's data through the "company_name" and "vendor_name" column's value. When match with either the company_name or vendor_name column's value, record will be collected.

2. get_related_invoices(company_name, vendor_name)

Get the company_name and vendor_name both in lower case, then compare with each of the InvoiceData's data through the "company_name" and "vendor_name" column's value. Match when both company name and vendor name exist in the record.

### Views

CompanyValidationView

This class provides the company validation view. To verify if the company is a user in the system, it uses the InvoiceData model's get_invoices_by_company_name method to look for any invoice record that contains the company name. If there's invoice belong to the company, it means that the company exist in the system.

CompanyRelationView

This class provides calculation of the commercial relationship between companies. To calculate the relationship score, it uses the InvoiceData model's get_related_invoices method by taking the company's name and vendor's name as params and then lookup for the invoice records. 

If there's no invoice records, it means that there's no relation between the two companies hence the score value will be null.

If there's records, it means that there's relation between the two companies. Score is calculated by
- total records found
- average time (day) between each records (invoice date)

More invoice records indicates that the two companies have done a lot businesses with each other meaning that their relationship is strong. Less record, the relationship is weak. However, the relationship is even more stronger if time distance between each record transactions are shorter which mean the two companies have done business with each other quite frequence, and if the time is long, it means their relationship is become weaker.

So, let's say 1 invoice is 1 point, and this point will be decreased by over time.

step = 30 (number of days that decrease 1 point) this can be changed to shorter or longer

score = total - average_delay/step

If score is negative, it will be 0. As we do not want to have negative score, 0 meaning that the relationship between the two companies need to be restored.

The value of score is scale down using logarithm based 10.

score = log10(total - average_delay/step)