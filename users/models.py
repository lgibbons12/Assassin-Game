from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class CustomUser(AbstractUser):
    is_dead = models.BooleanField(default=False)
    target_name = models.CharField(max_length=255, blank=True, null=True)
    