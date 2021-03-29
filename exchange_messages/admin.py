from django.contrib import admin

# Register your models here.
from .models import ExchangeMessage, Discussion

admin.site.register(ExchangeMessage)

admin.site.register(Discussion)
