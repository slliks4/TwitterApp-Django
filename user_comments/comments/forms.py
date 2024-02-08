from django import forms
from .models import Posts,Profile
from django.contrib.auth.models import User 

class Addpost(forms.ModelForm):
    class Meta:
        model = Posts
        fields=('title','content')

class Edit_model(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class Edit_profile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','profile_pic')

class Create_profile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_pic']