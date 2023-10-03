import csv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taxes.models import Email
from taxes.serializers import EmailSerializer
from rest_framework import status
import pandas as pd
from .models import Transaction
from datetime import datetime, timedelta  # Import datetime

# Define a dictionary to store securities' data
securities = {}


@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from datetime import datetime

# ...

@api_view(['POST'])
@csrf_exempt
def merge_csv_files(request):
    csv_files = request.FILES.getlist('files')

    if not csv_files:
        return HttpResponse('No files uploaded', status=400)

    merged_rows = []
    headers = None

    for csv_file in csv_files:
        if csv_file.name.endswith('.csv'):
            csv_data = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

            for row in csv_data:
                if not headers:
                    headers = list(row.keys())
                    merged_rows.append(headers)

                # Replace missing values with empty strings
                for header in headers:
                    if header not in row:
                        row[header] = ''

                # Append the original row to merged_rows
                merged_rows.append([row[header] for header in headers])

                # Update securities dictionary
                action = row.get('Action', '')
                ticker = row.get('Ticker', '')
                date_str = row.get('Time', '')

                if action == 'Market buy':
                    purchase_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    if ticker not in securities:
                        securities[ticker] = {'purchase_date': purchase_date, 'transactions': []}
                    securities[ticker]['transactions'].append({'date': purchase_date, 'action': 'buy'})

                elif action == 'Market sell':
                    if ticker in securities:
                        sale_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        securities[ticker]['transactions'].append({'date': sale_date, 'action': 'sell'})

    if not merged_rows:
        return HttpResponse('No records found', status=400)

    # Filter and sort the merged rows by date for 'Market sell' and 'Market buy'
    filtered_rows = []
    for row in merged_rows:
        if row[0] == 'Market sell' or row[0] == 'Market buy':
            filtered_rows.append(row)

    # Sort the filtered rows by date (assuming date is in the 'Time' column)
    filtered_rows.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'))

    # Create a CSV response with the filtered and sorted data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_data.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerows(filtered_rows)

    return response



def calculate_taxes(merged_rows, headers):
    # Calculate taxes and store results in a dictionary
    tax_results = {
        'Ticker': [],
        'Total Market Sell (EUR)': [],
        'Total Market Sell (USD)': [],
    }

    # Iterate through the merged rows to calculate taxes
    for row in merged_rows:
        # Convert row to a dictionary
        row_dict = dict(zip(headers, row))
        action = row_dict.get('Action', '')
        ticker = row_dict.get('Ticker', '')
        total = row_dict.get('Total', '')
        currency_total = row_dict.get('Currency (Total)', '')

        if action == 'Market sell':
            if currency_total == 'EUR':
                total_eur = float(total.split(' ')[0])
                if ticker not in tax_results['Ticker']:
                    tax_results['Ticker'].append(ticker)
                    tax_results['Total Market Sell (EUR)'].append(total_eur)
                else:
                    index = tax_results['Ticker'].index(ticker)
                    tax_results['Total Market Sell (EUR)'][index] += total_eur
            elif currency_total == 'USD':
                total_usd = float(total.split(' ')[0])
                if ticker not in tax_results['Ticker']:
                    tax_results['Ticker'].append(ticker)
                    tax_results['Total Market Sell (USD)'].append(total_usd)
                else:
                    index = tax_results['Ticker'].index(ticker)
                    tax_results['Total Market Sell (USD)'][index] += total_usd

    # Apply Time Test and calculate taxes based on it
    for ticker in tax_results['Ticker']:
        if ticker in securities:
            short_term_gains_eur = 0
            short_term_gains_usd = 0
            long_term_gains_eur = 0
            long_term_gains_usd = 0

            # Define the time frame for short-term vs. long-term gains (e.g., 6 months)
            time_frame = timedelta(days=180)

            # Sort transactions by date
            transactions = sorted(securities[ticker]['transactions'], key=lambda x: x['date'])

            for i in range(len(transactions)):
                if transactions[i]['action'] == 'sell':
                    sale_date = transactions[i]['date']
                    for j in range(i - 1, -1, -1):
                        if transactions[j]['action'] == 'buy':
                            purchase_date = transactions[j]['date']
                            holding_period = sale_date - purchase_date

                            # Check if it's a short-term or long-term gain
                            if holding_period <= time_frame:
                                short_term_gains_eur += tax_results['Total Market Sell (EUR)'][tax_results['Ticker'].index(ticker)]
                                short_term_gains_usd += tax_results['Total Market Sell (USD)'][tax_results['Ticker'].index(ticker)]
                            else:
                                long_term_gains_eur += tax_results['Total Market Sell (EUR)'][tax_results['Ticker'].index(ticker)]
                                long_term_gains_usd += tax_results['Total Market Sell (USD)'][tax_results['Ticker'].index(ticker)]

            # Store the calculated gains back in tax_results
            tax_results['Short-Term Gains (EUR)'] = short_term_gains_eur
            tax_results['Short-Term Gains (USD)'] = short_term_gains_usd
            tax_results['Long-Term Gains (EUR)'] = long_term_gains_eur
            tax_results['Long-Term Gains (USD)'] = long_term_gains_usd

    return tax_results




