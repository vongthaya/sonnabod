from django.db import models
from category.models import Category


class Menu(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='images', default='menu.jpg')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def item_count(self):
        return len(self.menuitem_set.filter(menu_id=self.id))

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name