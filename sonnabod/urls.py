"""sonnabod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from menu import views as menu_views
from django.contrib.auth.views import LoginView
from authentication import views as auth_view


urlpatterns = [
    path('', include('home.urls')),
    path('api/v1/menu/', menu_views.get_all_menu, name='get_all_menu'),
    path('menu/', include('menu.urls')),
    path('category/', include('category.urls')),
    path('table/', include('table.urls')),
    path('order/', include('order.urls')),
    path('receipt/', include('receipt.urls')),
    path('report/', include('report.urls')),
    path('payment/', include('payment.urls')),
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_view.logout_view, name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)