from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Customer,Debt,Paymnet,Cheque
import bcrypt
from django.db.models import Sum





def login(request):
    return render(request,"login.html")

def register(request):
  if request.POST:
    errors = Customer.objects.basic_validate(request.POST)
    if len(errors)>0:
      for key,value in errors.items():
        messages.error(request,value)
      return redirect('/register')
    else:
      password=request.POST['password']
      hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
      Customer.objects.create(first_name=request.POST['first_name'],
                          second_name=request.POST['second_name'],
                          email=request.POST['email'],
                          identity=request.POST['identity'],
                          address=request.POST['address'],
                          mobile=request.POST['mobile'],
                          password = hash
                          )
      
      request.session ['first_name']=request.POST['first_name']
      return redirect('/home')
  return render(request, 'registration.html')


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

def payments_api(request):

    payments = Paymnet.objects.all().select_related('debt__customer')
    payments_data = [
        {
            'id': payment.id,
            'payment_type': payment.payment_type,
            'amount_payment': payment.amount_payment,
            'customer_name': f"{payment.debt.customer.first_name} {payment.debt.customer.second_name}",
            'customer_email': payment.debt.customer.email,
            'created_at': payment.created_at.date(),
            'total_debt' :payment.debt.amount_debt,
            'amount_remain' :payment.debt.amount_debt - payment.amount_payment
        }
        for payment in payments
    ]
    
    return JsonResponse(payments_data, safe=False)



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
            print('Received data:', data)  # 
            
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
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)  # Login the user
                return redirect('/home')  # Redirect to a home page or dashboard
            else:
                error_message = "Invalid password"
        else:
            error_message = "Invalid email address"
        
        return render(request, 'home.html', {'error_message': error_message})
    
    return render(request, 'home.html')

def home(request):
    return render(request,"home.html")

def logout_view(request):
        return redirect('/') 

def customer_summary(request):
    # Get all customers with their debts and cheques
    customers = Customer.objects.all()
    debts = Debt.objects.all()
    cheques = Cheque.objects.all()

    data = {
        'customers': customers,
        'debts': debts,
        'cheques': cheques,
    }

    return render(request, 'home.html', data)

def add_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_id = data.get('customer_id')
        payment_amount = data.get('payment_amount')
        payment_type = data.get('payment_type')

        try:
            customer = Customer.objects.get(id=customer_id)
            payment = Payment.objects.create(
                customer=customer,
                amount_payment=payment_amount,
                payment_type=payment_type,
            )
            response = {'success': True}
        except Customer.DoesNotExist:
            response = {'success': False, 'error': 'Customer not found'}

        return JsonResponse(response)


def chart_data(request):
    # جلب المبالغ الإجمالية لكل زبون
    debts = Debt.objects.values('customer__first_name', 'customer__second_name').annotate(total_debt=Sum('amount_debt'))

    # إنشاء البيانات المطلوبة
    labels = [f"{debt['customer__first_name']} {debt['customer__second_name']}" for debt in debts]
    values = [debt['total_debt'] for debt in debts]

    # إرجاع البيانات بتنسيق JSON
    return JsonResponse({'labels': labels, 'values': values})