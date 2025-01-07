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
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText





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


      photo = request.FILES.get('photo') 

      Customer.objects.create(first_name=request.POST['first_name'],
                          second_name=request.POST['second_name'],
                          email=request.POST['email'],
                          identity=request.POST['identity'],
                          address=request.POST['address'],
                          mobile=request.POST['mobile'],

                          password = hash,
                          photo=photo,
                          )
      
      request.session ['first_name']=request.POST['first_name']
      return redirect('/home')
  return render(request, 'registration.html')


def main(request):
    return render(request,"main.html")


def about(request):
    return render(request,"about.html")


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


def debt_view(request):
    customer_id = request.GET.get('customer_id')
    try:
        debts = Debt.objects.filter(customer_id=customer_id,status_debt=False)
        
        debt_data = [
        {
            'id': debt.id,
            'amount_debt': debt.amount_debt,
            'notes': debt.notes,
        }
        for debt in debts
    ]

        return JsonResponse(debt_data, safe=False)
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return JsonResponse({'error': 'Failed to retrieve debts'}, status=500)
    
    

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


                # Check if the email is the special email
                if email == "naqd@gmail.com":
                    return redirect('/admin/')  # Redirect to the Django admin page
                

                return redirect('/home')  # Redirect to a home page or dashboard
            else:
                error_message = "Invalid password"
        else:
            error_message = "Invalid email address"
        
        return render(request, 'home.html', {'error_message': error_message})

    data = {
        "first_name": request.session.get('first_name', ''),
        "second_name": request.session.get('second_name', '')
    }
       
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
        debt_id = data.get('debt_id')

        try:
            customer = Customer.objects.get(id=customer_id)
            debt = Debt.objects.get(id=debt_id)
           
            if debt.amount_debt==float(payment_amount):
                payment = Paymnet.objects.create(
                    debt=debt,
                    amount_payment=payment_amount,
                    payment_type=payment_type,
                    
                )
                
                debt.status_debt=True
                debt.save()
                
                response = {'success': True}
            else:
                print("in if create")
                response = {'success': False, 'error': 'Payemnt Amount should Equal Debt Amount !!!'}   
            
        except Customer.DoesNotExist:
            response = {'success': False, 'error': 'Customer not found'}

        return JsonResponse(response)

def chart_data_1(request):
    debts = Debt.objects.values('customer__first_name', 'customer__second_name').annotate(total_debt=Sum('amount_debt'))
    labels = [f"{debt['customer__first_name']} {debt['customer__second_name']}" for debt in debts]
    values = [debt['total_debt'] for debt in debts]
    
    return JsonResponse({'labels': labels, 'values': values})


def chart_data_2(request):
    payments = Paymnet.objects.values('debt__customer__first_name', 'debt__customer__second_name').annotate(total_payments=Sum('amount_payment'))

    labels = [f"{payment['debt__customer__first_name']} {payment['debt__customer__second_name']}" for payment in payments]
    values = [payment['total_payments'] for payment in payments]

    return JsonResponse({'labels': labels, 'values': values})


