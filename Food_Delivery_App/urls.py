"""Food_Delivery_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path 
from customer.views import Home, About, Order, Contact, Menu, MenuSearch, Login, Signup, Adminlogin, AddMenu, Owner, Delete, Update
from django.conf.urls.static import static
from django.conf import settings
# from .views import Login, Signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view(), name='home'),  
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search', MenuSearch.as_view(), name='menu-search'),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('order/', Order.as_view(), name='order'),
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('addmenu/', AddMenu.as_view(), name='addmenu'),
    path('owner/', Owner.as_view(), name='owner'),
    path('adminlogin/', Adminlogin.as_view(), name='adminlogin'),
    path('deletedish/<str:pk>', Delete.as_view(), name="deletedish"),
    path('updatedish/', Update.as_view(), name="updatedish"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
