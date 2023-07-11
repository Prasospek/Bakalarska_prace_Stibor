from rest_framework import serializers
from taxes.models import Email

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = {"email", "message"}