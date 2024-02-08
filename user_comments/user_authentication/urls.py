from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',views.user_login, name='user_login'),
    path('signup/', views.user_signup, name='user_signup'),
    path('logout/', views.user_logout, name='user_logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),
]