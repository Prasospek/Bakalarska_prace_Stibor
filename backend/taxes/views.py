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


# Mergefiles but only market selll
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
#             csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), quoting=csv.QUOTE_MINIMAL)
#             rows = list(csv_data)

#             if not headers:
#                 headers = rows[0]
#                 merged_rows.append(headers)

#             for row in rows[1:]:
#                 if row and row[0] == 'Market sell':  # Filter rows with Action "Market sell"
#                     merged_rows.append(row)

#     if not merged_rows:
#         return HttpResponse('No "Market sell" records found', status=400)

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="market_sell_data.csv"'

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

    # Create variables to track FIFO
    fifo_stocks = []

    for csv_file in csv_files:
        if csv_file.name.endswith('.csv'):
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), quoting=csv.QUOTE_MINIMAL)
            rows = list(csv_data)

            if not headers:
                headers = rows[0]
                merged_rows.append(headers)

            for row in rows[1:]:
                if row and row[0] == 'Market sell':  # Filter rows with Action "Market sell"
                    merged_rows.append(row)

                    # Apply FIFO-based tax calculation
                    calculate_taxes_for_sell(row, fifo_stocks, merged_rows)

    if not merged_rows:
        return HttpResponse('No "Market sell" records found', status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="market_sell_data.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerows(merged_rows)

    return response

def calculate_taxes_for_sell(sell_row, fifo_stocks, merged_rows):
    sell_shares = float(sell_row[5])
    sell_date = pd.to_datetime(sell_row[1])
    total_profit = 0

    while sell_shares > 0 and fifo_stocks:
        buy_shares, buy_date, buy_price = fifo_stocks[0]
        holding_period = (sell_date - pd.to_datetime(buy_date)).days

        if buy_shares <= sell_shares:
            profit = (sell_shares / buy_shares) * (float(sell_row[6]) - buy_price)
            total_profit += profit
            sell_shares -= buy_shares
            fifo_stocks.pop(0)
        else:
            profit = sell_shares * (float(sell_row[6]) - buy_price)
            total_profit += profit
            fifo_stocks[0] = (buy_shares - sell_shares, buy_date, buy_price)
            sell_shares = 0

        # Check if the holding period is greater than 3 years (1095 days)
        if holding_period >= 1095:
            sell_row[-1] = 'Tax-exempt sale'
        else:
            sell_row[-1] = 'Taxable sale'

        # Append tax information to the merged rows
        merged_rows.append(sell_row)
        merged_rows.append(['', '', '', '', '', '', '', '', '', f'Total Profit: {total_profit}', '', '', '', '', '', ''])



@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



