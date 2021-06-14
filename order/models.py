from django.db import models
from menu.models import Menu, MenuItem
from table.models import Table
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from secrets import token_hex


class Order(models.Model):
    order_id = models.CharField(max_length=50, blank=True)
    table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def total(self):
        total = 0
        for detail in self.details(status=True):
            total += detail.amount()
        return total

    def __str__(self):
        return self.order_id

    def details(self, **filter):
        return self.orderdetail_set.filter(**filter)

   
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.BooleanField(default=True)

    def amount(self):
        return self.price * self.qty

    def calculate_price(self):
        qs = OrderDetail.objects.filter(id=self.id)
        qs.update(price=self.menu.price)

    def has_item(self):
        return len(self.get_items()) > 0

    def get_items(self):
        return self.orderdetailitem_set.all()

    def __str__(self):
        return self.menu.name


class OrderDetailItem(models.Model):
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.item.name


def generate_order_id(sender, instance, **kwargs):
    if not instance.order_id:
        instance.order_id = str(token_hex(4)).upper()


def change_table_status(sender, instance, **kwargs):
    if instance.status == False:
        Table.objects.filter(id=instance.table.id).update(status=False)
    else:
        Table.objects.filter(id=instance.table.id).update(status=True)


def after_save_orderdetail(sender, instance, **kwargs):
    instance.calculate_price()


post_save.connect(after_save_orderdetail, sender=OrderDetail)
post_save.connect(change_table_status, sender=Order)
pre_save.connect(generate_order_id, sender=Order)