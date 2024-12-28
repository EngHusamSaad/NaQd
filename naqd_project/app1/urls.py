from django.urls import path     
from . import views
urlpatterns = [
    path('', views.login),   
    path('register', views.register), 
    path('customers_table', views.customers_table),  
 
]
