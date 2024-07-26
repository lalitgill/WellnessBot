from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField


def get_default_user():
    User = get_user_model()
    return User.objects.get_or_create(username='default_user')[0].id

class Reports(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=get_default_user
    )
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    extracted_text = models.TextField()
    summary = models.TextField()
    text_vector = ArrayField(models.FloatField(), size=1536, null=True)

    def __str__(self):
        return f"{self.file.name} - {self.user.username}"