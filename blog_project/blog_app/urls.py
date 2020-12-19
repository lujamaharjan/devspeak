from django.urls import path
from .views import *
app_name = 'blog_app'
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('myblogs/', MyBlogsView.as_view(), name="myblog")
]