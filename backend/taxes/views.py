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

# Create your views here.


@api_view(['POST'])
def get_action_column(request):
    csv_files = request.FILES.getlist('files')

    if csv_files:
        action_data = []

        for csv_file in csv_files:
            if csv_file.name.endswith('.csv'):
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
                header = next(csv_data)
                action_column_index = header.index('Action')
                action_data.extend([row[action_column_index] for row in csv_data])

        return Response({'action_data': action_data})

    return Response({'error': 'No files uploaded'}, status=400)






@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



