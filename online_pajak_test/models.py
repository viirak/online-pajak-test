import pandas as pd
from pathlib import Path


class InvoiceData(object):
    """
    The Invoice data object to provide access to the invoice \
    data source in the parquet file.
    """
    def __init__(self, *args):
        super(InvoiceData, self).__init__(*args)
        INVOICE_FILE = Path(__file__).parent.resolve()\
            .joinpath('../data/test_invoices.parquet')  # return DataFrame
        self.df = pd.read_parquet(INVOICE_FILE, \
          columns=['company_name', 'vendor_name', 'invoice_date'], \
            engine='pyarrow')

    def get_invoices_by_company_name(self, company_name):
        """
        Get the company name (in lower case), and return the record found
        as in DataFrame.
        """
        a = self.df['company_name'].str.lower() == company_name
        b = self.df['vendor_name'].str.lower() == company_name
        return self.df.loc[a | b] # DataFrame

    def get_related_invoices(self, company_name, vendor_name):
        """
        Get the company name, and vendor name (both in lower case), and 
        return the record found as in DataFrame.
        """
        a = (self.df['company_name'].str.lower() == company_name) & (
            self.df['vendor_name'].str.lower() == vendor_name)
        b = (self.df['company_name'].str.lower() == vendor_name) & (
            self.df['vendor_name'].str.lower() == company_name)
        return self.df.loc[a | b]
