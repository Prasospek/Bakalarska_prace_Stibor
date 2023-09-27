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

    for csv_file in csv_files:
        if csv_file.name.endswith('.csv'):
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            rows = list(csv_data)

            if not headers:
                headers = rows[0]
                merged_rows.append(headers)

            merged_rows.extend(rows[1:])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="merged_data.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerows(merged_rows)

    return response



