import csv
import queue
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from taxes.models import Email
from taxes.serializers import EmailSerializer
from rest_framework import status
from collections import defaultdict
from datetime import datetime, timedelta
from rest_framework.response import Response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def processCSV(request):
    final_tax = 0
    final_tax_netto = 0
    dict_of_queues = {}
    merged_rows = []
    headers = None
    
    
     # Create a PDF buffer
    pdf_buffer = BytesIO()

    # Create a PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

    csv_files = request.FILES.getlist('files')
    

    if not csv_files:
        return HttpResponse('No files uploaded', status=400)

    for csv_file in csv_files:
        if csv_file.name.endswith('.csv'):
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            rows = list(csv_data)

            if not headers:
                headers = rows[0]

            # Skip the header row (if present) and add data rows
            for row in rows[1:]:
                merged_rows.append(row)

    merged_rows.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'))
    
    for row in merged_rows:
        row_data = dict(zip(headers, row))
        if "Market buy" in row_data["Action"]:
            if row_data["Ticker"] in dict_of_queues:
                if "qBuy" in dict_of_queues[row_data["Ticker"]]:
                    dict_of_queues[row_data["Ticker"]]["qBuy"].put(
                        {"No. of shares": float(row_data["No. of shares"]),
                         "Time": row_data["Time"], "Total": float(row_data["Total"])})
                else:
                    dict_of_queues[row_data["Ticker"]]["qBuy"] = queue.Queue()
                    dict_of_queues[row_data["Ticker"]]["qBuy"].put(
                        {"No. of shares": float(row_data["No. of shares"]),
                         "Time": row_data["Time"], "Total": float(row_data["Total"])})
            else:
                qBuy = queue.Queue()
                qBuy.put({"No. of shares": float(row_data["No. of shares"]),
                          "Time": row_data["Time"], "Total": float(row_data["Total"])})
                dict_of_queues[row_data["Ticker"]] = {"qBuy": qBuy}
        if "Market sell" in row_data["Action"]:
            if row_data["Ticker"] in dict_of_queues:
                if "qSell" in dict_of_queues[row_data["Ticker"]]:
                    dict_of_queues[row_data["Ticker"]]["qSell"].put(
                        {"No. of shares": float(row_data["No. of shares"]),
                         "Time": row_data["Time"], "Total": float(row_data["Total"])})
                else:
                    dict_of_queues[row_data["Ticker"]]["qSell"] = queue.Queue()
                    dict_of_queues[row_data["Ticker"]]["qSell"].put(
                        {"No. of shares": float(row_data["No. of shares"]),
                         "Time": row_data["Time"], "Total": float(row_data["Total"])})
            else:
                qSell = queue.Queue()
                qSell.put({"No. of shares": float(row_data["No. of shares"]),
                           "Time": row_data["Time"], "Total": float(row_data["Total"])})
                dict_of_queues[row_data["Ticker"]] = {"qSell": qSell}

    for ticker, data in dict_of_queues.items():
        if "qSell" not in data:
            continue

        temp = 0

        while not data["qSell"].empty():
            temp = data["qSell"].get()
            if "qBuy" not in data:
                break
            first_bought = data["qBuy"].get()
            new = first_bought["No. of shares"] - temp["No. of shares"]
            tax = 0
            no_to_sell = temp["No. of shares"]
            value_to_sell = temp["Total"]
            not_for_tax = 0
            loss = 0
            purchase_date = datetime.strptime(first_bought["Time"], '%Y-%m-%d %H:%M:%S')
            tax_free_date = purchase_date + timedelta(days=3 * 365)

            if (datetime.strptime(temp["Time"], "%Y-%m-%d %H:%M:%S") - purchase_date).days < (365 * 3):
                pass
            else:
                no_to_sell = no_to_sell - first_bought["No. of shares"]
                not_for_tax = not_for_tax + first_bought["No. of shares"]

            if (temp["Total"] / temp["No. of shares"]) < (first_bought["Total"] / first_bought["No. of shares"]):
                loss = loss + (((first_bought["Total"] / first_bought["No. of shares"]) -
                                (temp["Total"] / temp["No. of shares"])) * temp["No. of shares"])

            while new < 0:
                first_bought = data["qBuy"].get()
                new = first_bought["No. of shares"] + new

                if (datetime.strptime(temp["Time"], "%Y-%m-%d %H:%M:%S") - datetime.strptime(first_bought["Time"], "%Y-%m-%d %H:%M:%S")).days < (365 * 3):
                    pass

                else:
                    no_to_sell = no_to_sell - first_bought["No. of shares"]
                    not_for_tax = not_for_tax + first_bought["No. of shares"]

                if (temp["Total"] / temp["No. of shares"]) < (first_bought["Total"] / first_bought["No. of shares"]):
                    loss = loss + (((first_bought["Total"] / first_bought["No. of shares"]) -
                                    (temp["Total"] / temp["No. of shares"])) * temp["No. of shares"])

            tax = (value_to_sell / temp["No. of shares"]) * no_to_sell * 0.23

            temp_queue = queue.Queue()
            temp_queue.put({"No. of shares": new, "Time": first_bought["Time"],
                            "Total": (first_bought["Total"] / first_bought["No. of shares"]) * new})
            while not data["qBuy"].empty():
                temp_queue.put(data["qBuy"].get())
            data["qBuy"] = temp_queue

            final_tax = final_tax + tax
            final_tax_netto = final_tax_netto + (tax - loss)

            print("Action: Market sell")
            print("Ticker:", ticker)
            print("No. of shares (Sold):", temp["No. of shares"])
            print("Time (Sold):", temp["Time"])
            print("Not for tax (Shares):", not_for_tax)
            print("Not for tax (Currency):", (value_to_sell / temp["No. of shares"]) * not_for_tax)
            print("To tax (Shares):", no_to_sell)
            print("To tax (Currency):", (value_to_sell / temp["No. of shares"]) * no_to_sell)
            print("Tax:", tax)
            print("Tax (After loss subtraction):", tax - loss)
            print("Earnings:", value_to_sell)
            print("Loss (Currency):", loss)
            print("Left in stack:", new)
            print()
            
          
             
        
            pdf.setFont("Times-Roman", 18)
            pdf.drawString(100, 770, "___________________________________________________ ")
            pdf.drawString(100, 770, "___________________________________________________ ")
            pdf.drawString(100, 730, "Action: Market sell")
            pdf.drawString(100, 710, "Ticker: " + ticker)
            pdf.drawString(100, 690, "No. of shares (Sold): " + str(temp["No. of shares"]))
            pdf.drawString(100, 670, "Time (Sold): " + temp["Time"])
            pdf.drawString(100, 650, "Not for tax (Shares): " + str(not_for_tax))
            pdf.drawString(100, 630, "Not for tax (Currency): " + str((value_to_sell / temp["No. of shares"]) * not_for_tax))
            pdf.drawString(100, 610, "To tax (Shares): " + str(no_to_sell))
            pdf.drawString(100, 590, "To tax (Currency): " + str((value_to_sell / temp["No. of shares"]) * no_to_sell))
            pdf.drawString(100, 570, "Tax: " + str(tax))
            pdf.drawString(100, 550, "Tax (After loss subtraction): " + str(tax - loss))
            pdf.drawString(100, 530, "Earnings: " + str(value_to_sell))
            pdf.drawString(100, 510, "Loss (Currency): " + str(loss))
            pdf.drawString(100, 490, "Left in stack: " + str(new))
            pdf.drawString(100, 470, "___________________________________________________ ")
            pdf.drawString(100, 470, "___________________________________________________ ")


            pdf.showPage()
            

    print("--------------------------------------------")
    print("Final tax (Brutto):", final_tax)
    print("Final tax (Netto):", final_tax_netto)
    print("--------------------------------------------")
    

    x1, y1 = 100, 640  # Starting point
    x2, y2 = 500, 640
    pdf.line(x1, y1, x2, y2)
    
    # Add content to the PDF
    pdf.setFont("Times-Roman", 23)
    pdf.drawString(190, 650, "Tax Information Report")
    pdf.drawString(100, 470, "____________________________________")

    # Add your tax calculation information to the PDF here
    pdf.drawString(100, 430, f"Final tax (Brutto): {final_tax}")
    pdf.drawString(100, 400, f"Final tax (Netto):  {final_tax_netto}")
    pdf.drawString(100, 380, "___________________________________")

    pdf.save()

    # Reset the buffer position to the beginning
    pdf_buffer.seek(0)

    # Prepare the PDF response
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'

    return response