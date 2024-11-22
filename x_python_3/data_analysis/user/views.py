from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import CustomUser

class UserRegister(CreateView):
    model = CustomUser
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user:user-login')

    def form_valid(self, form):
        request = self.request
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data.get('password'))
        new_user.is_active = True
        new_user.save()
        data = form.cleaned_data
        user = authenticate(request, email=data['email'], password=data['password'])
        if user is not None:
            login(request, user)
            messages.success(request, "Акаунт створено!")
            return redirect("user:user-login")
        return super().form_valid(form)


class UserLogin(LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Ви успішно ввійшли.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Перевірте дані для входу.")
        return super().form_invalid(form)


class UserLogout(LoginRequiredMixin, LogoutView):
    next_page = 'analysis:index'


class UserProfile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user/profile.html"
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
