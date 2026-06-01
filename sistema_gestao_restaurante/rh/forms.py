# forms.py
from django import forms
from django.contrib.auth.models import Group, Permission
from .models import PositionModel, EmployeeModel

class PositionForm(forms.ModelForm):
    # description = forms.CharField(widget=forms.Textarea, required=False)
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Cargo/Função'
        }),
        label='Nome'
    )
    
    description = forms.CharField(
        max_length=50,
        widget=forms.Textarea(attrs={
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-textarea focus:border-purple-400 focus:outline-none focus:shadow-outline-blue dark:focus:shadow-outline-gray',
            'rows': 3,
            'placeholder': 'Descreve o cargo/função...',
            'style': 'resize: none;',
        }),
        label='Descrição'
    )

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Permissões'
    )

    class Meta:
        model = Group
        fields = ['name','description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se estiver editando um grupo existente, inicialize as permissões selecionadas
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()
    
    def clean_permissions(self):
        # Remova as permissões que foram desmarcadas
        cleaned_permissions = self.cleaned_data.get('permissions', [])
        initial_permissions = (set(self.fields['permissions'].initial) if self.fields['permissions'].initial else set())
        removed_permissions = initial_permissions - set(cleaned_permissions)

        for permission in removed_permissions:
            self.instance.permissions.remove(permission)

        return cleaned_permissions


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        fields = ['name','salary','email','description','position']
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Nome do Funcionário'
        }),
        label='Nome'
    )
    salary = forms.DecimalField(
        min_value=0,
        max_value=10000000,
        widget=forms.NumberInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Informe o salário do funcionário'
        }),
        label='Salário'
    )
    email = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'E-mail'
        }),
        label='E-mail'
    )
    description = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Descrição'
        }),
        label='Descrição'
    )
    # status = forms.BooleanField(
    #     widget=forms.CheckboxInput(attrs={
    #         'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
    #         'placeholder': 'Estado'
    #     }),
    #     label='Estado'
    # )
    # position = forms.CharField(
    #     max_length=50,
    #     widget=forms.TextInput(attrs={
    #         'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
    #         'placeholder': 'Cargo/Função'
    #     }),
    #     label='Cargo'
    # )
    position = forms.ModelChoiceField(
        queryset=PositionModel.objects.all(),
        widget=forms.Select(attrs={
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray'
        }),
        label='Cargo'
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


