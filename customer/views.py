from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, OrderModel
# Create your views here.

class Home(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'home.html')
        
        
# class Lougout(View):
#     def get(self,request, *args, **kwargs):
#         return render(request, 'login.html')
        
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
    
        order = OrderModel.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'order_confirmation.html', context)
        
        
    