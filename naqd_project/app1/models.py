from django.db import models
from datetime import datetime
import re
from django import forms



class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='imgs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class CustomerManager (models.Manager):
    def basic_validate(self,postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['second_name']) < 2:
            errors["second_name"] = "last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="invalid email" 
        if not postData ['password']:
            errors ['password'] = "Enter password"
        else: 
            if len(postData['password']) < 4:
                errors["password"] = "Password should be at least 4 characters"
    
        
        return errors

class Customer(models.Model):
        photo=models.ImageField(upload_to='img/', null=True, blank=True)
        email=models.EmailField(max_length=254)
        password=models.TextField()
        first_name=models.CharField(max_length=50)
        second_name=models.CharField(max_length=50)
        identity=models.IntegerField()
        address=models.TextField()
        mobile=models.IntegerField()
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)
        objects = CustomerManager()


class Debt(models.Model):
    
    status_debt=models.BooleanField(default=False)
    notes=models.TextField()
    amount_debt=models.FloatField()
    customer=models.ForeignKey(Customer,related_name="debts", on_delete=models.CASCADE, null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Paymnet(models.Model):
    payment_type=models.TextField()
    amount_payment=models.FloatField()
    debt=models.ForeignKey(Debt,related_name="paymnets", on_delete=models.CASCADE, null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Cheque(models.Model):
    cheque_num=models.IntegerField()
    bank=models.TextField()
    write_date=models.DateTimeField()
    deposite_date=models.DateTimeField()
    amount_cheque=models.FloatField()
    status_cheque=models.BooleanField(default=False)
    payment=models.ForeignKey(Paymnet, related_name="cheques", on_delete=models.CASCADE, null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    

