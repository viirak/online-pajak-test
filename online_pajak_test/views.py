from statistics import mean
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InvoiceData
from .utils import get_diff_days, get_score
from rest_framework.permissions import AllowAny


class CompanyValidationView(APIView):
    """
    View to validate a company in the system.
    """

    permission_classes = (AllowAny,)

    def get(self, request, company_name):
        """
        Check to verify if a third-party company is exist in the system.
        
        To validate a company, make an HTTP GET to this company validation \
        resource URI.
        
        When creating a new request via the API, you must include the \
        company_name parameter. This value is the full company name which \
        include whitespaces like for example: "Perum Hassanah Iswahyudi"
        """
        name = company_name.lower()
        invoices = InvoiceData().get_invoices_by_company_name(name)
        is_company_exist = len(invoices) > 0
        str_exist = "exists" if is_company_exist else "does not exist"
        msg = "The company name: \"{}\" {} in the system.".format(
          company_name, str_exist)
        response_status = status.HTTP_200_OK if is_company_exist \
          else status.HTTP_404_NOT_FOUND
        return Response(data={"message": msg},status=response_status)


class CompanyRelationView(APIView):
    """
    View to get the relationship score between two companies to assess how \
    frequent 2 companies can be confirmed to be transacting with one another.
    """

    permission_classes = (AllowAny,)

    def get(self, request, company_names):
        """
        Retrieve the relationship score between companies.
        To get the relationship score between two companies, make an HTTP GET \
        request to this company relationship resource URI. 
        
        When creating a new request to this API, you must include the \
        company_names parameter. This value is the two company's full name \
        which include whitespaces separated by comma (,) like for example: \
        "Perum Hassanah Iswahyudi,CV Maryati Suryatmi Tbk"
        """
        slugs = company_names.split(',')
        rows = InvoiceData().get_related_invoices(
            slugs[0].lower(), slugs[1].lower())
        invoice_count = len(rows)
        if not rows.empty:
          average_day_delayed = 0
          if (invoice_count > 1):
            invoice_dates = rows['invoice_date'].tolist()
            diff_days = [get_diff_days(
                invoice_dates[i-1], invoice_dates[i]) \
                  for i in range(len(invoice_dates)) if (i > 0)]
            average_day_delayed = mean(diff_days)
          score = get_score(invoice_count, average_day_delayed)
          return Response(data={
            "score": score,
            "message": "There's relationship between these companies."
          }, status=status.HTTP_200_OK)
        else:
          return Response(data={
              "score": None,
              "message": "There's no relationship between these companies."
          }, status=status.HTTP_404_NOT_FOUND)
