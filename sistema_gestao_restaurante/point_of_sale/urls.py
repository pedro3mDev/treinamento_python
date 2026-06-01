from django.urls import include, path

from . import views

point_of_sale_patterns = (
    [
        path("", views.index, name="index"),
        # path("today-places/", views.today_places, name="today_places"),
        # path("today-events/", views.today_events, name="today_events"),
        # path("event-detail/", views.event_detail, name="event_detail"),
        # path("contact-us/<str:pack>/", views.contact_us, name="contact_us"),
        # path("send-email/<str:pack>/", views.send_email, name="send_email"),
        # path("privacity/", views.privacity, name="privacity"),
        # path("terms/", views.terms, name="terms"),
        # path("sent/", views.sent, name="sent"),
        path('criar-fatura/', views.create_invoice, name='create_invoice'),
        path('imprimir-fatura/<int:fatura_id>/', views.print_invoice, name='print_invoice'),
    ],
    "point_of_sale"
)

urlpatterns = [
    path("", include(point_of_sale_patterns)),
]