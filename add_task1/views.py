
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from show_task1.models import Post  # Assuming you have a model named 'Post'
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from . import forms

@login_required
def add_tasks(request):
    if request.method == 'POST': # if user click submit button
        task_form = forms.TaskForm(request.POST) 
        if task_form.is_valid():
            task_form.save()
            return redirect('add_tasks') 
    
    else: # user normally website e gele blank form pabe
        task_form = forms.TaskForm()
    return render(request, 'add_task.html', {'form' : task_form})

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
    else:
        register_form = forms.RegistrationForm()
    
    return render(request, 'register.html', {'form': register_form, 'type': 'Register'})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('profile')
            else:
                messages.warning(request, 'Login information incorrect')
                return redirect('user_login')
    else:
        form = AuthenticationForm()
    
    return render(request, 'register.html', {'form': form, 'type': 'Login'})

@login_required
def profile(request):
    data = Post.objects.filter(author=request.user)
    return render(request, 'profile.html', {'data': data})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Account updated successfully')
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': profile_form, 'type': 'Edit Profile'})


def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important for keeping the user logged in
            messages.success(request, 'Password updated successfully')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'pass_change.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')

class UserLoginView(LoginView):
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Login information incorrect')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
