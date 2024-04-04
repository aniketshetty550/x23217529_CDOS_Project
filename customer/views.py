from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import MenuItem, Category, OrderModel
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .forms import CreateUserForm
from .models import Category, MenuItem
from .forms import MenuItemForm
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
# Create your views here.

class Home(View):
    """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
    def get(self,request, *args, **kwargs):
        """ Used to define view functions, which handle HTTP requests and return HTTP responses """
        return render(request, 'home.html')

class Adminlogin(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
        return render(request, 'adminlogin.html')
        
class Update(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            if request.method == 'POST':
                return redirect('owner.html')
        def post(self, request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            id=request.POST.get('id')
            menu_item = MenuItem.objects.get(id=id)
            menu_item.price = request.POST.get('price')
            menu_item.description = request.POST.get('description')
            menu_item.save()
            return redirect('owner')
        
        
class Delete(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self, request, pk, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            menu_item = kwargs.get('id=pk')
            try:
                menu_item = MenuItem.objects.get(id=pk)
            except MenuItem.DoesNotExist:
                return redirect('owner') 
            menu_item.delete()
            return HttpResponse(json.dumps({'status': 'menu id deleted!'}))

class Viewfood(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, pk, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            # menu_items = MenuItem.objects.all()
            menu_item = MenuItem.objects.get(id=pk)
            return render(request, 'viewfood.html', {'menu_item':menu_item})

        
class AddMenu(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            if request.method == 'POST':
                form = MenuItemForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    return redirect('owner') 
            else:
                form = MenuItemForm()
            
            return render(request, 'addmenu.html', {'form': form, 'categories': Category.objects.all()})
            
        def post(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            if request.method == 'POST':
                form = MenuItemForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    return redirect('owner') 
            else:
                form = MenuItemForm()
            
            return render(request, 'addmenu.html', {'form': form, 'categories': Category.objects.all()})
        
        
    
        
class Menu(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            menu_items = MenuItem.objects.all()
            
            context = {
                'menu_items' : menu_items
            }
            
            return render(request, 'menu.html' , context)
        
class Owner(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            menu_items = MenuItem.objects.all()
            
            context = {
                'menu_items' : menu_items
            }
            
            return render(request, 'owner.html', context) 
        
        
class MenuSearch(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            query = self.request.GET.get("q")
            
            menu_items = MenuItem.objects.filter( 
                Q(name__icontains=query) |
                Q(price__icontains=query) |
                Q(description__icontains=query)
    
            )
                
            context = {
                'menu_items': menu_items
                    
            }
                
            return render(request, 'menu.html', context)
        
class Lougout(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            return render(request, 'login.html')
        
class Contact(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self,request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            return render(request, 'contact.html')
        
class About(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self, request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            return render(request, 'about.html')
        
class Order(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self, request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            
            starter = MenuItem.objects.filter(category__name__contains='Starter')
            dessert = MenuItem.objects.filter(category__name__contains='Dessert')
            drinks = MenuItem.objects.filter(category__name__contains='Drink')
            main_course = MenuItem.objects.filter(category__name__contains='Main_Course')
            
            
            context = {
                'drinks': drinks,
                'dessert': dessert,
                'main_course': main_course,
                'starter':starter ,
                
            }
            
            return render(request, 'order.html' , context)
            
        def post(self, request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            
            name = request.POST.get('name')
            email = request.POST.get('email')
            street = request.POST.get('street')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip')
            
            order_items = {
                'items': []
            }
    
            items = request.POST.getlist('items[]')
    
            for item in items:
                menu_item = MenuItem.objects.get(pk__contains=int(item))
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.name,
                    'price': menu_item.price
                }
    
                order_items['items'].append(item_data)
    
                price = 0
                item_ids = []
    
            for item in order_items['items']:
                price += item['price']
                item_ids.append(item['id']) 
        
            order = OrderModel.objects.create(price=price, name=name, email=email, street=street,city=city, state=state, zip_code=zip_code)
            order.items.add(*item_ids)
    
            context = {
                'items': order_items['items'],
                'price': price
            }
    
            return render(request, 'order_confirmation.html', context)


class Login(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self, request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            if request.method =='POST':
                email = request.POST.get('email')
                password = request.POST.get('password')
                user = authenticate(request, username=email, password=password)
                if user is None:
                    messages.error(request, "User Credential Invalid.")
                    return render(request, 'login.html')
                else:
                    auth_login(request, user)
                    return redirect('order')  
            else:
                return render(request, 'login.html')
                
        def post(self, request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            print(request.method)
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is None:
                messages.error(request, "User Credential Invalid.")
                return render(request, 'login.html')
            else:
                auth_login(request, user)
                print(self.request.user.is_staff)
                if self.request.user.is_staff:
                    return redirect('owner')
                else:  
                    return redirect('order')

class Signup(View):
        """ File that includes views for rendering templates and handling HTTP requests for your Django app"""
        def get(self, request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            return render(request, 'signup.html')
     
        def post(self, request, *args, **kwargs):
            """ Used to define view functions, which handle HTTP requests and return HTTP responses """
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
     
            if password != password_confirm:
                messages.error(request, "Passwords do not match.")
                return redirect('signup')
     
            try:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
                messages.success(request, "Account created successfully.")
                return redirect('login')  
            except Exception as e:
                messages.error(request, str(e))
                return redirect('signup')

    

        
    