from django.db import models
import uuid

# Create your models here.
class UploadedImage(models.Model):
    original_filename = models.CharField(max_length=255)
    file_uuid = models.UUIDField(null=True, blank=True)
    file_path = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    is_process = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class OcrResult(models.Model):
    image_id = models.IntegerField(null=True, blank=True)
    full_text = models.TextField()
    confidence = models.FloatField()
    processing_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'ocr_results'
