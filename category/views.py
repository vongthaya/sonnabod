from django.shortcuts import render
from .models import Category
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CategoryList(LoginRequiredMixin, ListView):
    model = Category


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'
    template_name = 'category/category_create.html'
    success_url = '/category'


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'category/category_update.html'
    success_url = '/category'


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/category_delete.html'
    success_url = '/category'