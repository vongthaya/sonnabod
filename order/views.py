from django.shortcuts import render, redirect, get_object_or_404
from table.models import Table as _Table
from menu.models import Menu
from payment.models import Payment
from order.models import Order, OrderDetail, OrderDetailItem
from category.models import Category
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import date
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from discount.models import DiscountType
from django.template.loader import render_to_string
import json


@login_required
def order_delete(req, order_id):
    order =get_object_or_404(Order, pk=order_id)
    order.delete()
    return redirect('/order')


@login_required
def print_receipt(req):
    order_id = req.GET['order_id']
    qs = Order.objects.filter(id=order_id)
    if qs.exists():
        order = qs.first()
        html = create_receipt_html(order)
        return JsonResponse({ 'status': 'ok', 'html': html })
    return JsonResponse({ 'status': 'fail'})


@login_required
def order_detail(req, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(req, 'order/order_detail.html', { 'order': order })


@login_required
@csrf_exempt
def order_update(req, order_id):
    if req.method == 'GET':
        order = get_object_or_404(Order, pk=order_id)
        data = {
            'order': order
        }
        return render(req, 'order/order_update.html', data)
    elif req.method == 'POST':
        order_details = json.loads(req.POST['order_detail'])

        # update order detail
        for od in order_details:
            qs = OrderDetail.objects.filter(id=od['id'])
            if qs.exists():
                order_detail = qs.first()
                order_detail.qty = int(od['qty'])
                status = od['status'] == 'True'
                order_detail.status = status
                order_detail.save()
        return JsonResponse({ 'status': 'ok' })


class OrderListView(LoginRequiredMixin, ListView):
    paginate_by = 50
    model = Order
    template_name = 'order/orders.html'
    context_object_name = 'orders'
    queryset = Order.objects.order_by('-id')


@login_required
@csrf_exempt
def update_qty_order_detail(req):
    order_detail_id = req.POST['id']
    qty = req.POST['qty']
    qs = OrderDetail.objects.filter(id=order_detail_id)
    if qs:
        od = qs.first()
        od.qty = qty
        od.save()
        return JsonResponse({ 'status': 'ok' })
    else:
        return JsonResponse({ 'status': 'fail' })


@login_required
@csrf_exempt
def cancel_order_detail(req):
    order_detail_id = req.POST['orderDetailId']
    order_id = req.POST['orderId']
    qs = OrderDetail.objects.filter(order_id=order_id, id=order_detail_id)
    if qs:
        od = qs.first()
        od.status = False
        od.save()
        return JsonResponse({ 'status': 'ok' })
    else:
        return JsonResponse({ 'status': 'fail' })


@login_required
def order_create(req, table_id):
    table = _Table.objects.get(id=table_id)
    menu_list = Menu.objects.all()
    categories = Category.objects.all()

    return render(req, 'order/create.html', {
        'table': table,
        'menu_list': menu_list,
        'categories': categories,
    })


@login_required
@csrf_exempt
def order_create_action(req):
    order_list = json.loads(req.POST['orderList'])
    table_id = req.POST['tableId']
    today = date.today().strftime('%d/%m/%Y')
    created_order_detail = []
    
    # create order
    order_qs = Order.objects.filter(table_id=table_id, status=False)
    if order_qs.exists():
        order = order_qs[0]
    else:
        order = Order.objects.create(table_id=table_id, user=req.user)

    # create order detail
    for elem in order_list:
        order_detail_qs = OrderDetail.objects.filter(order_id=order.id, menu_id=elem['id'])
        if order_detail_qs.exists():
            order_detail = order_detail_qs.first()
            order_detail.qty += int(elem['qty'])
            order_detail.save()
            # only use for print
            order_detail.qty = elem['qty']
        else:
            order_detail = OrderDetail.objects.create(
                order_id=order.id,
                menu_id=elem['id'],
                qty=elem['qty'],
            )

        # create order detail item
        for item in elem['items']:
            OrderDetailItem.objects.create(
                order_detail_id=order_detail.id,
                item_id=item['id']
            )

        created_order_detail.append(order_detail)

    order.order_details = created_order_detail
    order.created_at = today
    html = render_to_string('order/order_paper.html', { 'order': order })
    return JsonResponse({ 'status': 'ok', 'html': html }, safe=False)