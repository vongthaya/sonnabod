from django.shortcuts import render
from .models import Table
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView


class TableList(ListView):
    model = Table


class TableCreate(CreateView):
    model = Table
    fields = '__all__'
    template_name = 'table/table_create.html'
    success_url = '/table'


class TableUpdate(UpdateView):
    model = Table
    fields = '__all__'
    template_name = 'table/table_update.html'
    success_url = '/table'


class TableDelete(DeleteView):
    model = Table
    template_name = 'table/table_delete.html'
    success_url = '/table'