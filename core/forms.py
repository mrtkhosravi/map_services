from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Username')
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password')
        })
    )


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email address')
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_('First Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First name')
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_('Last Name'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Last name')
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Username')})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm password')})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
