from django.shortcuts import render
from .models import Payment
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class PaymentList(LoginRequiredMixin, ListView):
    model = Payment


class PaymentCreate(LoginRequiredMixin, CreateView):
    model = Payment
    fields = '__all__'
    template_name = 'payment/payment_create.html'
    success_url = '/payment'


class PaymentUpdate(LoginRequiredMixin, UpdateView):
    model = Payment
    fields = '__all__'
    template_name = 'payment/payment_update.html'
    success_url = '/payment'


class PaymentDelete(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'payment/payment_delete.html'
    success_url = '/payment'