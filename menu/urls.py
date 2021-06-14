from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_all_menu, name='get_all_menu'),
    path('all/', views.MenuList.as_view(), name='menu_all'),
    path('create/', views.MenuCreate.as_view(), name='menu_create'),
    path('<int:menu_id>/items', views.menu_item_list, name='menu_item_list'),
    path('<int:menu_id>/items/create', views.menu_item_create, name='menu_item_create'),
    path('<int:menu_id>/items/<int:item_id>/update', views.menu_item_update, name='menu_item_update'),
    path('<int:menu_id>/items/<int:item_id>/delete', views.menu_item_delete, name='menu_item_delete'),
    path('<int:pk>/update', views.MenuUpdate.as_view(), name='menu_update'),
    path('<int:pk>/delete', views.MenuDelete.as_view(), name='menu_delete'),
]