from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from django import forms

from .models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        fields = ['name','nif','phone_number','address']
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Nome do Cliente'
        }),
        label='Nome'
    )
    nif = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Número de Identificação Fiscal'
        }),
        label='NIF'
    )
    phone_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Nº de Telefone'
        }),
        label='Nº de Telefone'
    )
    address = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Endereço'
        }),
        label='Endereço'
    )
    
    
    # descricao = forms.CharField(
    #     max_length=50,
    #     widget=forms.Textarea(attrs={
    #         'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-textarea focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray',
    #         'rows': 3,
    #         'placeholder': 'Descreve o seu cliente...',
    #         'style': 'resize: none;',
    #     }),
    #     label='Descrição'
    # )

