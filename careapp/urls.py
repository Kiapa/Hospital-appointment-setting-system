from django.contrib import admin
from django.urls import path
from careapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('starter/', views.starter, name='starter'),
    path('appointment/', views.appointment_request, name='appointment_request'),
    path('contact/', views.contact_request, name='contact_request'),
    path('show/', views.show, name='show'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.edit, name = 'edit'),
    path('', views.register, name='register')
]
