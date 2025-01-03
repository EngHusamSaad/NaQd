from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt




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

def debt_list(request):
    debts = Debt.objects.all()  # جلب جميع الديون من قاعدة البيانات
    return render(request, 'debt_list.html', {'debts': debts})

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
