from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu, MenuItem
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import MenuItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def menu_item_list(req, menu_id):
    menuitem_list = MenuItem.objects.filter(menu_id=menu_id)
    return render(req, 'menu/menuitem_list.html', { 
            'menuitem_list': menuitem_list,
            'menu_id': menu_id
        })


@login_required
def menu_item_create(req, menu_id):
    form = MenuItemForm(req.POST or None)

    if form.is_valid():
        MenuItem.objects.create(menu_id=menu_id, name=form.cleaned_data['item'])
        return redirect(f'/menu/{menu_id}/items')

    return render(req, 'menu/menuitem_create.html', {
        'menu_id': menu_id,
        'form': form
    })


@login_required
def menu_item_delete(req, menu_id, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    item.delete()
    return redirect(f'/menu/{menu_id}/items')


@login_required
def menu_item_update(req, menu_id, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    form = MenuItemForm({'item': item.name})

    if req.method == 'POST':
        form = MenuItemForm(req.POST)
        if form.is_valid():
            MenuItem.objects.filter(id=item_id).update(name=form.cleaned_data['item'])
            return redirect(f'/menu/{menu_id}/items')

    return render(req, 'menu/menuitem_update.html', {
        'form': form
    })


class MenuList(LoginRequiredMixin, ListView):
    model = Menu


class MenuCreate(LoginRequiredMixin, CreateView):
    model = Menu
    fields = '__all__'
    template_name = 'menu/menu_create.html'
    success_url = '/menu/all'


class MenuUpdate(LoginRequiredMixin, UpdateView):
    model = Menu
    fields = '__all__'
    template_name = 'menu/menu_update.html'
    success_url = '/menu/all'


class MenuDelete(LoginRequiredMixin, DeleteView):
    model = Menu
    template_name = 'menu/menu_delete.html'
    success_url = '/menu/all'


@login_required
def get_all_menu(req):
    menu_list = Menu.objects.all()
    menu_json = []

    for menu in menu_list:
        menu_json.append({
            'id': menu.id,
            'name': menu.name,
            'price': menu.price,
            'image': menu.image.url,
            'category': {
                'id': menu.category.id,
                'name': menu.category.name,
            },
            'items': [{ 'id': item.id , 'name': item.name } for item in menu.menuitem_set.all()]
        })

    return JsonResponse(menu_json, safe=False)