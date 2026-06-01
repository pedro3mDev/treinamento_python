from django.urls import include, path

from . import views

management_patterns = (
    [
        path("", views.index, name="index"),
        path("sign-in/", views.sign_in, name="sign_in"),
        path("logout-user/", views.logout_user, name="logout_user"),
        path("cadastro_produtos.html", views.cadastro_produto, name='cadastro_produto'),
        path("modelo.html", views.modelo, name='modelo'),
        path("lista_produtos.html", views.lista_produtos, name='lista_produtos'),
        path("dashboard.html", views.dashboard, name='dashboard'),
        path("dashboard.html", views.dashboard, name='dashboard'),
        # path("create-category/", views.create_category, name='create_category'),
        path("list-categories/", views.list_categories, name='list_categories'),
        path('category/<str:pk>/delete/', views.confirm_delete_category, name='confirm_delete_category'),
        path('category/<str:pk>/edit/', views.category_edit, name='category_edit'),

        path("list-taxes/", views.list_taxes, name='list_taxes'),
        path('tax/<str:pk>/delete/', views.confirm_delete_tax, name='confirm_delete_tax'),
        path('tax/<str:pk>/edit/', views.tax_edit, name='tax_edit'),

        path("list-payments-methods/", views.list_payment_methods, name='list_payment_method'),
        path('payment_method/<str:pk>/delete/', views.confirm_delete_payment_method, name='confirm_delete_payment_method'),
        path('payment_method/<str:pk>/edit/', views.payment_method_edit, name='payment_method_edit'),

        path('login.html', views.login_page, name='login'),
        path('cadastro.html', views.cadastro_page, name='cadastro'),
        path('pagina_vazia.html', views.pagina_vazia, name='pagina_vazia'),
        path('esqueceu-a-senha.html', views.esqueceu_a_senha, name='esqueceu_a_senha'),
        path('403.html', views.error_403, name='403'),
        path('404.html', views.error_404, name='404'),
        path('500.html', views.error_500, name='500'),


        # path("event-detail/", views.event_detail, name="event_detail"),
        # path("contact-us/<str:pack>/", views.contact_us, name="contact_us"),
        # path("send-email/<str:pack>/", views.send_email, name="send_email"),
        # path("privacity/", views.privacity, name="privacity"),
        # path("terms/", views.terms, name="terms"),
        # path("sent/", views.sent, name="sent"),
    ],
    "management"
)

urlpatterns = [
    path("", include(management_patterns)),
]