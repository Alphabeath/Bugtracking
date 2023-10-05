from django.urls import path, include
from . import views

app_name = "home"
urlpatterns = [
    path('', views.home, name='principal'),
    path('login', views.login, name='login'),
    
    path('exit', views.exit, name='exit'),
    path('signup', views.signup, name='signup')

]
