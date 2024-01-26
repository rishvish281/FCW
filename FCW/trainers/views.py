from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TrainerForm, EditTrainerForm
from .models import Trainer
from django.contrib.auth import authenticate, login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signing up
            login(request, user)
            return redirect('trainer_list')  # Redirect to the trainer list or another page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.contrib import messages
@login_required
def add_trainer(request):
    # Check if the user already has a trainer
    existing_trainer = Trainer.objects.filter(user=request.user).first()

    if existing_trainer:
        # Display a custom error message
        messages.error(request, "Only one trainer can be registered per account.")
        return redirect('trainers:trainer_list')  # Redirect to Trainer List or another page

    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            trainer = form.save(commit=False)
            trainer.user = request.user
            trainer.save()
            return redirect('trainers:trainer_list')  # Redirect to Trainer List or another page
    else:
        form = TrainerForm()

    return render(request, 'trainers/add_trainer.html', {'form': form})

@login_required
def edit_profile(request):
    trainer = request.user.trainer  # Assuming a OneToOneField from Trainer to User
    if request.method == 'POST':
        form = EditTrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('trainers:trainer_list')  # Redirect to Trainer List or another page
    else:
        form = EditTrainerForm(instance=trainer)
    return render(request, 'trainers/edit_profile.html', {'form': form})

def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers/trainer_list.html', {'trainers': trainers})
