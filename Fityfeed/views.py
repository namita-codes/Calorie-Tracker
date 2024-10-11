from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .filters import fooditemFilter
import requests
from datetime import date, timedelta

def home(request):
    return render(request, 'base.html')

@login_required(login_url='login')
@admin_only
def main(request):
    breakfast = Category.objects.filter(name='breakfast')[0].fooditem_set.all()[:5]
    lunch = Category.objects.filter(name='lunch')[0].fooditem_set.all()[:5]
    dinner = Category.objects.filter(name='dinner')[0].fooditem_set.all()[:5]
    snacks = Category.objects.filter(name='snacks')[0].fooditem_set.all()[:5]
    customers = Customer.objects.all()
    context = {
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snacks': snacks,
        'customers': customers,
    }
    return render(request, 'main.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def fooditem(request):
    breakfast = Category.objects.filter(name='breakfast')[0].fooditem_set.all()
    bcnt = breakfast.count()
    lunch = Category.objects.filter(name='lunch')[0].fooditem_set.all()
    lcnt = lunch.count()
    dinner = Category.objects.filter(name='dinner')[0].fooditem_set.all()
    dcnt = dinner.count()
    snacks = Category.objects.filter(name='snacks')[0].fooditem_set.all()
    scnt = snacks.count()
    context = {
        'breakfast': breakfast,
        'bcnt': bcnt,
        'lcnt': lcnt,
        'scnt': scnt,
        'dcnt': dcnt,
        'lunch': lunch,
        'dinner': dinner,
        'snacks': snacks,
    }
    return render(request, 'fooditem.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createfooditem(request):
    form = fooditemForm()
    if request.method == 'POST':
        form = fooditemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'createfooditem.html', context)

@unauthorized_user
def registerPage(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='user')
            user.groups.add(group)
            email = form.cleaned_data.get('email')
            Customer.objects.create(user=user, name=username, email=email)
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

@unauthorized_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')  # Redirect to main page
        else:
            messages.info(request, 'username or password is invalid')
    return render(request, 'login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

from datetime import date, timedelta

@login_required(login_url='login')
def userPage(request):
    user = request.user
    cust = user.customer
    fooditems = Fooditem.objects.all()
    myfilter = fooditemFilter(request.GET, queryset=fooditems)
    fooditems = myfilter.qs
    
    # Get date from GET parameters, default to today
    start_date = request.GET.get('start_date', date.today().isoformat())
    
    # Ensure date is in the correct format
    try:
        start_date = date.fromisoformat(start_date)
    except ValueError:
        start_date = date.today()
    
    # Filter user food items by date
    user_fooditems = UserFooditem.objects.filter(customer=cust, date_consumed__exact=start_date)
    
    total_calories = 0
    for user_fooditem in user_fooditems:
        total_calories += sum(fooditem.calorie for fooditem in user_fooditem.fooditem.all())
    
    calorie_left = 2000 - total_calories
    
    breakfast = user_fooditems.filter(meal_type='breakfast')
    lunch = user_fooditems.filter(meal_type='lunch')
    dinner = user_fooditems.filter(meal_type='dinner')
    snacks = user_fooditems.filter(meal_type='snacks')
    
    context = {
        'CalorieLeft': calorie_left,
        'totalCalories': total_calories,
        'cnt': user_fooditems.count(),
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snacks': snacks,
        'fooditem': fooditems,
        'myfilter': myfilter,
        'start_date': start_date,
    }
    return render(request, 'user.html', context)




def addFooditem(request):
    user = request.user
    cust = user.customer
    if request.method == "POST":
        form = UserFooditemForm(request.POST)
        if form.is_valid():
            user_fooditem = form.save(commit=False)
            user_fooditem.save()  # Save the object first
            user_fooditem.customer.set([cust])  # Use .set() to assign ManyToManyField
            form.save_m2m()  # Save many-to-many fields
            return redirect('userPage') 
    else:
        form = UserFooditemForm()
    context = {'form': form}
    return render(request, 'addUserFooditem.html', context)

def cali(request):
    api = None
    if request.method == 'POST':
        query = request.POST.get('query')
        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
        headers = {
            'X-Api-Key': 'J4GM9+IvPcPEU3vt5eS9YA==NBvKuVWyLQapw9GV'
        }
        try:
            api_request = requests.get(api_url + query, headers=headers)
            api_request.raise_for_status()  # Raise an error for bad status codes
            api = api_request.json()  # Parse JSON response
            print("API Response:", api)  # Debug print
        except requests.exceptions.RequestException as e:
            api = f"Oops! There was an error: {e}"
            print(e)
    
    return render(request, 'cali.html', {'api': api})

def bmi(request):
    if request.method == "POST":
        weight = float(request.POST['weight'])
        height = float(request.POST['height']) / 100  # convert cm to meters
        bmi_value = weight / (height * height)
        return render(request, 'bmi.html', {'bmi_value': bmi_value})
    return render(request, 'bmi.html')
