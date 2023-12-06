import csv
import queue
import json
import smtplib
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
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
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
# -*- coding: utf-8 -*-

@csrf_exempt
@api_view(['POST'])
def email_submit(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        sender_email = data.get('email')
        validate_email(sender_email)
        message = data.get('message')
        
        if not sender_email or not message:
            return JsonResponse({'error': 'Email ani zpráva nemůžou být prázdné !.'}, status=status.HTTP_400_BAD_REQUEST)
            

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
        non_csv_files = []
        
        
        possible_actions = [
            "Market buy", "Deposit", "Dividend (Ordinary)", "Market sell", "Withdrawal", "Interest on cash"
        ]
        
        expected_columns = [
            "Action", "Time", "ISIN", "Ticker", "Name", "No. of shares", "Price / share",
            "Currency (Price / share)", "Exchange rate", "Result", "Currency (Result)",
            "Total", "Currency (Total)", "Withholding tax", "Currency (Withholding tax)",
            "Charge amount", "Currency (Charge amount)", "Notes", "ID",
            "Currency conversion fee", "Currency (Currency conversion fee)"
        ]
        
        table_data = [
            ["Akce", "Hodnota"],
            ["Akce", "Market sell"],
            ["Ticker", ""],
            ["Počet prodánných akcií", ""],
            ["Čas (Prodeje)", ""],
            ["Ke nezdanění (Akcie)", ""],
            ["Ke nezdanění (Částka)", ""],
            ["Ke zdanění (Akcie)", ""],
            ["Ke zdanění (Částka)", ""],
            ["Daň", ""],
            ["Daň po odečtení ztrát", ""],
            ["Výdělek", ""],
            ["Ztráta (Měna)", ""],
            ["Zbývá: (Akcie)", ""],
        ]     
        
        
        
        # Registering font for special characters
        pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))
        

        
        # Create a PDF buffer
        pdf_buffer = BytesIO()

        # Create a PDF document
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
        pdf.setFont("Calibri", 25)

    
        # Front Page
        add_text(pdf,100,560,"Daňový výpis", 80)
        
        # Current formated date
        formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_text(pdf,70,300, f"Generované dne: {formatted_datetime}", 30)
        add_text(pdf,380,60,"ShareTaxMax 2023©", 20)

        pdf.showPage()

        # get files from FE
        csv_files = request.FILES.getlist('files')
        
        # no files uploaded
        if not csv_files:
            return HttpResponse('Nebyly vložený žadné soubory !', status=400)
        

        # Check content type -> checking MIME (Multipurpose Internet Mail Extensions)
        # Check if ends on .csv
        for csv_file in csv_files:
            if csv_file.content_type != 'text/csv' or not csv_file.name.endswith('.csv'):
                # Handle non-CSV files separately
                non_csv_files.append(csv_file.name)
                error_message = f"Chybné soubory: {', '.join(non_csv_files)}. Prosím vkládejte pouze CSV soubory."
                return HttpResponse(error_message, status=400)
                
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
                
                action_index = headers.index("Action")

                # Skip the header row (if present) and add data rows
                for row in rows[1:]:
                    
                    # Filter Market sell and Market buy for time efficiency
                    if row[action_index] in ["Market sell", "Market buy"]:
                        merged_rows.append(row)
                    # elif (row[action_index] not in possible_actions):
                    #     return HttpResponse(f'${row[action_index]}Chybí části HLAVIČKY souboru !', status=400)
                    
                   
                
        # Sort by time
        merged_rows.sort(key=lambda x: datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'))
        
        for row in merged_rows:
            # create a dictionary pairing individual
            # header with row for easier access to values
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
                    
        current_page = 0
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
                    first_bought = data["qBuy"].get()   # get next buy transaction from queue
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
                    
                current_page += 1
               

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
                
               
                
                data_row = [
                    "Market sell",  # Replace with actual data
                    ticker,          # Replace with actual data
                    str(temp["No. of shares"]),  # Replace with actual data
                    temp["Time"],    # Replace with actual data
                    str(not_for_tax),  # Replace with actual data
                    str((value_to_sell / temp["No. of shares"]) * not_for_tax),  # Replace with actual data
                    str(no_to_sell),  # Replace with actual data
                    str((value_to_sell / temp["No. of shares"]) * no_to_sell),  # Replace with actual data
                    str(tax),  # Replace with actual data
                    str(tax - loss) if tax - loss > 0 else "0",  # Replace with actual data
                    str(value_to_sell),  # Replace with actual data
                    str(loss),  # Replace with actual data
                    str(new)  # Replace with actual data
                  ]
                
                table_data.append(data_row)
             
                
                table_data = [
                    ["Akce", "Hodnota"],
                    ["Akce", "Market sell"],
                    ["Ticker", ticker],
                    ["Počet prodánných akcií", str(temp["No. of shares"])],
                    ["Čas (Prodeje)", temp["Time"]],
                    ["Ke nezdanění (Akcie)", str(not_for_tax)],
                    ["Ke nezdanění (Částka)", str((value_to_sell / temp["No. of shares"]) * not_for_tax)],
                    ["Ke zdanění (Akcie)", str(no_to_sell)],
                    ["Ke zdanění (Částka)", str((value_to_sell / temp["No. of shares"]) * no_to_sell)],
                    ["Daň", str(tax)],
                    ["Daň po odečtení ztrát",  str(tax - loss) if tax - loss > 0 else "0"],
                    ["Výdělek", str(value_to_sell)],
                    ["Ztráta (Měna)", str(loss)],
                    ["Zbývá: (Akcie)", str(new)],
                ] 
      
        
            row_heights = [50, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45]
    
            # DATA
            table = Table(table_data, colWidths=[250, 315], rowHeights=row_heights) 
            
            # Apply styles to the table
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertically
                ('FONTNAME', (0, 0), (-1, 0), 'Calibri'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 20),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 40),
            ])
            
            
            column_style = TableStyle([
                ('FONTNAME', (0, 0), (1, -1), "Calibri"),  # Apply the font to columns 0 and 1
                ('FONTSIZE', (0, 0), (1, -1), 22),  # Adjust the font size for columns 0 and 1
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertically
            ])

            table.setStyle(style)
            table.setStyle(column_style)
            
            pdf.drawString(580, 30, f"{current_page}")

            # Draw the table on the canvas 
            table.wrapOn(pdf, 400, 600)  # Adjust the width and height as needed
            table.drawOn(pdf, 20, 120)  # Adjust the x and y coordinates as needed
            
         

            pdf.showPage()
                
        
        print("--------------------------------------------")
        print("Final tax (Brutto):", final_tax)
        print("Final tax (Netto):", final_tax_netto)
        print("Final loss:", final_tax - final_tax_netto)
        print("--------------------------------------------")
        
        final_loss = final_tax - final_tax_netto
        # PDF  
      
        
        
        
        # Title line
        draw_pdf_line(pdf, 100,640,500,640)
        pdf.drawString(140, 650, "Danový informacní výpis")
        
        # EUR lines
        draw_pdf_line(pdf, 100,510,500,510)
        draw_pdf_line(pdf, 100,400,500,400)
        
        # CZK lines
        draw_pdf_line(pdf, 100,320,500,320)
        draw_pdf_line(pdf, 100,210,500,210)

        pdf.drawString(280, 530, "EUR")

        
        # FINAL EUR
        pdf.drawString(100, 480, f"Finální dan (Brutto): {final_tax:.2f}")
        pdf.drawString(100, 450, f"Finalní dan (Netto):  {final_tax_netto:.2f}")
        pdf.drawString(100, 420, f"Finalní ztráta:  {final_loss:.2f}")
        
        # FINAL CZK
        pdf.drawString(280, 340, "CZK")

        pdf.drawString(100, 290, f"Finální dan (Brutto): {final_tax * 23.54:.2f}")
        pdf.drawString(100, 260, f"Finalní dan (Netto):  {final_tax_netto * 23.54:.2f}")
        pdf.drawString(100, 230, f"Finalní ztráta:  {final_loss * 23.54:.2f}")
        
        
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
    
def add_text(pdf, x, y, text, size=12, font="Calibri"):
    pdf.setFont(font, size)
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
            if csv_file.content_type != 'text/csv' or not csv_file.name.endswith('.csv'):
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
        print(f"Chyba spojování souborů! : {str(e)}")
        return JsonResponse({'error': 'Chyba !'}, status=500)
    
    return response

