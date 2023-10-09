import csv
import queue
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taxes.models import Email
from taxes.serializers import EmailSerializer
from rest_framework import status
from collections import defaultdict  # Import defaultdict
from datetime import datetime, timedelta
import os
from io import StringIO

@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
# Načte to CSV, proloopuje řádky a pro každej Buy/Sell to vytvoří do dict_of_queues nový klíč pro daného tickera a nastaví mu 2 queue.
# Pokud již existuje, tak to do queues jen přidá.
# Následně projíždí queues a porovnává (obě FIFO), je potřeba pořešit kontrolu data
@api_view(['POST'])
@csrf_exempt
def processCSVaaaa(csv_data):
    final_tax=0
    final_tax_netto=0
    # SORT CSV , není implicitně by date
    dict_of_queues = {}
    with open('merge.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if "Market buy" in row["Action"]:
                if row["Ticker"] in dict_of_queues:
                    if "qBuy" in dict_of_queues[row["Ticker"]]:
                        dict_of_queues[row["Ticker"]]["qBuy"].put(
                            {"No. of shares": float(row["No. of shares"]), "Time": row["Time"],"Total": float(row["Total"])})
                    else:
                        dict_of_queues[row["Ticker"]]["qBuy"] = queue.Queue()
                        dict_of_queues[row["Ticker"]]["qBuy"].put(
                            {"No. of shares": float(row["No. of shares"]), "Time": row["Time"],"Total": float(row["Total"])})
                else:
                    qBuy = queue.Queue()
                    qBuy.put({"No. of shares": float(row["No. of shares"]), "Time": row["Time"],"Total": float(row["Total"])})
                    dict_of_queues[row["Ticker"]] = {"qBuy": qBuy}
            if "Market sell" in row["Action"]:
                if row["Ticker"] in dict_of_queues:
                    if "qSell" in dict_of_queues[row["Ticker"]]:
                        dict_of_queues[row["Ticker"]]["qSell"].put(
                            {"No. of shares": float(row["No. of shares"]), "Time": row["Time"],"Total": float(row["Total"])})
                    else:
                        dict_of_queues[row["Ticker"]]["qSell"] = queue.Queue()
                        dict_of_queues[row["Ticker"]]["qSell"].put(
                            {"No. of shares": float(row["No. of shares"]), "Time": row["Time"],"Total": float(row["Total"])})
                else:
                    qSell = queue.Queue()
                    qSell.put({"No. of shares": float(row["No. of shares"]), "Time": row["Time"],"Total": float(row["Total"])})
                    dict_of_queues[row["Ticker"]] = {"qSell": qSell}
                    
    for ticker, data in dict_of_queues.items():
        if "qSell" not in data:
            continue  # Skip tickers with no 'qSell' queue

        temp = 0

        while not data["qSell"].empty():
            if ticker=="MSFT":
                pass
            temp = data["qSell"].get()
            if "qBuy" not in data:
                break  # Skip if there is no 'qBuy' queue
            first_bought = data["qBuy"].get()
            new = first_bought["No. of shares"] - temp["No. of shares"]
            # Pokud je new <0, udělej znovu loop
            # Calculate the tax-free date based on the purchase date
            tax=0
            no_to_sell=temp["No. of shares"]
            value_to_sell=temp["Total"]
            not_for_tax=0
            loss=0
            purchase_date = datetime.strptime(first_bought["Time"], '%Y-%m-%d %H:%M:%S')
            tax_free_date = purchase_date + timedelta(days=3*365)  # Assuming 1 year = 365 days
            if (datetime.strptime(temp["Time"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(first_bought["Time"],"%Y-%m-%d %H:%M:%S")).days<(365*3):
                pass
                
            else:
                no_to_sell=no_to_sell-first_bought["No. of shares"]
                not_for_tax=not_for_tax+first_bought["No. of shares"]
            #print("Prodal jsem za kurz {0}/akcie, když jsem kupoval za {1}/akcie".format((temp["Total"]/temp["No. of shares"]),(first_bought["Total"]/first_bought["No. of shares"])))           
            if (temp["Total"]/temp["No. of shares"])<(first_bought["Total"]/first_bought["No. of shares"]):
                loss=loss+(((first_bought["Total"]/first_bought["No. of shares"])-(temp["Total"]/temp["No. of shares"]))*temp["No. of shares"])
            while new<0:
                first_bought = data["qBuy"].get()
                new = first_bought["No. of shares"] +new
                if (datetime.strptime(temp["Time"],"%Y-%m-%d %H:%M:%S")-datetime.strptime(first_bought["Time"],"%Y-%m-%d %H:%M:%S")).days<(365*3):
                    pass
                else:
                    #Odebírám od celkového počtu akcií, akcie, které nedaním
                    no_to_sell=no_to_sell-first_bought["No. of shares"]
                    not_for_tax=not_for_tax+first_bought["No. of shares"]
                #print("Prodal jsem za kurz {0}/akcie, když jsem kupoval za {1}/akcie".format((temp["Total"]/temp["No. of shares"]),(first_bought["Total"]/first_bought["No. of shares"])))           
                if (temp["Total"]/temp["No. of shares"])<(first_bought["Total"]/first_bought["No. of shares"]):
                    loss=loss+(((first_bought["Total"]/first_bought["No. of shares"])-(temp["Total"]/temp["No. of shares"]))*temp["No. of shares"])
            
            #Počet daněných akcií, (vynásobený celkovým ziskem poděleným počtem původních akcií) * 23 %
            #print(float(value_to_sell),temp["No. of shares"],no_to_sell)
            tax=(float(value_to_sell)/temp["No. of shares"])*no_to_sell*0.23
            #print("Prodal jsem {0} s daní {1}".format(temp["No. of shares"],tax))

            temp_queue = queue.Queue()
            temp_queue.put({"No. of shares": new, "Time": first_bought["Time"],"Total":(first_bought["Total"]/first_bought["No. of shares"])*new})
            while not data["qBuy"].empty():
                temp_queue.put(data["qBuy"].get())
            data["qBuy"] = temp_queue

            final_tax=final_tax+tax
            final_tax_netto=final_tax_netto+(tax-loss)


            #print("Action:", "Market buy" if "qBuy" in data else "Market sell")
            print("Action:","Market sell")
            
            print("Ticker:", ticker)
            #print("No. of shares (Bought):", first_bought["No. of shares"])
            #print("Time (Bought):", first_bought["Time"])
            print("No. of shares (Sold):", temp["No. of shares"])
            print("Time (Sold):", temp["Time"])
            print("Not for tax (Shares):",not_for_tax)
            print("Not for tax (Currency):",(float(value_to_sell)/temp["No. of shares"])*not_for_tax)
            print("To tax (Shares):",no_to_sell)
            print("To tax (Currency):",(float(value_to_sell)/temp["No. of shares"])*no_to_sell)
            print("Tax:",tax)
            print("Tax (After loss substraction):",tax-loss)
            print("Earnings:",value_to_sell)
            print("Loss (Currency):", loss)
            print("Left in stack:", new)
            print()  # Add a line break for readability
    print("--------------------------------------------")
    print("Final tax (Brutto):",final_tax)
    print("Final tax (Netto):",final_tax_netto)
    print("--------------------------------------------")



@api_view(['POST'])
@csrf_exempt
def processCSV(request):
    csv_files = request.FILES.getlist('files')

    if not csv_files:
        return HttpResponse('No files uploaded', status=400)

    merged_rows = []
    headers = None

    for csv_file in csv_files:
        if csv_file.name.endswith('.csv'):
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            rows = list(csv_data)

            if not headers:
                headers = rows[0]

            # Skip the header row (if present) and add data rows
            for row in rows[1:]:
                merged_rows.append(row)

    # Sort the merged_rows based on the "Time" column (assuming it's in the second position, adjust index as needed)
    merged_rows.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="merged_data.csv"'

    csv_writer = csv.writer(response)
    
    # Include headers and sorted data in the CSV response
    csv_writer.writerow(headers)
    csv_writer.writerows(merged_rows)

    return response
