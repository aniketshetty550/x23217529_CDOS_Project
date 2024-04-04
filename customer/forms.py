"""  It's used to define Django forms that are specific to the app """
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MenuItem


class CreateUserForm(UserCreationForm):
    """  It allows to access the admin page """
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        """ It gives access the admin """
        
class MenuItemForm(forms.ModelForm):
    """ It creates Menu Table at the backend """
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'image', 'price', 'category']
