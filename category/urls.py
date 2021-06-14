from django.urls import path
from . import views


urlpatterns = [
    path('', views.CategoryList.as_view(), name='category_list'),
    path('create', views.CategoryCreate.as_view(), name='category_create'),
    path('<int:pk>/update', views.CategoryUpdate.as_view(), name='category_update'),
    path('<int:pk>/delete', views.CategoryDelete.as_view(), name='category_delete'),
]