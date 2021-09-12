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
        Return a company that exist in the system.
        """
        name = company_name.lower()
        invoices = InvoiceData().get_invoices_by_company_name(name)
        is_company_exist = len(invoices) > 0
        str_exist = "exists" if is_company_exist else "does not exist"
        msg = "The company name: \"{}\" {} in the system.".format(
          company_name, str_exist)
        response_status = status.HTTP_200_OK if is_company_exist \
          else status.HTTP_404_NOT_FOUND
        return Response(
          data={"exist": is_company_exist, "message": msg},
          status=response_status)


class CompanyRelationView(APIView):
    """
    View to get relationship between companies.
    """

    permission_classes = (AllowAny,)

    def get(self, request, company_names):
        """
        Return the relationship score between companies.

        ---
        parameters:
        - name: username
          description: Foobar long description goes here
          required: true
          type: string
          paramType: form
        - name: password
          paramType: form
          required: true
          type: string
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
