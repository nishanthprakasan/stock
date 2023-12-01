

from django.urls import path, re_path
from home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('transaction', views.transaction_view, name="transaction_insert"),
    path('transaction/<int:id>/', views.transaction_view, name="transaction_update"),
    path('transaction/list', views.transaction_list, name="transaction_list"),
    path('transaction/delete/<int:id>/', views.transaction_delete, name="transaction_delete"),
    path('prediction', views.stock_prediction, name="stock_prediction"),
    path('dashboard', views.dashboard_view, name="dashboard_view"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
