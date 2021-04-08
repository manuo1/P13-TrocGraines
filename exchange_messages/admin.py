from django.contrib import admin

# Register your models here.
from .models import Discussion, ExchangeMessage

admin.site.register(ExchangeMessage)

admin.site.register(Discussion)
