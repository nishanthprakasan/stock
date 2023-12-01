from django import forms
from .models import Transaction



class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ['stock_Name','transaction_Date','quantity','purchase_Value',]
        widgets = {
            'transaction_Date': forms.DateInput(attrs={'class': 'datepicker'}),
            
        }
        labels = {
            'stock_Name' : 'Stock Name'
        }
        
        def __int__(self, *args, **kwargs):
            super(TransactionForm,self).__init__(*args,**kwargs)
            self.fields['stock_Name'].empty_label = 'Select'

class StockPredictionForm(forms.Form):
    stockname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Stock Symbol",
                "class": "form-control"
            }
        ))
    
