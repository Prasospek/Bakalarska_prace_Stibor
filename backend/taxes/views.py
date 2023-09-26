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


from decimal import Decimal
import io

# Create your views here.


# @api_view(['POST'])
# def get_action_column(request):
#     csv_files = request.FILES.getlist('files')

#     if csv_files:
#         data_by_file = {}

#         for csv_file in csv_files:
#             if csv_file.name.endswith('.csv'):
#                 csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
#                 header = next(csv_data)
#                 action_column_index = header.index('Action')
#                 file_data = []

#                 for row in csv_data:
#                     file_data.append(dict(zip(header, row)))

#                 data_by_file[csv_file.name] = file_data

#         action_data = []
#         for data in data_by_file.values():
#             action_data.extend([row['Action'] for row in data])

#         response_data = {'data_by_file': data_by_file, 'action_data': action_data}
#         return JsonResponse(response_data)

#     return JsonResponse({'error': 'No files uploaded'}, status=400)


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


# Mergefiles but only market sell
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
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), quoting=csv.QUOTE_MINIMAL)
            rows = list(csv_data)

            if not headers:
                headers = rows[0]
                merged_rows.append(headers)

            for row in rows[1:]:
                if row and row[0] == 'Market sell':  # Filter rows with Action "Market sell"
                    merged_rows.append(row)

    if not merged_rows:
        return HttpResponse('No "Market sell" records found', status=400)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="market_sell_data.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerows(merged_rows)

    return response





@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