def latest_customers(request):
    customers = Customer.objects.all().order_by('-created_at')[:5]
    customer_data = [
        {
            'id': customer.id,
            'name': f"{customer.first_name} {customer.second_name}",
            'mobile':customer.mobile,
            'created_at': customer.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for customer in customers
    ]
    return JsonResponse(customer_data, safe=False)

    
def delete_debt(request, pk):
    debt = get_object_or_404(Debt, pk=pk)
    if request.method == 'POST':
        debt.delete()
        return JsonResponse({'success': True})  # إرجاع استجابة JSON بعد الحذف
    return JsonResponse({'success': False}, status=400)
@csrf_exempt
def delete_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return JsonResponse({'message': 'Customer deleted successfully'}, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({'message': 'Customer not found'}, status=404)
    
@csrf_exempt
def update_customer(request, customer_id):
    if request.method == 'PUT':
        try:
            customer = Customer.objects.get(id=customer_id)
            data = json.loads(request.body)

            # تحديث الحقول بناءً على البيانات المدخلة
            customer.first_name = data.get('first_name', customer.first_name)
            customer.second_name = data.get('second_name', customer.second_name)
            customer.email = data.get('email', customer.email)
            customer.mobile = data.get('mobile', customer.mobile)

            customer.save()

            return JsonResponse({'message': 'Customer updated successfully'}, status=200)
        except Customer.DoesNotExist:
            return JsonResponse({'message': 'Customer not found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=400)
    
def edit_debt(request, debt_id):
    if request.method == 'POST':
        try:
            debt = Debt.objects.get(id=debt_id)
            data = json.loads(request.body)
            debt.amount_debt = data.get('amount_debt')
            debt.notes = data.get('notes')
            debt.save()
            return JsonResponse({'success': True})
        except Debt.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Debt not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@csrf_exempt
def update_customer(request, id):
    if request.method == 'PUT':
        try:
            # جلب العميل
            customer = Customer.objects.get(id=id)
            
            # قراءة البيانات المرسلة
            data = json.loads(request.body)
            print("Data received:", data)

            # تحديث الحقول
            customer.first_name = data.get('first_name', customer.first_name)
            customer.second_name = data.get('second_name', customer.second_name)
            customer.email = data.get('email', customer.email)
            customer.mobile = data.get('mobile', customer.mobile)
            customer.save()

            return JsonResponse({'message': 'Customer updated successfully!'})

        except Customer.DoesNotExist:
            print(f"Customer with ID {id} does not exist.")
            return JsonResponse({'error': 'Customer not found'}, status=404)

        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_customers(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        customers_data = [
            {
                'id': customer.id,
                'first_name': customer.first_name,
                'second_name': customer.second_name,
                'email': customer.email,
                'mobile': customer.mobile,
            }
            for customer in customers
        ]
        return JsonResponse(customers_data, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_customer(request, id):
    try:
        customer = Customer.objects.get(id=id)
        data = {
            'id': customer.id,
            'first_name': customer.first_name,
            'second_name': customer.second_name,
            'email': customer.email,
            'mobile': customer.mobile,
        }
        return JsonResponse(data)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    

@csrf_exempt  # تعطيل CSRF إذا كنت تستخدم JavaScript لإرسال الطلبات
def update_payment(request, id):
    if request.method == 'PUT':
        try:
            # الحصول على بيانات الطلب
            data = json.loads(request.body)
            payment = Payment.objects.get(id=id)

            # تحديث البيانات
            payment.payment_type = data.get('payment_type', payment.payment_type)
            payment.amount_payment = data.get('amount_payment', payment.amount_payment)
            payment.customer_name = data.get('customer_name', payment.customer_name)
            payment.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Payment updated successfully.',
                'payment': {
                    'id': payment.id,
                    'payment_type': payment.payment_type,
                    'amount_payment': payment.amount_payment,
                    'customer_name': payment.customer_name,
                    'created_at': payment.created_at,
                },
            })

        except Paymnet.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Payment not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



def send_reminder(request):
    if request.method == 'POST':
        try:
            debt_id = request.POST.get('debt_id')
            debt = get_object_or_404(Debt, id=debt_id)
            customer_email = debt.customer.email
            
            subject = 'Debt Notification'
            message = f"Dear {debt.customer.first_name} {debt.customer.second_name},\n\n" \
                      f"You have an outstanding debt of {debt.amount_debt}.\n" \
                      f"Please make sure to settle it as soon as possible.\n\n" \
                      f"Thank you for your attention!"

            send_mail(
                subject,
                message,
                'System@palestinebar.ps',
                [customer_email],
                fail_silently=False,
            )
            return JsonResponse({"message": "Email sent successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"message": f"Failed to send email: {str(e)}"}, status=500)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=400)


