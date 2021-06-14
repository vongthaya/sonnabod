from django.db import models
from menu.models import Menu, MenuItem
from table.models import Table
from payment.models import Payment
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from secrets import token_hex
from discount.models import DiscountType
from order.models import Order


class Receipt(models.Model):
    no = models.CharField(max_length=50, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    old_receipt_id = models.IntegerField(null=True, blank=True)
    table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    discount_type = models.ForeignKey(DiscountType, null=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.CharField(
        max_length=10, 
        choices=[ ('new', 'ບິນໃໝ່'), ('old', 'ບິນເກົ່າ') ],
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.no

    def get_total_discount(self):
        discount = self.subtotal - self.total
        return discount

    def discount_by(self, value):
        return self.discount_type.short_name == value

    def calculate_sub_total(self):
        subtotal = 0
        for item in self.details():
            amount = item.price * item.qty
            subtotal += amount
        return subtotal
    
    def calculate_total(self):
        discount_amount = 0

        if self.discount_by('percent'):
            discount_amount = (self.discount * self.subtotal) / 100
        elif self.discount_by('cash'):
            discount_amount = self.discount
        
        total = self.subtotal - discount_amount
        return total

    def details(self, **filter):
        return self.receiptdetail_set.filter(**filter)

    def payments(self, **filter):
        return self.receiptpayment_set.filter(**filter)

    def get_discount(self):
        if self.discount_by('no-discount'):
            return 0
        elif self.discount_by('percent'):
            return '{:,}'.format(self.discount) + ' %'
        elif self.discount_by('cash'):
            return '{:,}'.format(self.discount) + ' ກີບ'


class ReceiptDetail(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.BooleanField(default=True)

    def amount(self):
        return self.price * self.qty

    def __str__(self):
        return self.menu.name


class ReceiptPayment(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.payment.name


def generate_receipt_no(sender, instance, **kwargs):
    if not instance.no:
        instance.no = str(token_hex(4)).upper()

pre_save.connect(generate_receipt_no, sender=Receipt)