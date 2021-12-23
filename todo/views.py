from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import createUserForm, orderForm
from .filters import orderFilter


# Create your views here.
# def list_todo(request):
#     context = {'todo_list':Todo.objects.all()}
#     return render(request,'todo/todo_list.html', context)

# def add_todo(request:HttpRequest):
#     todo = Todo(content = request.POST['content'])
#     todo.save()
#     return redirect('/todo/list/')

# def delete_todo(request, todo_id):
#     todo_deleted = Todo.objects.get(id=todo_id)
#     todo_deleted.delete()
#     return redirect('/todo/list/')

# def update_todo(request, todo_id):
#     todo_updated = Todo.objects.get(id=todo_id)
#     todo_updated.content = Todo(content = request.POST['content'])
#     todo_updated.save()

#     print(todo_updated)
#     return redirect('/todo/list/')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createUserForm
        if request.method == "POST":
            form = createUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'todo/register.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == "POST":
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username or Password incorrect')
		context = {}
		return render(request, 'todo/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def home(request):
    order = Order.objects.all()
    customer = Customer.objects.all()
    total_customers = customer.count()
    total_order = order.count()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    context = {'order': order, 'customer': customer, 'total_customers': total_customers,
               'total_order': total_order, 'delivered': delivered, 'pending': pending}

    return render(request, 'todo/dashboard.html', context)


def product(request):
    products = Products.objects.all()
    context = {'products': products}
    return render(request, 'todo/profile.html', context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    total_order = order.count()
    myFilter = orderFilter(request.GET, queryset=order)
    order = myFilter.qs
    context = {'customer': customer, 'order': order,
               'total_order': total_order, 'myFilter': myFilter}
    return render(request, 'todo/customer.html', context)


def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = orderForm(initial={'customer': customer})
    if request.method == "POST":
        form = orderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'todo/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = orderForm(instance=order)
    if request.method == "POST":
        form = orderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'todo/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'todo/delete.html', context)
