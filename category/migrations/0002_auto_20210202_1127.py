# Generated by Django 2.2 on 2021-02-02 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.CharField(choices=[('ອາຫານ', 'ອາຫານ'), ('ເຄື່ອງດື່ມ', 'ເຄື່ອງດື່ມ')], max_length=100),
        ),
    ]
