from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
]
