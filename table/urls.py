from django.urls import path
from . import views


urlpatterns = [
    path('', views.TableList.as_view(), name='table_list'),
    path('create', views.TableCreate.as_view(), name='table_create'),
    path('<int:pk>/update', views.TableUpdate.as_view(), name='table_update'),
    path('<int:pk>/delete', views.TableDelete.as_view(), name='table_delete'),
]