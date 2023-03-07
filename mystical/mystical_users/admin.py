from django.contrib import admin
from .models import *
# Register your models here.


class SchemaAdmin(admin.ModelAdmin):
    list_display = ('title', 'modified')


admin.site.register(Schema, SchemaAdmin)