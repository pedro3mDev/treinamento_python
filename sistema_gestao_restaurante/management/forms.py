from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from django import forms

from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input', 'placeholder': 'Último nome'}),
            'email': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input', 'type': 'email', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input', 'placeholder': 'Palavra-passe'}),
            'password2': forms.PasswordInput(attrs={'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input', 'placeholder': 'Confirme a sua palavra-passe'}),
        }

class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Produto'
        }),
        label='Nome'
    )
    
    price = forms.DecimalField(
        min_value=500,
        max_value=999999,
        widget=forms.NumberInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Kz 1.000'
        }),
        label='Preço'
    )

    categoria = forms.ModelChoiceField(
        queryset=CategoryModel.objects.all(),
        widget=forms.Select(attrs={
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray'
        })
    )

    taxa = forms.ModelChoiceField(
        queryset=TaxModel.objects.all(),
        widget=forms.Select(attrs={
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray'
        })
    )

    # taxa = forms.ChoiceField(
    #     choices=[
    #         ('opcao1', 'Opção 1'),
    #         ('opcao2', 'Opção 2'),
    #         ('opcao3', 'Opção 3'),
    #         ('opcao4', 'Opção 4'),
    #     ],
    #     widget=forms.Select(attrs={
    #         'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray'
    #     })
    # )

    codigo = forms.IntegerField(
        min_value=100000000,
        max_value=999999999,
        widget=forms.NumberInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': '3523565752'
        })
    )

    arquivo = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'file-upload-default',
            'accept': 'image/*'
        })
    )


    descricao = forms.CharField(
        max_length=50,
        widget=forms.Textarea(attrs={
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-textarea focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray',
            'rows': 3,
            'placeholder': 'Descreve o seu Produto...',
            'style': 'resize: none;',
        }),
        label='Descrição'
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['name','description']

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Categoria'
        }),
        label='Nome'
    )
    
    description = forms.CharField(
        max_length=50,
        widget=forms.Textarea(attrs={
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-textarea focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray',
            'rows': 3,
            'placeholder': 'Descreve a categoria...',
            'style': 'resize: none;',
        }),
        label='Descrição'
    )

class TaxForm(forms.ModelForm):
    class Meta:
        model = TaxModel
        fields = ['name','description','percentage']

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Categoria'
        }),
        label='Nome'
    )

    percentage = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Taxa'
        }),
        label='Taxa'
    )
    
    description = forms.CharField(
        max_length=50,
        widget=forms.Textarea(attrs={
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-textarea focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray',
            'rows': 3,
            'placeholder': 'Descreve a categoria...',
            'style': 'resize: none;',
        }),
        label='Descrição'
    )

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethodModel
        fields = ['name','description']

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Metodo de Pagamento'
        }),
        label='Nome'
    )
    
    description = forms.CharField(
        max_length=150,
        widget=forms.Textarea(attrs={
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-textarea focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray',
            'rows': 3,
            'placeholder': 'Descreve o metodo de pagamento...',
            'style': 'resize: none;',
        }),
        label='Descrição'
    )
