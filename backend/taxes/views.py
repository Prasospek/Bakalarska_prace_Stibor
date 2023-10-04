import csv
import queue
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taxes.models import Email
from taxes.serializers import EmailSerializer
from rest_framework import status
from collections import defaultdict  # Import defaultdict
from datetime import datetime, timedelta

# Define a dictionary to store securities' data
securities = {}


@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        # In your merge_csv_files function, modify the CSV header and writing part like this:

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_data.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerow(['Action', 'Time', 'Ticker', 'Total', 'Currency (Total)'])  # Header for the merged data

    for row in filtered_rows:  # Write the filtered rows first
        csv_writer.writerow(row)

    csv_writer.writerow([])  # Add an empty row for separation

    csv_writer.writerow(['Ticker', 'Number of Market Sells (EUR)', 'Total Market Sells (USD)', 'Number of Market Buys (EUR)', 'Total Market Buys (USD)'])  # Additional header

    for ticker, tax_data in tax_results.items():
        csv_writer.writerow([
            ticker,
            tax_data['num_sells_eur'],
            tax_data['total_sells_usd'],
            tax_data['num_buys_eur'],
            tax_data['total_buys_usd']
        ])

    return response

#s
def calculate_taxes(merged_rows, headers):
    # Calculate taxes and store results in a dictionary
    tax_results = defaultdict(lambda: {'num_sells_eur': 0, 'total_sells_usd': 0.0, 'num_buys_eur': 0, 'total_buys_usd': 0.0})

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
                tax_results[ticker]['num_sells_eur'] += 1
                tax_results[ticker]['total_sells_usd'] += total_eur
            elif currency_total == 'USD':
                total_usd = float(total.split(' ')[0])
                tax_results[ticker]['num_sells_usd'] += 1
                tax_results[ticker]['total_sells_usd'] += total_usd

        elif action == 'Market buy':
            if currency_total == 'EUR':
                total_eur = float(total.split(' ')[0])
                tax_results[ticker]['num_buys_eur'] += 1
                tax_results[ticker]['total_buys_usd'] += total_eur
            elif currency_total == 'USD':
                total_usd = float(total.split(' ')[0])
                tax_results[ticker]['num_buys_usd'] += 1
                tax_results[ticker]['total_buys_usd'] += total_usd

    return tax_results


 
# Načte to CSV, proloopuje řádky a pro každej Buy/Sell to vytvoří do dict_of_queues nový klíč pro daného tickera a nastaví mu 2 queue.
# Pokud již existuje, tak to do queues jen přidá.
# Následně projíždí queues a porovnává (obě FIFO), je potřeba pořešit kontrolu data
def processCSV():
    dict_of_queues = {}
    with open('2022.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if "Market buy" in row["Action"]:
                if row["Ticker"] in dict_of_queues:
                    if "qBuy" in dict_of_queues[row["Ticker"]]:
                        dict_of_queues[row["Ticker"]]["qBuy"].put(
                            {"No. of shares": row["No. of shares"], "Time": row["Time"]})
                    else:
                        dict_of_queues[row["Ticker"]]["qBuy"] = queue.Queue()
                        dict_of_queues[row["Ticker"]]["qBuy"].put(
                            {"No. of shares": row["No. of shares"], "Time": row["Time"]})
                else:
                    qBuy = queue.Queue()
                    qBuy.put({"No. of shares": row["No. of shares"], "Time": row["Time"]})
                    dict_of_queues[row["Ticker"]] = {"qBuy": qBuy}
            if "Market sell" in row["Action"]:
                if row["Ticker"] in dict_of_queues:
                    if "qSell" in dict_of_queues[row["Ticker"]]:
                        dict_of_queues[row["Ticker"]]["qSell"].put(
                            {"No. of shares": row["No. of shares"], "Time": row["Time"]})
                    else:
                        dict_of_queues[row["Ticker"]]["qSell"] = queue.Queue()
                        dict_of_queues[row["Ticker"]]["qSell"].put(
                            {"No. of shares": row["No. of shares"], "Time": row["Time"]})
                else:
                    qSell = queue.Queue()
                    qSell.put({"No. of shares": row["No. of shares"], "Time": row["Time"]})
                    dict_of_queues[row["Ticker"]] = {"qSell": qSell}
        for ticker in dict_of_queues:
            temp=0
            while not ticker["qSell"].empty():
                temp = ticker["qSell"].get()
                first_bought = ticker["qBuy"].get()
                new = first_bought["No. of shares"] - temp["No. of shares"]
                # EXCEPTION když < 0
                temp_queue = queue.Queue()
                # Tady by mělo stačit porovnat čas u first_bought a temp a nastavit nějaký vhodný nový čas pro prvek new
                # nejspíš to bude původní datum, případně pokud se prodejem zredukuje na 0, tak se už nebude přidávat a další řádek se skipne
 
                temp_queue.put({"No. of shares": new, "Time": "DATUM PLACEHOLDER"})  # - jaký datum???
                while not ticker["qBuy"].empty():
                    temp_queue.put(ticker["qBuy"].get())
                ticker["qBuy"] = temp_queue
                print(first_bought["No. of shares"], temp["No. of shares"], new["No. of shares"])
 
processCSV()