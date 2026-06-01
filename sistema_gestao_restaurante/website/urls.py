from django.urls import include, path

from . import views

website_patterns = (
    [
        path("", views.index, name="index"),
    ],
    "website"
)

urlpatterns = [
    path("", include(website_patterns)),
]