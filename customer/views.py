from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, OrderModel
from django.db.models import Q
# Create your views here.

class Home(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'home.html')
        
class Menu(View):
    def get(self,request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        
        context = {
            'menu_items' : menu_items
        }
        
        return render(request, 'menu.html' , context)
        
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
        
# class Lougout(View):
#     def get(self,request, *args, **kwargs):
#         return render(request, 'login.html')
        
class Contact(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'contact.html')

# class Login(View):
#     def get(self,request, *args, **kwargs):
#         return render(request, 'login.html')
        
# class Signup(View):
#     def get(self,request, *args, **kwargs):
#         return render(request, 'signup.html')

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
        
        
    