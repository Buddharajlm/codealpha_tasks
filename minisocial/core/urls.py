from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("register/", views.register_page, name="register-page"),
    path("login/", views.login_page, name="login-page"),
    path("api/register/", views.api_register),
    path("api/login/", views.api_login),
    path("api/logout/", views.api_logout),
    path("api/me/", views.api_me),
    path("api/posts/", views.api_posts),
    path("api/posts/<int:post_id>/", views.api_post_delete),
    path("u/<str:username>/", views.profile_page, name="profile-page"),
    path("api/users/me/", views.api_update_me),
    path("api/users/search/", views.api_user_search),
    path("api/users/<str:username>/", views.api_profile),
    path("api/users/<str:username>/follow/", views.api_follow),
    path("api/posts/<int:post_id>/like/", views.api_like),
    path("api/posts/<int:post_id>/comments/", views.api_comments),
    path("api/comments/<int:comment_id>/", views.api_comment_delete),
]