from django.db import models

class Stock(models.Model):
    code = models.CharField(max_length=100)
    exchange = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
