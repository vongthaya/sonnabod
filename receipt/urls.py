from django.urls import path
from . import views


urlpatterns = [
    path('', views.ReceiptListView.as_view(), name='receipts'),
    path('<pk>', views.receipt_detail, name='receipt_detail'),
    path('recreate-receipt/<pk>', views.recreate_receipt, name='recreate_receipt'),
    path('create/<table_id>', views.create_receipt, name='create_receipt')
]