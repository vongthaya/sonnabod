from django.urls import path
from . import views


urlpatterns = [
    path('', views.PaymentList.as_view(), name='payment_list'),
    path('create', views.PaymentCreate.as_view(), name='payment_create'),
    path('<int:pk>/update', views.PaymentUpdate.as_view(), name='payment_update'),
    path('<int:pk>/delete', views.PaymentDelete.as_view(), name='payment_delete'),
]