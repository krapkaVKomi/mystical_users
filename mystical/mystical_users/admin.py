from django.contrib import admin
from .models import *
# Register your models here.


class SchemaAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job', 'email', 'domain_name',
                    'phone_number', 'company_name', 'text', 'integer', 'date')


admin.site.register(Schema, SchemaAdmin)