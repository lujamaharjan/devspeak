from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.forms import ValidationError
from .models import *
from .forms import SignupForm, LoginForm, BlogForm
# Create your views here.


class HomeView(TemplateView):
    template_name = "./blog_app/index.html"


class SignupView(CreateView):
    form_class = SignupForm
    model = User
    success_url = reverse_lazy('blog_app:home')
    template_name = "./blog_app/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        return redirect(self.success_url)

class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('blog_app:home')
    template_name = "./blog_app/login.html"

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            print("User not found")
            return redirect(reverse('blog_app:login') + '?error=Credientials not matched!')
        if next := self.request.GET.get('next'):
            return redirect(next)
        return redirect(self.success_url)


def logout_view(request):
    logout(request)
    return redirect('blog_app:home')


class ProfileView(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    template_name = 'blog_app/blogger/blogger_admin.html'

class MyBlogsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'blog_app/blogger/myblogs.html'

