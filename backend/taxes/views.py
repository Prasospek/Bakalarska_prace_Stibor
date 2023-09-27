from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taxes.serializers import EmailSerializer
from rest_framework import status
import csv
from taxes.models import Email
import pandas as pd
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from taxes.models import Email
from datetime import datetime

from decimal import Decimal
import io

# Create your views here.


#MERGE FILES !!!

# @api_view(['POST'])
# @csrf_exempt
# def merge_csv_files(request):
#     csv_files = request.FILES.getlist('files')

#     if not csv_files:
#         return HttpResponse('No files uploaded', status=400)

#     merged_rows = []
#     headers = None

#     for csv_file in csv_files:
#         if csv_file.name.endswith('.csv'):
#             csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
#             rows = list(csv_data)

#             if not headers:
#                 headers = rows[0]
#                 merged_rows.append(headers)

#             merged_rows.extend(rows[1:])

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="merged_data.csv"'

#     csv_writer = csv.writer(response)
#     csv_writer.writerows(merged_rows)

#     return response




@api_view(['POST'])
@csrf_exempt
def merge_csv_files(request):
    csv_files = request.FILES.getlist('files')

    if not csv_files:
        return HttpResponse('No files uploaded', status=400)

    merged_rows = []
    headers = None

    total_tax_free = {}
    total_taxed = {}
    total_market_sell = {}
    total_market_buy = {}  # Initialize total for Market Buy by currency

    for csv_file in csv_files:
        if csv_file.name.endswith('.csv'):
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), quoting=csv.QUOTE_MINIMAL)
            rows = list(csv_data)

            if not headers:
                headers = rows[0]
                merged_rows.append(headers)

            for row in rows[1:]:
                action = row[0]
                action_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')

                # Calculate the difference in years
                years_difference = (datetime.now() - action_time).days / 365

                total = float(row[10]) if row[10] else 0.0
                currency = row[7]  # Currency column index may vary; update accordingly

                if action and 'Market sell' in action:  # Check for "Market sell" transactions
                    if currency not in total_market_sell:
                        total_market_sell[currency] = 0.0
                    total_market_sell[currency] += total

                if action and 'Market buy' in action:  # Check for "Market buy" transactions
                    if currency not in total_market_buy:
                        total_market_buy[currency] = 0.0
                    total_market_buy[currency] += total

                if years_difference > 3:
                    if currency not in total_tax_free:
                        total_tax_free[currency] = 0.0
                    total_tax_free[currency] += total
                else:
                    if currency not in total_taxed:
                        total_taxed[currency] = 0.0
                    total_taxed[currency] += total

                merged_rows.append(row)

    if not merged_rows:
        return HttpResponse('No records found', status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="merged_market_data.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerows(merged_rows)

    # Append the grand totals to the end of the CSV by currency
    for currency, amount in total_market_sell.items():
        csv_writer.writerow([f'Market sell with tax ({currency}):', amount])
    for currency, amount in total_market_buy.items():
        csv_writer.writerow([f'Market buy ({currency}):', amount])
    for currency, amount in total_tax_free.items():
        csv_writer.writerow([f'Total tax free ({currency}):', amount])

    return response


@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



