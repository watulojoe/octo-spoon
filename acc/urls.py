from django.urls import path
from . import views

from django.contrib.auth import views as auth_view


urlpatterns = [
    path('', views.home_view, name="home"),

    # signup login and logout urls
    path("signup", views.signup_user, name="signup"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    
    # changing password
    # NOTE: the user must be logged in
    path('password_change/',
         auth_view.PasswordChangeView.as_view(template_name='change/change_password.html'),
         name='change_password'),
    path('password_change/done/',
         auth_view.PasswordChangeDoneView.as_view(template_name='change/password_change_done.html'),
         name='password_change_done'),

    
    # reseting password
    path("reset_password/",
          auth_view.PasswordResetView.as_view(template_name='reset/reset_password.html'),
            name='reset_password'),
    path("reset_password_sent/",
          auth_view.PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'),
            name='password_reset_done'),
    path("reset/<uidb64>/<token>/",
          auth_view.PasswordResetConfirmView.as_view(template_name='reset/password_reset_form.html'),
            name='password_reset_confirm'),
    path("reset_password_complete/",
          auth_view.PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'),
            name='password_reset_complete'),

]