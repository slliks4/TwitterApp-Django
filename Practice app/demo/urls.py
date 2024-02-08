from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list/', views.Profile_list, name='profile_list'),
    path('view_profile/<int:id>', views.View_profile, name='view_profile'),
    path('search_users/', views.Search_users, name='search_users'),
]
