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
def csv_data_view(request):
    if "file" in request.FILES:
        csv_file = request.FILES["file"]
        
        if csv_file.name.endswith(".csv"):
            
            df = pd.read_csv(csv_file)
            
            df["NewColumn"] = "Hello"
            
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="modified_data.csv"'
            
            df.to_csv(path_or_buf=response, index=False)
            
            return response
        
    return HttpResponse("Invalid request be", status=400)

@api_view(['POST'])
def email_submit(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



