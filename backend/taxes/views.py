import csv
import queue
import json
import smtplib
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from taxes.models import Email
from taxes.serializers import EmailSerializer
from rest_framework import status
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
from django.utils import timezone
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
from postmarker.core import PostmarkClient
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


@csrf_exempt
@api_view(['POST'])
def email_submit(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        sender_email = data.get('email')
        validate_email(sender_email)
        message = data.get('message')

        # Save to the Email model
        email_instance = Email.objects.create(email=sender_email, message=message, sent_at=timezone.now())

        # Email credentials
        smtp_server = config('SMTP_SERVER', default='smtp.gmail.com')
        smtp_port = config('SMTP_PORT', default='587')
        
        my_email = config('EMAIL_USER', default='')
        email_password = config('EMAIL_PASSWORD', default='')

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = my_email
        msg['Subject'] = message

        # Attach the body to the message
        msg.attach(MIMEText(message, 'plain'))

        # Setup the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        # Login to the email account
        server.login(my_email, email_password)

        # Send the email
        server.sendmail(sender_email, my_email, msg.as_string())

        # Quit the server
        server.quit()
        

        return JsonResponse({'message': 'Email uložen a odeslán !'}, status=status.HTTP_200_OK)
    except ValidationError as ve:
        return JsonResponse({'Chyba! Nevalidní emailová adresa'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@csrf_exempt
def processCSV(request):
    try:
        # initialization of variables
        final_tax = 0
        final_tax_netto = 0
        dict_of_queues = {}
        merged_rows = []
        headers = None
        
        expected_columns = [
            "Action", "Time", "ISIN", "Ticker", "Name", "No. of shares", "Price / share",
            "Currency (Price / share)", "Exchange rate", "Result", "Currency (Result)",
            "Total", "Currency (Total)", "Withholding tax", "Currency (Withholding tax)",
            "Charge amount", "Currency (Charge amount)", "Notes", "ID",
            "Currency conversion fee", "Currency (Currency conversion fee)"
        ]
        
        # Create a PDF buffer
        pdf_buffer = BytesIO()

        # Create a PDF document
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

        # get files from FE
        csv_files = request.FILES.getlist('files')
        
        # no files uploaded
        if not csv_files:
            return HttpResponse('Nebyly vložený žadné soubory !', status=400)

        # Check content type -> checking MIME (Multipurpose Internet Mail Extensions)
        # Check if ends on .csv
        for csv_file in csv_files:
            if csv_file.content_type != 'text/csv' or not csv_file.name.endswith('.csv'):
                return HttpResponse('Nevalidní soubory! Prosím vložte soubor typu CSV', status=400)


        # Processing CSV
        for csv_file in csv_files:
            if csv_file.name.endswith('.csv'):
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
                rows = list(csv_data)

                if not headers:
                    headers = rows[0]
                    
                # Check columns
                if not set(expected_columns).issubset(set(headers)):
                    return HttpResponse('Chybí části HLAVIČKY souboru !', status=400)

                # Skip the header row (if present) and add data rows
                for row in rows[1:]:
                    merged_rows.append(row)

        # Sort by time
        merged_rows.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'))
        
        for row in merged_rows:
            # create a dictionary pairing individua
            # l header with row for easier access to values
            row_data = dict(zip(headers, row))  
            
            if "Market buy" in row_data["Action"]:
                #Check if given Ticker in dict_of_queues
                if row_data["Ticker"] in dict_of_queues:
                    if "qBuy" in dict_of_queues[row_data["Ticker"]]:
                        # Information about Market buy trasnaction for ticker to track transactions
                        dict_of_queues[row_data["Ticker"]]["qBuy"].put(
                            {
                            "No. of shares": float(row_data["No. of shares"]),
                            "Time": row_data["Time"], 
                            "Total": float(row_data["Total"])
                            })
                    else:
                        # if qBuy is not present create new queue and add transaction to it
                        dict_of_queues[row_data["Ticker"]]["qBuy"] = queue.Queue()
                        dict_of_queues[row_data["Ticker"]]["qBuy"].put(
                            {
                            "No. of shares": float(row_data["No. of shares"]),
                            "Time": row_data["Time"], 
                            "Total": float(row_data["Total"])
                            })
                else:
                    # new Queue for market buy
                    qBuy = queue.Queue()
                    qBuy.put(
                        {
                            "No. of shares": float(row_data["No. of shares"]),
                            "Time": row_data["Time"], 
                            "Total": float(row_data["Total"])
                        })
                    dict_of_queues[row_data["Ticker"]] = {"qBuy": qBuy}
                    
            if "Market sell" in row_data["Action"]:
                if row_data["Ticker"] in dict_of_queues:
                    if "qSell" in dict_of_queues[row_data["Ticker"]]:
                        # If the Ticker is present and has a "qSell" queue, add the current "Market sell" transaction to the queue
                        dict_of_queues[row_data["Ticker"]]["qSell"].put(
                            {
                            "No. of shares": float(row_data["No. of shares"]),
                            "Time": row_data["Time"], 
                            "Total": float(row_data["Total"])
                            })
                    else:
                        # If the Ticker is present but doesn't have a "qSell" queue, create a new one and add the transaction
                        dict_of_queues[row_data["Ticker"]]["qSell"] = queue.Queue()
                        dict_of_queues[row_data["Ticker"]]["qSell"].put(
                            {
                            "No. of shares": float(row_data["No. of shares"]),
                            "Time": row_data["Time"], 
                            "Total": float(row_data["Total"])
                            })
                else:
                    # If the Ticker is not present, create a new "qSell" queue and add the transaction
                    qSell = queue.Queue()
                    qSell.put(
                        {
                            "No. of shares": float(row_data["No. of shares"]),
                            "Time": row_data["Time"], 
                            "Total": float(row_data["Total"])
                        })
                    dict_of_queues[row_data["Ticker"]] = {"qSell": qSell}
                    
            
        for ticker, data in dict_of_queues.items():
            if "qSell" not in data:
                continue

            temp = 0

            while not data["qSell"].empty():
                # assign next sell transaction from que qSell and assign it to temp
                temp = data["qSell"].get()
                if "qBuy" not in data:
                    break
                # get next buy transaction from qBuy and assign to first_bought
                first_bought = data["qBuy"].get()
                # new number of shares
                new = first_bought["No. of shares"] - temp["No. of shares"]
                # initialization of variables
                tax = 0
                no_to_sell = temp["No. of shares"]
                value_to_sell = temp["Total"]
                not_for_tax = 0
                loss = 0
                purchase_date = datetime.strptime(first_bought["Time"], '%Y-%m-%d %H:%M:%S')
                
                # Time test
                if (datetime.strptime(temp["Time"], "%Y-%m-%d %H:%M:%S") - purchase_date).days < (365 * 3):
                    pass
                else:
                    if no_to_sell - first_bought["No. of shares"]>0:
                        # Reduce the remaining shares to sell by the number of shares from the current buy transaction
                        no_to_sell = no_to_sell - first_bought["No. of shares"]
                        # Add the number of shares from the current buy transaction to the "not_for_tax" variable
                        not_for_tax = not_for_tax + first_bought["No. of shares"]
                    else:
                        not_for_tax=no_to_sell
                        no_to_sell=0                    

                # Calculating potentional loss on shares if share we sold had lower / higher price 
                if (temp["Total"] / temp["No. of shares"]) < (first_bought["Total"] / first_bought["No. of shares"]):
                    # Calculate the loss by comparing the average prices and multiplying by the number of shares sold
                    loss = loss + (((first_bought["Total"] / first_bought["No. of shares"]) -
                                    (temp["Total"] / temp["No. of shares"])) * temp["No. of shares"])
                while new < 0:
                    print("Jsem na nule")
                    first_bought = data["qBuy"].get()   #get next buy transaction from queue
                    new = first_bought["No. of shares"] + new

                    # Time test
                    if (datetime.strptime(temp["Time"], "%Y-%m-%d %H:%M:%S") - datetime.strptime(first_bought["Time"], "%Y-%m-%d %H:%M:%S")).days < (365 * 3):
                        pass

                    else:
                        # If the remaining shares to sell is greater than the current buy transaction, adjust variables
                        if no_to_sell - first_bought["No. of shares"]>0:
                            no_to_sell = no_to_sell - first_bought["No. of shares"]
                            not_for_tax = not_for_tax + first_bought["No. of shares"]
                        else:
                            not_for_tax=no_to_sell
                            no_to_sell=0 

                    # Calculating potentional loss on shares if share we sold had lower / higher price 
                    if (temp["Total"] / temp["No. of shares"]) < (first_bought["Total"] / first_bought["No. of shares"]):
                        loss = loss + (((first_bought["Total"] / first_bought["No. of shares"]) -
                                        (temp["Total"] / temp["No. of shares"])) * temp["No. of shares"])
                        
                
                # Calculatiion of tax
                tax = (value_to_sell / temp["No. of shares"]) * no_to_sell                    

                temp_queue = queue.Queue()
                
                # Add modified buy transaction to temp_queue
                temp_queue.put(
                    {
                        "No. of shares": new, 
                        "Time": first_bought["Time"],
                        "Total": (first_bought["Total"] / first_bought["No. of shares"]) * new
                    })
                
                #Transfer remaining buy transactions to temp_queue
                while not data["qBuy"].empty():
                    temp_queue.put(data["qBuy"].get())
                data["qBuy"] = temp_queue

                final_tax = final_tax + tax
                if tax-loss>0:
                    final_tax_netto = final_tax_netto + (tax - loss)
                else:
                    final_tax_netto = final_tax_netto + (0)

                print("Action: Market sell")
                print("Ticker:", ticker)
                print("No. of shares (Sold):", temp["No. of shares"])
                print("Time (Sold):", temp["Time"])
                print("Not for tax (Shares):", not_for_tax)
                print("Not for tax (Currency):", (value_to_sell / temp["No. of shares"]) * not_for_tax)
                print("To tax (Shares):", no_to_sell)
                print("To tax (Currency):", (value_to_sell / temp["No. of shares"]) * no_to_sell)
                print("Tax:", tax)
                if tax-loss>0:
                    print("Tax (After loss subtraction):", tax - loss)
                else:
                    print("Tax (After loss subtraction):", 0)
                print("Earnings:", value_to_sell)
                print("Loss (Currency):", loss)
                print("Left in stack:", new)
                print()
                
                # PDF GENERATED TEXT
            
                pdf.setFont("Times-Roman", 18)
                draw_pdf_line(pdf, 100,760,500,760)
                draw_pdf_line(pdf, 100,760,500,760)
                
        
                pdf.drawString(100, 730, "Action: Market sell")
                pdf.drawString(100, 710, "Ticker: " + ticker)
                pdf.drawString(100, 690, "No. of shares (Sold): " + str(temp["No. of shares"]))
                pdf.drawString(100, 670, "Time (Sold): " + temp["Time"])
                pdf.drawString(100, 650, "Not for tax (Shares): " + str(not_for_tax))
                pdf.drawString(100, 630, "Not for tax (Currency): " + str((value_to_sell / temp["No. of shares"]) * not_for_tax))
                pdf.drawString(100, 610, "To tax (Shares): " + str(no_to_sell))
                pdf.drawString(100, 590, "To tax (Currency): " + str((value_to_sell / temp["No. of shares"]) * no_to_sell))
                pdf.drawString(100, 570, "Tax: " + str(tax))
                if tax-loss>0:
                    pdf.drawString(100, 550, "Tax (After loss subtraction): " + str(tax - loss))
                else:
                    pdf.drawString(100, 550, "Tax (After loss subtraction): " + str(0))
                pdf.drawString(100, 530, "Earnings: " + str(value_to_sell))
                pdf.drawString(100, 510, "Loss (Currency): " + str(loss))
                pdf.drawString(100, 490, "Left in stack: " + str(new))
            
                draw_pdf_line(pdf, 100,470,500,470)
                draw_pdf_line(pdf, 100,470,500,470)


                pdf.showPage()
                

        print("--------------------------------------------")
        print("Final tax (Brutto):", final_tax)
        print("Final tax (Netto):", final_tax_netto)
        print("Final loss:", final_tax - final_tax_netto)
        print("--------------------------------------------")
        
        final_loss = final_tax - final_tax_netto
        # PDF  
        pdf.setFont("Times-Roman", 35)
        
        # Title line
        draw_pdf_line(pdf, 100,640,500,640)
        pdf.drawString(140, 650, "Tax Information Report")
        
        # EUR lines
        draw_pdf_line(pdf, 100,510,500,510)
        draw_pdf_line(pdf, 100,400,500,400)
        
        # CZK lines
        draw_pdf_line(pdf, 100,320,500,320)
        draw_pdf_line(pdf, 100,210,500,210)

        draw_bold_text(pdf, 280, 530, "EUR", 20)
        pdf.setFont("Times-Roman", 20)
        
        # FINAL EUR
        pdf.drawString(100, 480, f"Final tax (Brutto): {final_tax:.2f}")
        pdf.drawString(100, 450, f"Final tax (Netto):  {final_tax_netto:.2f}")
        pdf.drawString(100, 420, f"Final loss:  {final_loss:.2f}")
        
    # FINAL CZK
        draw_bold_text(pdf, 280, 340, "CZK", 20)
        pdf.setFont("Times-Roman", 20)
        pdf.drawString(100, 290, f"Final tax (Brutto): {final_tax * 23.54:.2f}")
        pdf.drawString(100, 260, f"Final tax (Netto):  {final_tax_netto * 23.54:.2f}")
        pdf.drawString(100, 230, f"Final loss:  {final_loss * 23.54:.2f}")
        
        
        pdf.save()

        # Reset the buffer position to the beginning
        pdf_buffer.seek(0)

        # Prepare the PDF response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'


        return response
    except Exception as e:
        print (f"Error processing CSV: {str(e)}")

        #Genereric error for user
        return HttpResponseServerError("Nastala chyba při zpracování CSV souborů!")

def draw_pdf_line(pdf, x1, y1, x2, y2):
    pdf.line(x1, y1, x2, y2)
    
def draw_bold_text(pdf, x, y, text, font_size):
    pdf.setFont("Times-Bold", font_size)
    pdf.drawString(x, y, text)


@api_view(['POST'])
@csrf_exempt
def merge_csv_files(request):
    try:
        # Files from FE
        csv_files = request.FILES.getlist('files')

        if not csv_files:
            return HttpResponse('No files uploaded', status=400)
   
        # Initialize pandas DataFrame
        merged_data = pd.DataFrame()
        non_csv_files = []

        for csv_file in csv_files:
            if not csv_file.name.endswith('.csv'):
                non_csv_files.append(csv_file.name)
                continue

            df = pd.read_csv(csv_file)
            merged_data = merged_data.append(df, ignore_index=True)

        if non_csv_files:
            # Handle non-CSV files separately
            error_message = f"Chybné soubory: {', '.join(non_csv_files)}. Prosím vkládejte pouze CSV soubory."
            return HttpResponse(error_message, status=400)

        if merged_data.empty:
            return HttpResponse('No matching rows found', status=400)

        # Sort the merged data by the "Time" column ("Time" is the name of the date column)
        merged_data['Time'] = pd.to_datetime(merged_data['Time'], format='%Y-%m-%d %H:%M:%S')
        merged_data.sort_values(by='Time', inplace=True)

        # Type of csv -> download
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="merged_data.csv"'

        merged_data.to_csv(response, index=False)
    except Exception as e:
        # Log the error for further investigation
        print(f"Error merging CSV files: {str(e)}")
        return JsonResponse({'error': 'Chyba !'}, status=500)
    
    return response

