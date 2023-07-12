from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taxes.serializers import EmailSerializer
from rest_framework import status
import csv
from django.core.mail import send_mail
from taxes.models import Email

# Create your views here.


@api_view(['POST'])
def csv_data_view(request):
    if 'file' in request.FILES:
        csv_file = request.FILES['file']

        if csv_file.name.endswith('.csv'):
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            header = next(csv_data)
            sticker_column_index = header.index('sticker')
            sticker_data = [row[sticker_column_index] for row in csv_data]

            return Response({'sticker_data': sticker_data})

    return Response({'error': 'Invalid request'}, status=400)

@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



