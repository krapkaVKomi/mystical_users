from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Schema(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', null=True, blank=True)
    modified = models.DateTimeField(auto_now_add=True, verbose_name='Modified')
    full_name = models.CharField(max_length=100, verbose_name='Full name', null=True, blank=True)
    job = models.CharField(max_length=100, verbose_name='Job', null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=254, null=True, blank=True)
    domain_name = models.URLField(max_length=200, verbose_name='Domain name', null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name='Phone number', null=True, blank=True)
    company_name = models.CharField(max_length=100, verbose_name='Company name', null=True, blank=True)
    text = models.TextField(verbose_name='Text', null=True, blank=True)
    integer = models.IntegerField(verbose_name='Integer', null=True, blank=True)
    date = models.DateField(verbose_name='Date', null=True, blank=True)

    def __str__(self):
        return self.title




