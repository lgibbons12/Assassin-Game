from django.contrib import admin
from .models import CustomUser, Player
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Player)