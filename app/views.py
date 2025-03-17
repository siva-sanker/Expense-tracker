from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Sum
from .models import Category,Expense

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
        if 'add_expense' in request.POST:
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

    total_expense=sum(float(expense.price) for expense in expenses)

    category_sum=(Expense.objects.filter(user=request.user).values('category__name').annotate(total=Sum('price')))

    return render(request,'expensetracker.html',{
        'username':username,
        'categories':categories,
        'expenses':expenses,
        'total_expense':total_expense,
        'category_wise_sum':category_sum})

def logout_user(request):
    logout(request)
    return HttpResponse('''
        <script>
            alert("You have successfully logged out.");
            window.location.href = "/signup/";
        </script>
    ''')

def addc(request):
    if request.method=='POST':
        name=request.POST['category']
        c=Category(name=name)
        c.save()
        return HttpResponse('''
        <script>
            alert("Category Added Successfully!");
            window.location.href = "/expense/";
        </script>
    ''')
    return render(request,'addcategory.html')