from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.translation import gettext as _, activate, get_language
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, UserRegistrationForm


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Pollution Tracker')
        return context


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Welcome back, %(username)s!') % {'username': user.username})
                return redirect('dashboard:home')
            else:
                messages.error(request, _('Invalid username or password.'))
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Account created for %(username)s! You can now log in.') % {'username': username})
            return redirect('core:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, _('You have been logged out successfully.'))
    return redirect('core:home')


def set_language(request):
    """Set the language preference"""
    if request.method == 'GET':
        language = request.GET.get('language')
        if language in ['en', 'fa']:
            # Set the language in the session
            request.session['django_language'] = language
            # Activate the language for the current request
            activate(language)
            # Force session save
            request.session.save()
            messages.success(request, _('Language changed successfully.'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
