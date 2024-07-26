# serializers.py
from rest_framework import serializers
from uploadreports.models import Reports

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ['id', 'file', 'uploaded_at', 'description', 'summary']