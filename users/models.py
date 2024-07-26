from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.
class UserRole(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True)
    class Meta:
        db_table = 'user_roles'

class User(AbstractUser):
    email = models.EmailField(db_index=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True)
    #app_id = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    organisation_name = models.CharField(max_length=100, null=True)
    objects = UserManager()

    class Meta:
        db_table = 'users'