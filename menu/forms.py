from django import forms
from .models import MenuItem


class MenuItemForm(forms.Form):
    item = forms.CharField(label='ຊື່ຕົວເລືອກ')