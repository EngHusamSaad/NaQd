from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Customer





def login(request):
    return render(request,"login.html")


def register(request):
    return render(request,"registration.html")


def main(request):
    return render(request,"main.html")


def customers_list(request):
    customers = Customer.objects.all()
    data = [
        {
            'id': customer.id,
            'first_name': customer.first_name,
            'second_name': customer.second_name,
            'email': customer.email,
            'mobile': customer.mobile,
        }
        for customer in customers
    ]
    return JsonResponse(data, safe=False)

def debts_list(request):
    debts = Debt.objects.select_related('customer').all()
    data = [
        {
            'id': debt.id,
            'amount_debt': debt.amount_debt,
            'status_debt': debt.status_debt,
            'customer_name': f"{debt.customer.first_name} {debt.customer.second_name}",
        }
        for debt in debts
    ]
    return JsonResponse(data, safe=False)



def select_customer(request):
    pass
    # if request.method == 'POST':
    #     try:
    #         print(request.body)

    #         data = json.loads(request.body)
    #         item_id = data.get('item_id')
    #         customer_id = data.get('customer_id')
            
    #         customer_select=Customer.objects.get(id=customer_id)
    #         item=Item.objects.get(id=item_id)
            
    #         item.customer=customer_select
    #         item.isAvailble=False
    #         item.sold_date=datetime.now()
    #         item.save()
    #         return JsonResponse({'success': True, 'message': f'{item.name_item} was sold Successfully by {customer_select.first_name} {customer_select.second_name} ! '})
        
    #     except json.JSONDecodeError as e:
    #         return JsonResponse({
    #     "error": "Invalid JSON format",
    #     "message": str(e)
    # }, status=400)
    # else:
    #         return JsonResponse({"error": "Invalid request method"}, status=405)






def add_debts(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Received data:', data)  # للتشخيص
            
            customer_id = data.get('customer_id')
            debt_amount = data.get('debtamount')
            debt_description = data.get('debtDescription')

            if not customer_id or not debt_amount or not debt_description:
                return JsonResponse({'success': False, 'error': 'البيانات غير مكتملة'})

            if not Customer.objects.filter(id=customer_id).exists():
                return JsonResponse({'success': False, 'error': 'العميل غير موجود'})

            customer = Customer.objects.get(id=customer_id)

            Debt.objects.create(
                customer=customer,
                amount_debt=debt_amount,
                notes=debt_description
            )

            return JsonResponse({'success': True})
        except Exception as e:
            print('Error:', str(e))  # للتشخيص
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'طلب غير صالح'})



def customers_view(request):
    try:
        customers = Customer.objects.all().values('id', 'first_name', 'second_name')
        return JsonResponse(list(customers), safe=False)
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return JsonResponse({'error': 'Failed to retrieve customers'}, status=500)
    

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if email exists in the User model
        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            user = None
        
        if user is not None:
            # Authenticate the user using the email and password
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)  # Login the user
                return redirect('/main')  # Redirect to a home page or dashboard
            else:
                error_message = "Invalid password"
        else:
            error_message = "Invalid email address"
        
        return render(request, 'app1/login.html', {'error_message': error_message})
    
    return render(request, 'app1/login.html')