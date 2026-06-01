from django.shortcuts import render, get_object_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.db.models import Sum
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .decorators import *

from django.conf import settings
from .forms import *
from .models import *
from point_of_sale.models import *
from crm.models import *
from datetime import datetime


# Create your views here.
@login_required
def index(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    invoices = InvoiceModel.objects.all()
    # Configurar a paginação com 10 itens por página
    paginator = Paginator(invoices, 10)
    page = request.GET.get('page')

    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um inteiro, mostrar a primeira página
        invoices = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostrar a última página
        invoices = paginator.page(paginator.num_pages)
    context = {
        'invoices': invoices,
        'total_invoices': invoices.paginator.count,
        'qtd_products_sales': InvoiceLineModel.objects.values('product__name').annotate(total_quantity=Sum('quantity')),
        'total_customers':CustomerModel.objects.all().count(),
        'total_billing': InvoiceModel.objects.all().aggregate(Sum('total'))['total__sum'],
        'total_billing_year': InvoiceModel.objects.filter(created_at__year=current_year).aggregate(Sum('total'))['total__sum'],
        'total_billing_month': InvoiceModel.objects.filter(created_at__year=current_year, created_at__month=current_month).aggregate(Sum('total'))['total__sum']
    
    }
    print(context)
    return render(request, "management/dashboard.html", context)

@admin_only
def create_employer(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Conta criada com sucesso: {user.username}')
            return HttpResponseRedirect(reverse('accounts:user_login'))
    context = {'form':form}

    return render(request, "management/index.html", context)

@unautenticate_user
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username , password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('management:dashboard'))
        else:
            messages.info(request, 'Username ou palavra-passe incorreta')
            return render(request, 'management/login.html')
    context = {}
    return render(request, 'management/login.html',context)

@login_required
@permission_required('management.change_category')
def category_edit(request, pk):
    category = get_object_or_404(CategoryModel, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Categoria {category} editado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:list_categories'))
    else:
        form = CategoryForm(instance=category)

    return render(request, 'form.html', {'form': form, 'category': category, 'title': 'Editar Categoria'})

@login_required
@permission_required('management.view_category')
def list_categories(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            # Lógica para lidar com dados do formulário aqui
            # ...
            produto = CategoryModel(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                saved_by=request.user
            )
            produto.save()
            messages.success(request, "Cadastrado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:list_categories'))

    else:
        form = CategoryForm()
    categories = CategoryModel.objects.all()
    
    # Configurar a paginação com 10 itens por página
    paginator = Paginator(categories, 10)
    page = request.GET.get('page')

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um inteiro, mostrar a primeira página
        categories = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostrar a última página
        categories = paginator.page(paginator.num_pages)
    # messages.success(request, "messge here", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
    # messages.error(request, "messge here", "text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500")
    # messages.warning(request, "messge here", "text-orange-500 bg-orange-100 dark:text-orange-100 dark:bg-orange-500")
    # messages.info(request, "messge here", "text-teal-500 bg-teal-100 dark:text-teal-100 dark:bg-teal-500")
    context = {
        'categories': categories,
        'total_categories': categories.paginator.count,
        'form':form
    }
    return render(request, "management/categories_list.html", context)

@login_required
@permission_required('management.delete_category')
def confirm_delete_category(request, pk):
    if not request.user.has_perm('management.delete_category'):
        messages.error(request, "ERRO: Não possui permissão para eliminar categorias!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        return HttpResponseRedirect(reverse('management:list_categories'))
    category = get_object_or_404(CategoryModel, pk=pk)

    if request.method == 'POST':
        messages.success(request, f"Categoria {category} eliminada com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        category.delete()
    else:
        messages.error(request, "Erro ao eliminar Cliente!", "text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500")
    return HttpResponseRedirect(reverse('management:list_categories'))

@login_required
@permission_required('management.change_tax')
def tax_edit(request, pk):
    if not request.user.has_perm('management.change_tax'):
        messages.error(request, "ERRO: Não possui permissão para criar ou editar impostos!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        return HttpResponseRedirect(reverse('management:list_taxes'))
    tax = get_object_or_404(TaxModel, pk=pk)

    if request.method == 'POST':
        form = TaxForm(request.POST, instance=tax)
        if form.is_valid():
            form.save()
            messages.success(request, f"Imposto {tax} editado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:list_taxes'))
    else:
        form = TaxForm(instance=tax)

    return render(request, 'form.html', {'form': form, 'tax': tax, 'title': 'Editar Imposto'})

@login_required
@permission_required('management.view_tax')
def list_taxes(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    if request.method == 'POST':
        if not request.user.has_perm('management.change_tax'):
            messages.error(request, "ERRO: Não possui permissão para criar ou editar impostos!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:list_taxes'))
        form = TaxForm(request.POST, request.FILES)
        if form.is_valid():
            # Lógica para lidar com dados do formulário aqui
            # ...
            produto = TaxModel(
                name=form.cleaned_data['name'],
                percentage=form.cleaned_data['percentage'],
                description=form.cleaned_data['description'],
                saved_by=request.user
            )
            produto.save()
            messages.success(request, "Cadastrado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:list_taxes'))

    else:
        form = TaxForm()
    taxes = TaxModel.objects.all()
    # Configurar a paginação com 10 itens por página
    paginator = Paginator(taxes, 10)
    page = request.GET.get('page')

    try:
        taxes = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um inteiro, mostrar a primeira página
        taxes = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostrar a última página
        taxes = paginator.page(paginator.num_pages)
    context = {
        'taxes': taxes,
        'total_taxes': taxes.paginator.count,
        'form':form
    }
    return render(request, "management/taxes_list.html", context)

@login_required
@permission_required('management.delete_tax')
def confirm_delete_tax(request, pk):
    tax = get_object_or_404(TaxModel, pk=pk)

    if request.method == 'POST':
        messages.success(request, f"Imposto {tax} eliminado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        tax.delete()
    else:
        messages.error(request, "Erro ao eliminar Imposto!", "text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500")
    return HttpResponseRedirect(reverse('management:list_taxes'))

@login_required
@permission_required('management.change_payment_method')
def payment_method_edit(request, pk):
    if not request.user.has_perm('management.change_payment_method'):
        messages.error(request, "ERRO: Não possui permissão para criar ou editar metodo de pagamento!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        return HttpResponseRedirect(reverse('management:list_payment_method'))
    payment_method = get_object_or_404(PaymentMethodModel, pk=pk)

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=payment_method)
        if form.is_valid():
            form.save()
            messages.success(request, f"Metodo de Pagamento {payment_method} editado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:list_payment_method'))
    else:
        form = PaymentMethodForm(instance=payment_method)

    return render(request, 'form.html', {'form': form, 'payment_method': payment_method, 'title': 'Editar Imposto'})

@login_required
@permission_required('management.view_payment_method')
def list_payment_methods(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    if request.method == 'POST':
        if not request.user.has_perm('management.change_payment_method'):
            messages.error(request, "ERRO: Não possui permissão para criar ou editar impostos!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:list_payment_method'))
        form = PaymentMethodForm(request.POST, request.FILES)
        if form.is_valid():
            # Lógica para lidar com dados do formulário aqui
            # ...
            produto = PaymentMethodModel(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                saved_by=request.user
            )
            produto.save()
            messages.success(request, "Cadastrado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:list_payment_method'))

    else:
        form = PaymentMethodForm()
    payment_methods = PaymentMethodModel.objects.all()
    # Configurar a paginação com 10 itens por página
    paginator = Paginator(payment_methods, 10)
    page = request.GET.get('page')

    try:
        payment_methods = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um inteiro, mostrar a primeira página
        payment_methods = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostrar a última página
        payment_methods = paginator.page(paginator.num_pages)
    context = {
        'payment_methods': payment_methods,
        'total_payment_methods': payment_methods.paginator.count,
        'form':form
    }
    return render(request, "management/payment_methods_list.html", context)

@login_required
@permission_required('management.delete_payment_method')
def confirm_delete_payment_method(request, pk):
    payment_method = get_object_or_404(PaymentMethodModel, pk=pk)

    if request.method == 'POST':
        messages.success(request, f"Metodo de Pagamento {payment_method} eliminado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        payment_method.delete()
    else:
        messages.error(request, "Erro ao eliminar Metodo de Pagamento!", "text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500")
    return HttpResponseRedirect(reverse('management:list_payment_method'))

@login_required
def logout_user(request):
    logout(request)
    # return sign_in(request)
    return HttpResponseRedirect(reverse('website:index'))

@login_required
@permission_required('management.change_product')
def cadastro_produto(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Lógica para lidar com dados do formulário aqui
            # ...
            produto = ProductModel(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price'],
                category_id=form.cleaned_data['categoria'],
                tax_id=form.cleaned_data['taxa'],
                code=form.cleaned_data['codigo'],
                arquivo=form.cleaned_data['arquivo'],
                description=form.cleaned_data['descricao'],
                saved_by=request.user
            )
            produto.save()
            messages.success(request, "Cadastrado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('management:cadastro_produto'))

    else:
        form = ProductForm()

    context = {
        'exclude_menu_bar': True,
        'exclude_menu_bar1': True,
        'exclude_menu_bar3': True,
        'exclude_menu_bar4': True,
        'exclude_menu_bar5': True,
        'form': form
    }
    return render(request, 'management/cadastro_produtos.html',context)

@login_required
@permission_required('management.view_product')
def lista_produtos(request):
    products = ProductModel.objects.all()
    # Configurar a paginação com 10 itens por página
    paginator = Paginator(products, 10)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um inteiro, mostrar a primeira página
        products = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostrar a última página
        products = paginator.page(paginator.num_pages)

    context = {
        'exclude_menu_bar': True,
        'exclude_menu_bar1': True,
        'exclude_menu_bar2': True,
        'exclude_menu_bar4': True,
        'exclude_menu_bar5': True,
        'products': products
    }
    return render(request, 'management/lista_produtos.html',context)

def modelo(request):

    context = {
        
        'exclude_menu_bar': True,
        'exclude_menu_bar2': True,
        'exclude_menu_bar3': True,
        'exclude_menu_bar4': True,
        'exclude_menu_bar5': True,
    }
    return render(request, 'management/modelo.html',context)

@login_required
def dashboard(request):
    customers = CustomerModel.objects.all()
    # Configurar a paginação com 10 itens por página
    paginator = Paginator(customers, 10)
    page = request.GET.get('page')

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um inteiro, mostrar a primeira página
        customers = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostrar a última página
        customers = paginator.page(paginator.num_pages)

    context = {
        
        'exclude_menu_bar1': True,
        'exclude_menu_bar2': True,
        'exclude_menu_bar3': True,
        'exclude_menu_bar4': True,
        'exclude_menu_bar5': True,
        'total_customers':customers
    }
    return render(request, 'management/dashboard.html',context)

@login_required
def analise(request):

    context = {
        
        'exclude_menu_bar1': True,
        'exclude_menu_bar2': True,
        'exclude_menu_bar3': True,
        'exclude_menu_bar4': True,
        'exclude_menu_bar': True,
    }
    return render(request, 'management/analise.html',context)


def login_page(request):

    context = {}
    return render(request, 'management/login.html',context)

def cadastro_page(request):

    context = {}
    return render(request, 'management/cadastro.html',context)

def pagina_vazia(request):

    context = {
        
        'exclude_menu_bar': True,
        'exclude_menu_bar1': True,
        'exclude_menu_bar2': True,
        'exclude_menu_bar3': True,
        'exclude_menu_bar4': True,
    }
    return render(request, 'management/pagina_vazia.html',context)

def esqueceu_a_senha(request):
    context = {}
    return render(request, 'management/esqueceu-a-senha.html',context)

def error_403(request):
    context = {}
    return render(request, 'management/403.html',context)

def error_404(request):
    context = {}
    return render(request, 'management/404.html',context)

def error_500(request):
    context = {}
    return render(request, 'management/500.html',context)
