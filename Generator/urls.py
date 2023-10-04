from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup_view, name="Sign Up"),
    path('login/', views.login_view, name="login"),
    path('generate/', views.generate_password, name="generate_password"),
]