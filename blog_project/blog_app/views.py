from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, View, UpdateView, DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.forms import ValidationError
from .models import *
from .forms import SignupForm, LoginForm, BlogForm, CommentForm
# Create your views here.


class HomeView(TemplateView):
    template_name = "./blog_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_blogs'] = Blog.objects.all().order_by("-id")[:4]
        return context
    


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

@login_required
def logout_view(request):
    logout(request)
    return redirect('blog_app:home')


class ProfileView(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    template_name = 'blog_app/blogger/blogger_admin.html'


class MyBlogsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'blog_app/blogger/myblogs.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'blog_app/blogger/create_blog.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog_app:myblogs')

    def form_valid(self, form):
        form.instance.blogger = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'

    template_name = 'blog_app/blogger/update_blog.html'
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('blog_app:myblogs')



class BlogDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Blog
    success_url = reverse_lazy('blog_app:myblogs')


@login_required
def update_bio(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.bio = request.POST.get('bio')
        user.save()
    return redirect('blog_app:profile')


@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.profile_picture = request.FILES.get('profile_picture')
        print(request.FILES.get('profile_picture'))
        user.save()
    return redirect('blog_app:profile')


class Blog_Detail_View(DetailView):
    template_name = 'blog_app/blog.html'
    model = Blog

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        blog = get_object_or_404(Blog,id=int(kwargs.get('pk')))
        blog.views = blog.views + 1
        blog.save()
        return handler(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = Like.objects.filter(blog=int(self.kwargs.get('pk'))).count()
        if Like.objects.filter(blog=int(self.kwargs.get('pk')), blogger=self.request.user.id).count() != 0:
            context['color'] = "red"
        else:
            context['color'] = "black"
        context['comments'] = Comment.objects.filter(blog=int(self.kwargs.get('pk')))
        return context
    




@login_required(login_url="/login/")
def like_view(request,id):
    if Like.objects.filter(blog=int(id), blogger=request.user.id).count() == 0:
        like = Like(blog=get_object_or_404(Blog,id=int(id)), blogger=request.user)
        like.save()
    else:
        like = Like.objects.get(blog=get_object_or_404(Blog,id=int(id)), blogger=request.user)
        like.delete()
    return redirect('blog_app:blog_detail', pk=int(id))


def create_comment_view(request, blog_id):
    if request.method == "POST":
        content = request.POST.get('comment')
        blogger = request.user
        blog = Blog.objects.get(id=int(blog_id))

        comment = Comment(content=content, blogger=blogger, blog=blog)
        comment.save()
    return redirect('blog_app:blog_detail', pk=int(blog_id))


@login_required(login_url="/login/")
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id = int(comment_id))
    blog_id = comment.blog.id
    comment.delete()
    return redirect('blog_app:blog_detail', pk=int(blog_id))


@login_required(login_url="/login/")
def edit_comment(request, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(id=int(comment_id))
        comment.content = request.POST.get('comment')
        blog_id = comment.blog.id
        comment.save()
    return redirect('blog_app:blog_detail', pk=blog_id)