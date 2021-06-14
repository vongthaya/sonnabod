from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders'),
    path('create/table/<table_id>', views.order_create, name='order_create'),
    path('create/', views.order_create_action, name='order_create_action'),
    path('cancel/order-detail', views.cancel_order_detail, name='cancel_order_detail'),
    path('order-detail/update-qty', views.update_qty_order_detail, name='update_qty_order_detail'),
    path('<order_id>/', views.order_update, name='order_update'),
    path('<order_id>/detail/', views.order_detail, name='order_detail'),
    path('<order_id>/delete/', views.order_delete, name='order_delete'),
    path('print-receipt', views.print_receipt, name='print_receipt'),
]