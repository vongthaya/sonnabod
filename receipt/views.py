from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ReceiptPayment, ReceiptDetail, Receipt
from django.template.loader import render_to_string
from django.http import JsonResponse
from order.models import Order
from payment.models import Payment
from discount.models import DiscountType
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
import json


def render_recreate_receipt_page(req, receipt):
    payments = receipt.payments()
    payments_len = len(payments)

    payment_type1 = payments[0].payment_id
    payment1 = payments[0].amount

    payment_type2 = ''
    payment2 = ''

    if payments_len == 2:
        payment_type2 = payments[1].payment_id
        payment2 = payments[1].amount

    payments = Payment.objects.all()
    discount_types = DiscountType.objects.all()
    details_json = [{ 'menuId': detail.menu_id , 'menu': detail.menu.name, 'qty': detail.qty, 'price': detail.price } 
                    for detail in receipt.details()]

    data = {
        'receipt': receipt,
        'payment_type1': payment_type1,
        'payment1': payment1,
        'payment_type2': payment_type2,
        'payment2': payment2,
        'payments': payments,
        'discount_types': discount_types,
        'details_json': details_json
    }

    return render(req, 'receipt/recreate_receipt.html', data)


def recreate_receipt_process(req, old_receipt):
    discount = float(req.POST['discount'])
    subtotal = float(req.POST['subTotal'])
    total = float(req.POST['total'])
    no = req.POST['no']
    discount_type = DiscountType.objects.get(short_name=req.POST['discountType'])
    payments = json.loads(req.POST['payments'])
    details = json.loads(req.POST['details'])

    # create receipt
    receipt = Receipt(
        order_id=old_receipt.order_id,
        old_receipt_id=old_receipt.id,
        table=old_receipt.table,
        subtotal=subtotal,
        total=total,
        discount=discount,
        discount_type=discount_type,
        user=req.user
    )
    receipt.save()

    # create receipt detail
    for detail in details:
        ReceiptDetail.objects.create(
            receipt=receipt,
            menu_id=detail['menuId'],
            qty=detail['qty'],
            price=detail['price']
        )

    # create receipt payment
    for payment in payments:
        ReceiptPayment.objects.create(
            receipt=receipt, 
            payment_id=payment['id'], 
            amount=payment['amount']
        )
    
    # update old receipt status to old
    Receipt.objects.filter(id=old_receipt.id).update(status='old')
    
    html = render_to_string('receipt/receipt_paper.html', { 'receipt': receipt })
    return JsonResponse({ 'status': 'ok', 'html': html })


class ReceiptListView(LoginRequiredMixin, ListView):
    paginate_by = 50
    model = Receipt
    template_name = 'receipt/receipt.html'
    context_object_name = 'receipts'
    queryset = Receipt.objects.order_by('-id')


@login_required
@csrf_exempt
def recreate_receipt(req, pk):
    is_get_method = req.method == 'GET'
    is_post_method = req.method == 'POST'
    receipt = get_object_or_404(Receipt, id=pk)

    if is_get_method:
        return render_recreate_receipt_page(req, receipt)
    elif is_post_method:
        return recreate_receipt_process(req, receipt)


@login_required
def receipt_detail(req, pk):
    receipt = get_object_or_404(Receipt, id=pk)
    return render(req, 'receipt/receipt_detail.html', { 'receipt': receipt })


@login_required
@csrf_exempt
def create_receipt(req, table_id):
    is_get_method = req.method == 'GET'
    is_post_method = req.method == 'POST'

    if is_get_method:
        return render_create_receipt_page(req, table_id)
    elif is_post_method:
        return checkout(req)


def checkout(req):
    order_id = req.POST['orderId']
    discount = float(req.POST['discount'])
    subtotal = float(req.POST['subTotal'])
    total = float(req.POST['total'])
    discount_type = DiscountType.objects.get(short_name=req.POST['discountType'])
    payments = json.loads(req.POST['payments'])

    # update order status to True
    qs = Order.objects.filter(id=order_id)
    if not qs.exists():
        return JsonResponse({ 'status': 'fail' })
    order = qs.first()
    order.status = True
    order.total = total
    order.save()

    # create receipt
    receipt = Receipt(
        order=order,
        table=order.table,
        subtotal=subtotal,
        total=total,
        discount=discount,
        discount_type=discount_type,
        user=req.user
    )
    receipt.save()

    # create receipt detail
    for detail in order.details(status=True):
        ReceiptDetail.objects.create(
            receipt=receipt,
            menu=detail.menu,
            qty=detail.qty,
            price=detail.menu.price
        )

    # create receipt payment
    for payment in payments:
        ReceiptPayment.objects.create(
            receipt=receipt, 
            payment_id=payment['id'], 
            amount=payment['amount']
        )
    
    html = render_to_string('receipt/receipt_paper.html', { 'receipt': receipt })
    return JsonResponse({ 'status': 'ok', 'html': html })


def render_create_receipt_page(req, table_id):
    order_qs = Order.objects.filter(table_id=table_id, status=False)

    if not order_qs:
        return redirect('/')

    order = order_qs.first()
    order_details = order.details(status=True)
    payments = Payment.objects.all()
    discount_types = DiscountType.objects.order_by('-id')

    return render(req, 'receipt/create.html', 
        {
            'order': order, 
            'order_details': order_details,
            'payments': payments,
            'discount_types': discount_types
        }
    )