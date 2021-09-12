import pandas as pd
from pathlib import Path


class InvoiceData(object):
    def __init__(self, *args):
        super(InvoiceData, self).__init__(*args)
        INVOICE_FILE = Path(__file__).parent.resolve()\
            .joinpath('../data/test_invoices.parquet')  # return DataFrame
        self.invoice_df = pd.read_parquet(INVOICE_FILE, \
          columns=['company_name', 'vendor_name', 'invoice_date'], \
            engine='pyarrow')

    def get_invoices_by_company_name(self, company_name):
      a = self.invoice_df['company_name'].str.lower() == company_name
      b = self.invoice_df['vendor_name'].str.lower() == company_name
      return self.invoice_df.loc[a | b] # DataFrame

    def get_related_invoices(self, company_name, vendor_name):
      a = (self.invoice_df['company_name'].str.lower() == company_name) & (
          self.invoice_df['vendor_name'].str.lower() == vendor_name)
      b = (self.invoice_df['company_name'].str.lower() == vendor_name) & (
          self.invoice_df['vendor_name'].str.lower() == company_name)
      return self.invoice_df.loc[a | b]
