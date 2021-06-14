from django.urls import path
from . import views


urlpatterns = [
    path('day', views.report_day, name='report_day'),
    path('month', views.report_month, name='report_month'),
    path('year', views.report_year, name='report_year'),
]
