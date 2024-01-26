from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'trainers'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('add_trainer/', views.add_trainer, name='add_trainer'),
    path('trainer_list/', views.trainer_list, name='trainer_list'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
