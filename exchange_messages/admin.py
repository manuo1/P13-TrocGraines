from django.contrib import admin

# Register your models here.
from .models import Discussion, ExchangeMessage


""" add models to admin page """

admin.site.register(ExchangeMessage)

admin.site.register(Discussion)
