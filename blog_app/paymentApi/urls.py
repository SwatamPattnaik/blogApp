from django.urls import path
from . import views

app_name = 'paymentApi'

urlpatterns = [
    path('users/', views.users, name='users'),
    path('add/', views.add, name='add'),
    path('iou/', views.iou, name='iou')
]
