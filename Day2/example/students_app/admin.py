from django.contrib import admin
from .models import Students, Exchange_Student

# Register your models here.
admin.site.register([Students, Exchange_Student])