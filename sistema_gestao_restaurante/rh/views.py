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
@permission_required('rh.view_employee')
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    employeers = EmployeeModel.objects.all()
    
    # Configurar a paginação com 10 itens por página
    paginator = Paginator(employeers, 10)
    page = request.GET.get('page')

    try:
        employeers = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um inteiro, mostrar a primeira página
        employeers = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostrar a última página
        employeers = paginator.page(paginator.num_pages)
    context = {
        'employeers': employeers,
        'total_employeers': employeers.paginator.count,
    }
    return render(request, "rh/employeers_list.html", context)

@login_required
@permission_required('rh.change_employee')
def create_employee(request):

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            # Lógica para lidar com dados do formulário aqui
            # ...
            form.save()
            messages.success(request, "Cadastrado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('rh:index'))

    else:
        form = EmployeeForm()

    context = {
        'exclude_menu_bar': True,
        'exclude_menu_bar1': True,
        'exclude_menu_bar3': True,
        'exclude_menu_bar4': True,
        'exclude_menu_bar5': True,
        'title': 'Cadastrar Funcionário',
        'form': form
    }
    return render(request, 'form.html',context)

@login_required
@permission_required('rh.delete_employee')
def confirm_delete(request, pk):
    employee = get_object_or_404(EmployeeModel, pk=pk)

    if request.method == 'POST':
        messages.success(request, f"Cliente {employee} eliminado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        if employee.user:
            employee.user.delete()
        employee.delete()
    else:
        messages.error(request, "Erro ao eliminar Cliente!", "text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500")
    return HttpResponseRedirect(reverse('rh:index'))

@login_required
@permission_required('rh.change_employee')
def employee_edit(request, pk):
    employee = get_object_or_404(EmployeeModel, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            if employee.user:
                user = employee.user
                user.groups.clear()
                user.groups.add(employee.position.group)
            messages.success(request, f"Cliente {employee} editado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('rh:index'))
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'form.html', {'form': form, 'employee': employee, 'title': 'Editar Cliente'})

@login_required
@permission_required('rh.change_position')
def position_edit(request, pk):
    if not request.user.has_perm('rh.change_position'):
        messages.error(request, "ERRO: Não possui permissão para criar ou editar cargos/funções!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        return HttpResponseRedirect(reverse('rh:list_position'))
    position = get_object_or_404(PositionModel, pk=pk)
    group = get_object_or_404(Group, pk=position.group.pk)

    if request.method == 'POST':
        form = PositionForm(request.POST, instance=group)
        if form.is_valid():
            position.description = form.cleaned_data['description']
            form.save()
            position.save()
            group.permissions.set(form.cleaned_data['permissions'])
            messages.success(request, f"Cargo {position} editado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('rh:list_positions'))
    else:
        form = PositionForm(instance=group)
        form['description'].initial = position.description

    return render(request, 'form.html', {'form': form, 'position': position, 'title': 'Editar Imposto'})

@login_required
@permission_required('rh.view_position')
def list_positions(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    if request.method == 'POST':
        if not request.user.has_perm('rh.change_position'):
            messages.error(request, "ERRO: Não possui permissão para criar ou editar impostos!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('rh:list_positions'))
        form = PositionForm(request.POST, request.FILES)
        if form.is_valid():
            # Lógica para lidar com dados do formulário aqui
            # ...
            group = form.save()
            position = PositionModel(
                group=group,
                description=form.cleaned_data['description'],
            )
            group.permissions.set(form.cleaned_data['permissions'])
            position.save()
            messages.success(request, "Cadastrado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
            return HttpResponseRedirect(reverse('rh:list_positions'))

    else:
        form = PositionForm()
    positions = PositionModel.objects.all()
    
    # Configurar a paginação com 10 itens por página
    paginator = Paginator(positions, 10)
    page = request.GET.get('page')

    try:
        positions = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um inteiro, mostrar a primeira página
        positions = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, mostrar a última página
        positions = paginator.page(paginator.num_pages)
    context = {
        'positions': positions,
        'total_positions': positions.paginator.count,
        'form':form
    }
    return render(request, "rh/positions_list.html", context)

@login_required
@permission_required('rh.delete_position')
def confirm_delete_position(request, pk):
    position = get_object_or_404(PositionModel, pk=pk)

    if request.method == 'POST':
        messages.success(request, f"Cargo/Função {position} eliminado com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        position.group.delete()
        position.delete()
    else:
        messages.error(request, "Erro ao eliminar Cargo/Função!", "text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500")
    return HttpResponseRedirect(reverse('rh:list_positions'))

@login_required
@permission_required('rh.change_employee')
def give_employee_access(request, pk):
    employee = get_object_or_404(EmployeeModel, pk=pk)

    # Verifique se o usuário já possui acesso
    if employee.user is not None:
        messages.warning(request, "Aviso: o presente funcionário já possui usuário atribuido!", "text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500")
        return HttpResponseRedirect(reverse('rh:index'))

    # Crie um novo usuário para o funcionário
    user = User.objects.create_user(username=employee.email, first_name=employee.name, password='senha_temporaria')
    # user.save()
    
    # Associe o novo usuário ao funcionário
    employee.user = user
    employee.save()
    user.groups.add(employee.position.group)
    messages.warning(request, "Acesso concedido com sucesso!", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
    return HttpResponseRedirect(reverse('rh:index'))

@login_required
@permission_required('rh.change_employee')
def remove_user(request, pk):
    employee = get_object_or_404(EmployeeModel, pk=pk)

    if employee.user:
        # user = employee.user
        employee.user.delete()
        employee.user = None
        employee.save()
        
        # Lógica adicional, se necessário, como excluir o usuário completamente.
        
        messages.warning(request, f"Usuário removido com sucesso para o funcionário {employee.name}", "text-green-500 bg-green-100 dark:text-green-100 dark:bg-green-500")
        return HttpResponse(f"Usuário removido com sucesso para o funcionário {employee.name}")
        return HttpResponseRedirect(reverse('rh:index'))
    else:
        messages.warning(request, f"O funcionário {employee.name} não tem um usuário associado.", "text-orange-500 bg-orange-100 dark:text-orange-100 dark:bg-orange-500")
        return HttpResponse(f"O funcionário {employee.name} não tem um usuário associado.")
        return HttpResponseRedirect(reverse('rh:index'))