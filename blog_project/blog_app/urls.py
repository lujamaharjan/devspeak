from django.urls import path
from .views import *
app_name = 'blog_app'
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('myblogs/', MyBlogsView.as_view(), name="myblogs"),
    path('create_blog/', BlogCreateView.as_view(), name="create_blog"),
    path("update_blog/<int:pk>/", BlogUpdateView.as_view(), name="update_blog"),
    path("delete_blog/<int:pk>/", BlogDeleteView.as_view(), name="blog_delete"),
    path("update_bio/", update_bio, name="update_bio"),
    path("update_profile_picture/", update_profile_picture, name="update_profile_picture"),
    path("blog/<int:pk>/", Blog_Detail_View.as_view(), name="blog_detail"),
    path("blog_like/<int:id>/", like_view, name="blog_like"),
    path("create_comment_view/<int:blog_id>/", create_comment_view, name="create_comment_view"),
    path("delete_comment/<int:comment_id>/", delete_comment, name="delete_comment"),
    path("comment_edit/<int:comment_id>/", edit_comment, name="edit_comment")
]