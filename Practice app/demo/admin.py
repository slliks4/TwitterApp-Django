from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import Group,User

class Profile_inline(admin.StackedInline):
    model = Profile

class user_model(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [Profile_inline]

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User,user_model)
