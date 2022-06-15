from django.urls import path

from app.example.views import ExampleView

urlpatterns = [
    path("", ExampleView.as_view()),
]
