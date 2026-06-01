from django.shortcuts import render

# Create your views here.
from django.urls import include, path

from . import views

management_patterns = (
    [
        path("", views.index, name="index"),
        path("create-customer/", views.create_customer, name="create_customer"),
        path('<str:pk>/delete/', views.confirm_delete, name='customer_confirm_delete'),
        path('<str:pk>/edit/', views.customer_edit, name='customer_edit'),


        # path("event-detail/", views.event_detail, name="event_detail"),
        # path("contact-us/<str:pack>/", views.contact_us, name="contact_us"),
        # path("send-email/<str:pack>/", views.send_email, name="send_email"),
        # path("privacity/", views.privacity, name="privacity"),
        # path("terms/", views.terms, name="terms"),
        # path("sent/", views.sent, name="sent"),
    ],
    "crm"
)

urlpatterns = [
    path("", include(management_patterns)),
]