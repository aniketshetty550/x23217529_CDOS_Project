from django.shortcuts import render
from django.views import View
# Create your views here.

class Home(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'home.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')
        
class Order(View):
    def get(self, request, *args, **kwargs):
         return render(request, 'about.html')