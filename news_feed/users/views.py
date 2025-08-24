from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy("main:index")
    
    def form_valid(self, form):
        user = form.get_user()
        
        if user:
            auth.login(self.request, user)
            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
            return HttpResponseRedirect(self.success_url)

    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home - Авторизация'
        return context
    
class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")
    
    def form_valid(self, form):
        
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)
            messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)
    

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["title"] = 'Регистрация'
        return context


class UserProfileView(UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset = None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)
    

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["title"] = 'Профиль'
        return context
    

def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse("main:index"))