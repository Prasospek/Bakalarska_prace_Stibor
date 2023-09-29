from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taxes.serializers import EmailSerializer
from rest_framework import status
import csv
from taxes.models import Email


from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from taxes.models import Email
from datetime import datetime
from collections import defaultdict
from decimal import Decimal
import io

# Create your views here.

@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#MERGE FILES !!!


@api_view(['POST'])
@csrf_exempt
def merge_csv_files(request):
    csv_files = request.FILES.getlist('files')

    if not csv_files:
        return HttpResponse('No files uploaded', status=400)

    merged_rows = []
    headers = None

    # Initialize dictionaries to store sums for each Ticker and currency
    market_buy_sums = defaultdict(lambda: defaultdict(float))
    market_sell_sums = defaultdict(lambda: defaultdict(float))

    for csv_file in csv_files:
        if csv_file.name.endswith('.csv'):
            csv_data = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            for row in csv_data:
                if not headers:
                    headers = row.keys()
                    merged_rows.append(headers)

                action = row['Action']
                ticker = row['Ticker']
                total = row['Total']
                currency = row['Currency (Total)']

                # Function to convert Euro currency value to float
                def euro_to_float(euro_str):
                    if isinstance(euro_str, str):
                        euro_str = euro_str.replace(',', '.')  # Replace comma with dot
                        return float(euro_str) if euro_str.replace('.', '', 1).isdigit() else 0.0
                    else:
                        return float(euro_str)  # If it's already a float, just return it

                # Function to convert currency to CZK or USD
                def convert_to_czk_or_usd(amount, currency):
                    if currency == 'EUR':
                        czk_amount = amount * 24.54
                        return amount, 'CZK', czk_amount
                    elif currency == 'USD':
                        czk_amount = amount * 0.038  # Assuming 1 USD is approximately 0.038 CZK
                        return amount, 'CZK', czk_amount
                    else:
                        return amount, currency, 0.0

                # Check if the action is a Market buy or Market sell
                if action == 'Market buy':
                    if currency == 'EUR':
                        total_eur = euro_to_float(total)
                        market_buy_sums[ticker]['EUR'] += total_eur
                        amount, currency_czk, czk_amount = convert_to_czk_or_usd(total_eur, 'EUR')
                        row['Total'] = f"{total_eur:.2f} EUR ({czk_amount:.2f} {currency_czk})"
                    else:
                        # Extract exchange rate from the row (you may need to adjust this part)
                        exchange_rate = euro_to_float(row['Exchange rate'])
                        total_eur = euro_to_float(row['Total'])
                        if exchange_rate:
                            total = total_eur / exchange_rate
                            market_buy_sums[ticker][currency] += total
                            amount, currency_czk, czk_amount = convert_to_czk_or_usd(total, currency)
                            row['Total'] = f"{total:.2f} {currency} ({czk_amount:.2f} {currency_czk})"
                elif action == 'Market sell':
                    if currency == 'EUR':
                        total_eur = euro_to_float(total)
                        market_sell_sums[ticker]['EUR'] += total_eur
                        amount, currency_czk, czk_amount = convert_to_czk_or_usd(total_eur, 'EUR')
                        row['Total'] = f"{total_eur:.2f} EUR ({czk_amount:.2f} {currency_czk})"
                    else:
                        # Extract exchange rate from the row (you may need to adjust this part)
                        exchange_rate = euro_to_float(row['Exchange rate'])
                        total_eur = euro_to_float(row['Total'])
                        if exchange_rate:
                            total = total_eur / exchange_rate
                            market_sell_sums[ticker][currency] += total
                            amount, currency_czk, czk_amount = convert_to_czk_or_usd(total, currency)
                            row['Total'] = f"{total:.2f} {currency} ({czk_amount:.2f} {currency_czk})"

                merged_rows.append([row[header] for header in headers])  # Append the original row to merged_rows

    if not merged_rows:
        return HttpResponse('No records found', status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="merged_data.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerows(merged_rows)

    # Output the sums of Market buys and Market sells for each Ticker and currency
    for ticker, buy_sums in market_buy_sums.items():
        for currency, buy_sum in buy_sums.items():
            amount, currency_czk, czk_amount = convert_to_czk_or_usd(buy_sum, currency)
            csv_writer.writerow([f'Sum of Market buys for {ticker} ({currency}):', f"{buy_sum:.2f} {currency} ({czk_amount:.2f} {currency_czk})"])
    for ticker, sell_sums in market_sell_sums.items():
        for currency, sell_sum in sell_sums.items():
            total_eur = euro_to_float(sell_sum)
            amount, currency_czk, czk_amount = convert_to_czk_or_usd(total_eur, currency)
            csv_writer.writerow([f'Sum of Market sells for {ticker} ({currency}):', f"{sell_sum:.2f} {currency} ({czk_amount:.2f} {currency_czk})"])

    return response






