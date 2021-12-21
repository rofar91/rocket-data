from django.urls import path

from . import views

urlpatterns = [
    path('', views.Employees.as_view()),
    path('level/<int:level>', views.Hierarchy.as_view()),
]
