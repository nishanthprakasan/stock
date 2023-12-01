

from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.

class CompanyProfile(models.Model):
    stock_Name = models.CharField(max_length=50)
    company_Name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    market_cap = models.BigIntegerField()
    
    def __str__(self):
        return self.company_Name
    

class CompanyPrice(models.Model):
    stock_Name = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    ltp = models.DecimalField(max_digits=10, decimal_places=2)
    pc =  models.DecimalField(max_digits=10, decimal_places=2)



class Transaction(models.Model):

    transaction_Date = models.DateField()
    quantity = models.PositiveBigIntegerField()
    purchase_Value = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_Name = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    class Meta:
        ordering = ['id']

class Holdings(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    stock_Name = models.ForeignKey(CompanyProfile, on_delete=models.DO_NOTHING)
    quantity = models.BigIntegerField()
    ltp = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return  self.quantity * self.ltp
    @property
    def profit(self,value):
        return 0
    
    class Meta:
        managed = False
        db_table = 'home_holdingsview'


