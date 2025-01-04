from django.contrib import admin
from .models import Customer,Debt,Paymnet,Cheque

admin.site.register(Customer)
admin.site.register(Debt)
admin.site.register(Paymnet)
admin.site.register(Cheque)
