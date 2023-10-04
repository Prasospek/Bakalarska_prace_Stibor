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

    # Calculate taxes
    tax_results = calculate_taxes(filtered_rows, headers)

    # Create a CSV response with the filtered and sorted data, including tax results
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_data.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerows(filtered_rows)

    # Add tax results to the CSV file
    csv_writer.writerow([])  # Add an empty row for separation
    csv_writer.writerow(['Tax Results'])  # Add a header for tax results
    for key, value in tax_results.items():
        csv_writer.writerow([key, value])


    return response



def calculate_taxes(merged_rows, headers):
    # Check if headers is not None and has at least one element
    if headers is None or len(headers) == 0:
        return {}  # Return an empty dictionary when there are no headers

    # Calculate taxes and store results in a dictionary
    tax_results = {
        'Ticker': [],
        'Total Market Sell (EUR)': [],
        'Total Market Sell (USD)': [],
    }

    # Define a dictionary to track purchase and sale history for each security
    security_history = {}

    # Iterate through the merged rows to calculate taxes
    for row in merged_rows:
        # Check if the row contains at least as many elements as there are headers
        if len(row) >= len(headers):
            # Convert row to a dictionary
            row_dict = dict(zip(headers, row))
            action = row_dict.get('Action', '')
            ticker = row_dict.get('Ticker', '')
            total = row_dict.get('Total', '')
            currency_total = row_dict.get('Currency (Total)', '')
            date_str = row_dict.get('Time', '')

            if action == 'Market sell':
                total_eur = 0.0  # Initialize total in EUR for this sale

                # Convert total amount to EUR if it's in USD
                if currency_total == 'USD':
                    exchange_rate = float(row_dict.get('Exchange rate', '1.0'))
                    total_usd = float(total.split(' ')[0])
                    total_eur = total_usd * exchange_rate

                # Check if the security has been sold within the last 3 years
                if ticker in security_history:
                    for purchase_date in security_history[ticker]['purchases']:
                        sale_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        time_held = sale_date - purchase_date
                        if time_held < tax_free_threshold:
                            # This sale is taxable
                            if ticker not in tax_results['Ticker']:
                                tax_results['Ticker'].append(ticker)
                                tax_results['Total Market Sell (EUR)'].append(total_eur)
                            else:
                                index = tax_results['Ticker'].index(ticker)
                                tax_results['Total Market Sell (EUR)'][index] += total_eur
                            break  # Stop checking previous purchases

                # Update security history with the sale date
                if ticker not in security_history:
                    security_history[ticker] = {'purchases': []}
                security_history[ticker]['purchases'].append(datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S'))

    return tax_results





