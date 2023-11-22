from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from datetime import datetime

class YourTestCase(TestCase):
    def test_processCSV_sorting(self):
        # Your test setup code

        # Make a request to your view (modify this based on your actual URL)
        response = self.client.post('/your-process-csv-url/', {'files': your_files})

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the 'pdf_filename' and 'merged_rows' are present in the JSON response
        json_response = response.json()
        self.assertTrue('pdf_filename' in json_response)
        self.assertTrue('merged_rows' in json_response)

        # Check if the PDF file exists (you might need to adjust the path)
        pdf_filename = json_response['pdf_filename']
        self.assertTrue(os.path.exists(pdf_filename))

        # Additional checks for the sorting logic based on 'merged_rows'

        # Your test cleanup code

