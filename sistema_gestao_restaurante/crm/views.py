from django.shortcuts import render, get_object_or_404
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from django.conf import settings
from .forms import *
from .models import *



# Create your views here.
@login_required
@permission_required('crm.view_customer')
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
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
        'customers': customers,
        'total_customers': customers.paginator.count,
    }
    return render(request, "crm/customers_list.html", context)

@login_required
def create_customer(request):

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            # Lógica para lidar com dados do formulário aqui
            # ...
            produto = CustomerModel(
                name=form.cleaned_data['name'],
                nif=form.cleaned_data['nif'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
            )
            produto.save()
            messages.success(request, "Cadastrado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('crm:index'))

    else:
        form = CustomerForm()

    context = {
        'exclude_menu_bar': True,
        'exclude_menu_bar1': True,
        'exclude_menu_bar3': True,
        'exclude_menu_bar4': True,
        'exclude_menu_bar5': True,
        'title': 'Cadastrar Cliente',
        'form': form
    }
    return render(request, 'form.html',context)

@login_required
@permission_required('crm.delete_customer')
def confirm_delete(request, pk):
    customer = get_object_or_404(CustomerModel, pk=pk)

    if request.method == 'POST':
        messages.success(request, f"Cliente {customer} eliminado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        customer.delete()
    else:
        messages.error(request, "Erro ao eliminar Cliente!", "text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500")
    return HttpResponseRedirect(reverse('crm:index'))

@login_required
@permission_required('crm.change_customer')
def customer_edit(request, pk):
    customer = get_object_or_404(CustomerModel, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cliente {customer} editado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('crm:index'))
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'form.html', {'form': form, 'customer': customer, 'title': 'Editar Cliente'})