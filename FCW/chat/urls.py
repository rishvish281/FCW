from django.urls import path
from . import views
app_name = 'chat'
urlpatterns = [
    path('<str:room>/', views.roomy, name='roomy'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]