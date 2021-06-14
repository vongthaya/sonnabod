# Generated by Django 2.2 on 2021-06-13 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discount', '0001_initial'),
        ('table', '0001_initial'),
        ('payment', '0001_initial'),
        ('menu', '0001_initial'),
        ('order', '0007_auto_20210613_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(blank=True, max_length=50)),
                ('old_receipt_id', models.IntegerField(blank=True, null=True)),
                ('subtotal', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('new', 'ບິນໃໝ່'), ('old', 'ບິນເກົ່າ')], default='new', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('discount_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='discount.DiscountType')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Order')),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='table.Table')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10)),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.Payment')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipt.Receipt')),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('status', models.BooleanField(default=True)),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.Menu')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipt.Receipt')),
            ],
        ),
    ]