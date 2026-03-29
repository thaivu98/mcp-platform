from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sessions/', views.session_list, name='session_list'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
]
