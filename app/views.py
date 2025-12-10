from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models.functions import Round
from .models import Category,Expense,Balance
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Sum
import csv
import json

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            uname = request.POST['uname']
            mail = request.POST['mail']
            pwd = request.POST['pwd']
            cpwd = request.POST['cpwd']

            if pwd != cpwd:
                messages.error(request, "Passwords do not match!")
                return redirect('signup')

            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already exist!")
                return redirect('signup')
            if User.objects.filter(email=mail).exists():
                messages.error(request,"Email already exist!")
                return redirect('signup')

            hashed_pwd = make_password(pwd)
            User.objects.create(username=uname, email=mail, password=hashed_pwd)
            messages.success(request,"Registered Successfully!")
            return redirect('signup')

        elif 'login' in request.POST:
            uname = request.POST['uname']
            pwd = request.POST['pwd']
            user = authenticate(username=uname, password=pwd)
            if user:
                login(request, user)  # Logs in the user and starts a session
                request.session['username'] = uname
                user_id=request.user.id
                print(user_id)
                return redirect('expense')  # Redirect to your expense page
            else:
                messages.error(request,"Invalid username or password!")
                return redirect('signup')
    return render(request, 'signup.html')

def expense(request):
    username = request.session.get('username', None)
    categories = Category.objects.filter(createdBy=request.user)

    if request.method == 'POST':
        if 'bal' in request.POST:
            amount = request.POST.get('bal')
            if amount:
                Balance.objects.update_or_create(
                    user=request.user,
                    defaults={'balance': amount}
                )

        elif 'add_expense' in request.POST:
            price = float(request.POST['price'])
            cat_id = request.POST['category']

            category = Category.objects.get(id=cat_id,createdBy=request.user)

            Expense.objects.create(category=category, price=price, user=request.user)

            return redirect('expense')

        elif 'delete_expense' in request.POST:
            Expense.objects.filter(user=request.user).delete()
            return redirect('expense')

        elif 'delete_one' in request.POST:
            item = Expense.objects.order_by("-id").first()  # Latest expense
            if item:
                item.delete()

    expenses = Expense.objects.filter(user=request.user)
    b=None
    try:
        b = Balance.objects.get(user=request.user)
        salary=b.balance if b else 0
    except Balance.DoesNotExist:
        salary=0

    total_expense = round(sum(float(expense.price) for expense in expenses),2)

    remaining_balance = round(salary- total_expense,2) if salary else 0

    # Calculate category-wise totals
    category_sum = Expense.objects.filter(user=request.user).values('category__name').annotate(total=Round(Sum('price'),2))
    category_names = [data['category__name'] for data in category_sum]
    category_totals = [data['total'] for data in category_sum]

    # Serialize the data into JSON
    category_names_json = json.dumps(category_names)
    category_totals_json = json.dumps(category_totals)

    data_points = [
        {'label': 'Salary', 'value': salary},
        {'label': 'Expenses', 'value': total_expense},
        {'label': 'Remaining', 'value': remaining_balance},
    ]

    # Serialize data for the template
    line_chart_data = json.dumps(data_points)

    return render(request, 'expensetracker.html', {
        'username': username,
        'categories': categories,
        'expenses': expenses,
        'total_expense': total_expense,
        'category_wise_sum': category_sum,
        'bal': b,
        'remaining': remaining_balance,
        'category_names_json': category_names_json,  # Pass serialized data
        'category_totals_json': category_totals_json,  # Pass serialized data
        'line_chart_data': line_chart_data, 
    })



def export_expenses_to_csv(request):
     
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    
    writer = csv.writer(response)
    writer.writerow(['Category', 'Price','Created_At'])  

   
    expenses = Expense.objects.filter(user=request.user)

    for expense in expenses:
        writer.writerow([expense.category.name, expense.price, expense.created_at])  

    return response

def logout_user(request):
    if request.user.is_authenticated: 
        Balance.objects.filter(user=request.user).delete()
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('signup')

def addc(request):
    if request.method == 'POST':
        name = request.POST.get('category')
        if name:
            # Check if the category already exists
            if not Category.objects.filter(name=name,createdBy=request.user).exists():
                Category.objects.create(name=name,createdBy=request.user)
                messages.success(request, "Category Added Successfully! ✅")
            else:
                messages.warning(request, "Category already exists! ❗")
    return redirect('expense')