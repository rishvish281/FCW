from django.urls import path
from . import views
app_name = 'counter'
urlpatterns = [
    path('home', views.home, name='home'),
]
