from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import RegisterForm, LoginForm, AddProductForm

# Create your views here.
def home(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'core/home.html', context)


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'core/signup.html', context)


def login_page(request):
    form = LoginForm

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
    context = {'form': form}
    return render(request, 'core/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('core:home')


@login_required
def new_item(request):
    form = AddProductForm()

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('core:home')
        else:
            print("Form errors:", form.errors)
    context = {
        'form': form,
        'title': 'Add New Item'
    }
    return render(request, 'core/form.html', context)


@login_required
def edit_items(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    form = AddProductForm(instance=product)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('core:home')

    context = {
        'form': form,
        'product': product,
        'title': 'Edit Items',
    }
    return render(request, 'core/form.html', context)


def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'core/detail.html', context)


def delete_view(request, pk):
     product = get_object_or_404(Product, pk=pk, created_by=request.user)
     if request.method == "POST":
        product.delete()
        return redirect('core:home')

     context = {
         'product': product
     }
     return render(request, 'core/delete.html', context)


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'core/search.html', context)


