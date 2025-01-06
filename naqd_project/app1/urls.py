from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),   
    path('register', views.register,name="register"), 
    path('main', views.main,name="main"),
    path('api/customers/', views.customers_list, name='customers-list'),
    path('api/debts/', views.debts_list, name='debts-list'),
    path('api/payments/', views.payments_api, name='payments_api'),
    
    
    
    path('select_customer/', views.select_customer, name='select_customer'),
    path('customers_view', views.customers_view, name='customers_view'),

    path('debt_view', views.debt_view, name='debt_view'),

    path('add_payment/', views.add_payment, name='add_payment'),

    path('login_view', views.login_view, name='login_view'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),

    
    path('chart-data-1/', views.chart_data_1, name='chart_data_1'),
    path('chart-data-2/', views.chart_data_2, name='chart_data_2'),
    # path('chart-data-3/', views.chart_data_3, name='chart_data_3'),
    # path('chart-data-4/', views.chart_data_4, name='chart_data_4'),
    path('latest-customers/', views.latest_customers, name='latest_customers'),  # نقطة النهاية لجلب آخر الزبائن

    path('api/customers/delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('api/customers/<int:id>/', views.get_customer, name='get_customer'),
    path('api/customers/', views.get_customers, name='get_customers'),
    path('api/customers/<int:id>/', views.update_customer, name='update_customer'),
    
    path('add_debts/', views.add_debts, name='add_debts'),
    path('delete_debt/<int:pk>/', views.delete_debt, name='delete_debt'),
    path('edit_debt/<int:debt_id>/', views.edit_debt, name='edit_debt'),
    



    path('api/payments/<int:id>/', views.update_payment, name='update_payment'),


]