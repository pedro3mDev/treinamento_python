from django.shortcuts import render

# Create your views here.
from django.urls import include, path

from . import views

management_patterns = (
    [
        path("", views.index, name="index"),
        path("create-employee/", views.create_employee, name="create_employee"),
        path('<str:pk>/delete/', views.confirm_delete, name='employee_confirm_delete'),
        path('<str:pk>/edit/', views.employee_edit, name='employee_edit'),
        path('give_access/<str:pk>/', views.give_employee_access, name='give_employee_access'),
        path('remove_user/<str:pk>/', views.remove_user, name='remove_user'),

        path("list-positions/", views.list_positions, name='list_positions'),
        path('position/<str:pk>/delete/', views.confirm_delete_position, name='confirm_delete_position'),
        path('position/<str:pk>/edit/', views.position_edit, name='position_edit'),
    ],
    "rh"
)

urlpatterns = [
    path("", include(management_patterns)),
]