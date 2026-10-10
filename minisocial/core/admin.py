from django.contrib import admin
from .models import Profile, Post, Comment, Like, Follow

admin.site.register([Profile, Post, Comment, Like, Follow])