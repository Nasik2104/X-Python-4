from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Повтор Пароля')

    class Meta:
        model = CustomUser
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Паролі не збігаються')
        return data.get('password2')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            qs = CustomUser.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('User does not exists')
        return super(LoginForm, self).clean()