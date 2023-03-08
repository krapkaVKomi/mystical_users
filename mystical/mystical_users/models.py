from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class File(models.Model):
    title = models.CharField(max_length=100, default='file', null=True)
    path = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.title


class Schema(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', null=True, blank=True)
    modified = models.DateTimeField(auto_now_add=True, verbose_name='Modified')
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Column(models.Model):
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=20)
    order = models.IntegerField()
    start = models.IntegerField(blank=True, null=True)
    end = models.IntegerField(blank=True, null=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, blank=True)


