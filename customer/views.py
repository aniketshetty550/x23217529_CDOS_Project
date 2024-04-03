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

# Create your views here.

class Home(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'home.html')

class Adminlogin(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'adminlogin.html')
  
# class Delete(View):
#     def get(self,request, *args, **kwargs):
#         if request.method == 'POST':
#             menu_item = get_object(MenuItem, id=menu_item)
#             menu_item.delete()
#         return redirect('owner.html')
#     def post(self,request, *args, **kwargs):
#         if request.method == 'POST':
#             menu_item = get_object(MenuItem, id=menu_item)
#             menu_item.delete()
#         return redirect('owner.html')
        
class Delete(View):
    def get(self, request, *args, **kwargs):
        menu_item_id = kwargs.get('menu_item_id')
        try:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
        except MenuItem.DoesNotExist:
            return redirect('owner') 
        menu_item.delete()
        return redirect('owner')  

        
        
class AddMenu(View):
    def get(self,request, *args, **kwargs):   
        if request.method == 'POST':
            form = MenuItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('owner')  # Redirect to the menu page after adding a new menu item
        else:
            form = MenuItemForm()
        
        return render(request, 'addmenu.html', {'form': form, 'categories': Category.objects.all()})
        
    def post(self,request, *args, **kwargs):   
        if request.method == 'POST':
            form = MenuItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('owner')  # Redirect to the menu page after adding a new menu item
        else:
            form = MenuItemForm()
        
        return render(request, 'addmenu.html', {'form': form, 'categories': Category.objects.all()})
        
        
    
        
class Menu(View):
    def get(self,request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        
        context = {
            'menu_items' : menu_items
        }
        
        return render(request, 'menu.html' , context)
        
class Owner(View):
    def get(self,request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        
        context = {
            'menu_items' : menu_items
        }
        
        return render(request, 'owner.html' , context) 
        
        
class MenuSearch(View):
    def get(self,request, *args, **kwargs):
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
    def get(self,request, *args, **kwargs):
        return render(request, 'login.html')
        
class Contact(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'contact.html')
        
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')
        
class Order(View):
    def get(self, request, *args, **kwargs):
        
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
    def get(self, request, *args, **kwargs):
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
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')
 
    def post(self, request, *args, **kwargs):
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

    

        
    