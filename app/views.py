from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Sum
from .models import Category,Expense,Balance
import csv

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
                return HttpResponse(f'''
                <script> alert("Passwords do not match!"); window.location.href = "{reverse('signup')}"; </script>
                ''')

            if User.objects.filter(username=uname).exists():
                return HttpResponse(f'''
                <script> alert("Username already exists!"); window.location.href = "{reverse('signup')}"; </script>
                ''')
            if User.objects.filter(email=mail).exists():
                return HttpResponse(f'''
                <script> alert("Email already exists!"); window.location.href = "{reverse('signup')}"; </script>
                ''')

            hashed_pwd = make_password(pwd)
            User.objects.create(username=uname, email=mail, password=hashed_pwd)
            return HttpResponse(f'''
            <script> alert("Registered successfully"); window.location.href = "{reverse('signup')}"; </script>
            ''')

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
                return HttpResponse(f'''
                <script> alert("Invalid username or password!"); window.location.href = "{reverse('signup')}"; </script>
                ''')
    return render(request, 'signup.html')


def expense(request):

    username=request.session.get('username',None)
    categories=Category.objects.all()

    if request.method=='POST':
        if 'bal' in request.POST:
            amount=request.POST.get('bal')
            if amount:
                Balance.objects.update_or_create(
                    user=request.user,
                    defaults={'balance': amount}
                )
        
        elif 'add_expense' in request.POST:
            price=float(request.POST['price'])
            cat_id=request.POST['category']
        
            category=Category.objects.get(id=cat_id)

            Expense.objects.create(category=category,price=price,user=request.user)

            return redirect('expense')
        
        elif 'delete_expense' in request.POST:
            Expense.objects.filter(user=request.user).delete()
            return redirect('expense')
        
        elif 'delete_one' in request.POST:
            item=Expense.objects.order_by("-id").first()    #?????
            if item:
                item.delete()
    
    expenses=Expense.objects.filter(user=request.user)

    try:
        b=Balance.objects.get(user=request.user)
    except Balance.DoesNotExist:
        b=None

    total_expense=sum(float(expense.price) for expense in expenses)

    remaining_balance = b.balance - total_expense if b else 0 

    category_sum=(Expense.objects.filter(user=request.user).values('category__name').annotate(total=Sum('price')))

    return render(request,'expensetracker.html',{
        'username':username,
        'categories':categories,
        'expenses':expenses,
        'total_expense':total_expense,
        'category_wise_sum':category_sum,
        'bal':b,
        'remaining':remaining_balance})


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
    return HttpResponse('''
        <script>
            alert("You have successfully logged out.");
            window.location.href = "/signup/";
        </script>
    ''')

def addc(request):
    if request.method == 'POST':
        name = request.POST.get('category')
        if name:
            # Check if the category already exists
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(name=name)
                return HttpResponse('''
                    <script>
                        alert("Category Added Successfully! ✅");
                        window.location.href = "/expense";
                    </script>
                ''')
            else:
                return HttpResponse('''
                    <script>
                        alert("Category already exists! ❗");
                        window.location.href = "/expense";
                    </script>
                ''')
    return redirect('expense')