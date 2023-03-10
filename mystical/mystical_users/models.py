from django.db import models


class Schema(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', blank=True)
    modified = models.DateTimeField(auto_now_add=True, verbose_name='Modified')

    def __str__(self):
        return self.title


class File(models.Model):
    path = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)
    file = models.FileField(null=True, upload_to='file')
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.path


class Column(models.Model):
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=20)
    order = models.IntegerField()
    number = models.IntegerField(blank=True, null=True)
    start = models.IntegerField(blank=True, null=True)
    end = models.IntegerField(blank=True, null=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


