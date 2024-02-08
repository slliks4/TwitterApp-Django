from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('addcomment/<str:slug>', views.comment, name='comment'),
    path('add_notes/', views.add_notes, name='add_notes'),
    path('view_post/<str:slug>', views.view_post, name='view_post'),
    path('delete_post/<str:slug>', views.delete_post, name='delete_post'),
    path('like_post/<str:slug>', views.like_post, name='like_post'),
    path('profile/', views.User_profile,name="profile"),
    path('view_profile',views.view_profile, name='view_profile'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
    path('create_profile',views.create_profile, name='create_profile'),
    path('profile_page/<int:id>',views.profile_page, name='profile_page'),
]