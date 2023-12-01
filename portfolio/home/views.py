

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect

from home.prediction import Prediction
from .forms import StockPredictionForm, TransactionForm
from .models import Transaction, Holdings
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os



def dashboard_view(request):
    context = { 'holdings' : Holdings.objects.filter(user=request.user)}
    buyvaluemap = {}
    profitmap = {}
    holdinglist = context['holdings']
    with connection.cursor() as cursor:
        cursor.execute("select id from auth_user where username = %s",[str(request.user)])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        userid = result[0]['id']

    for i in holdinglist:
       stockname = str(i.stock_Name)
       with connection.cursor() as cursor:
        cursor.execute("select ltp from public.home_companyprice where \"stock_Name_id\" = (Select id from public.home_companyprofile where \"company_Name\" = %s)" , [stockname])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        ltp = result[0]['ltp']

       print (stockname)
       print(ltp)
       cost = 0
       currentPrice = 0
       with connection.cursor() as cursor:
           cursor.execute("select  quantity, \"purchase_Value\" from public.home_transaction where \"stock_Name_id\" = (Select id from public.home_companyprofile where \"company_Name\" = %s) and user_id = %s", [stockname, userid])
           columns = [col[0] for col in cursor.description]
           result = [dict(zip(columns, row)) for row in cursor.fetchall()]

           for element in range(len(result)):
            cost = cost + (result[element]['purchase_Value'] * result[element]['quantity'])
            currentPrice = currentPrice + (ltp * (result[element]['quantity']))
            
           #cost =  cost + 
           #cursor.execute("Select id from public.home_companyprofile where \"stock_Name\" = %s", [stockname])
       buyvaluemap[stockname] = cost
       profitmap[stockname] = currentPrice - cost
       
    context['buyvaluemap'] =  buyvaluemap
    context['profitmap'] = profitmap
    print (profitmap)

    return render(request, "home/dashboard.html",context)

def transaction_list(request): 
    transactions = Transaction.objects.filter(user=request.user)
    p = Paginator(transactions, 5) 

    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = { 'page_obj': page_obj }
    return render(request, "home/transactions.html",context)

def transaction_delete(request,id): 
    transaction = Transaction.objects.get(pk=id)
    transaction.delete()
    return redirect("/home/transaction/list")

def transaction_view(request, id=0):
   if request.method == "GET":
        if id==0:
            form = TransactionForm()
            
        else:
            transaction = Transaction.objects.get(pk=id)
            form = TransactionForm(instance=transaction)
        return render(request, "home/investment.html",{'form':form})
   else:
        
        if id == 0:
            form = TransactionForm(request.POST)
        else:
            transaction = Transaction.objects.get(pk=id)
            form = TransactionForm(request.POST, instance=transaction)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("/home/transaction/list")  
   

 

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


def stock_prediction(request):
   
   #
   
   actualvalue = []
   predictedvalue = []
   if request.method == "GET":
     form = StockPredictionForm()
     msg = ''
   else:
    form = StockPredictionForm(request.POST)
    if form.is_valid():
       imagefile = "static/assets/img/stock.jpeg"
       if os.path.isfile(imagefile):
           os.remove(imagefile)
           print('deleted the file')
       else:    
            print('cound not find file')
       prediction = Prediction()
       actualvalue,predictedvalue = prediction.predict(form.cleaned_data.get("stockname"))
       
       msg = 'Stock Prediction'
    else:    
        msg = 'Error in Form Validation'
    

   return render(request, "home/prediction.html",{"form": form, "msg": msg, "actual": actualvalue, "prediction":predictedvalue})  
   


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

