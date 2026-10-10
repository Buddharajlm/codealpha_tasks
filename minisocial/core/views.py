import json
from django.db.models import Q
from .models import Comment, Follow, Like, Post, Profile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods, require_POST




def parse_json(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return {}


# ---------- Pages ----------

@ensure_csrf_cookie
def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "register.html")


@ensure_csrf_cookie
def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "login.html")


@ensure_csrf_cookie
def home_page(request):
    if not request.user.is_authenticated:
        return redirect("login-page")
    return render(request, "home.html", {"username": request.user.username})


# ---------- API ----------

@require_POST
def api_register(request):
    data = parse_json(request)
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if len(username) < 3:
        return JsonResponse({"error": "Username must be at least 3 characters."}, status=400)
    if username.lower() in {"me", "admin", "search"}:
        return JsonResponse({"error": "That username is reserved."}, status=400)
    if not email:
        return JsonResponse({"error": "Email is required."}, status=400)
    if User.objects.filter(username__iexact=username).exists():
        return JsonResponse({"error": "That username is taken."}, status=409)
    if User.objects.filter(email__iexact=email).exists():
        return JsonResponse({"error": "That email is already registered."}, status=409)

    try:
        validate_password(password)
    except ValidationError as e:
        return JsonResponse({"error": " ".join(e.messages)}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    Profile.objects.create(user=user)
    login(request, user)
    return JsonResponse({"username": user.username}, status=201)


@require_POST
def api_login(request):
    data = parse_json(request)
    user = authenticate(
        request,
        username=data.get("username", "").strip(),
        password=data.get("password", ""),
    )
    if user is None:
        return JsonResponse({"error": "Invalid username or password."}, status=401)
    login(request, user)
    return JsonResponse({"username": user.username})


@require_POST
def api_logout(request):
    logout(request)
    return JsonResponse({"ok": True})


@require_GET
def api_me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False}, status=401)
    return JsonResponse({"authenticated": True, "username": request.user.username})

# ---------- Posts API ----------

def serialize_post(post, user):
    return {
        "id": post.id,
        "author": post.author.username,
        "content": post.content,
        "created_at": post.created_at.isoformat(),
        "is_mine": post.author_id == user.id,
        "like_count": post.likes.count(),
        "liked_by_me": post.likes.filter(user=user).exists(),
        "comment_count": post.comments.count(),
    }


@require_http_methods(["GET", "POST"])
def api_posts(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)

    if request.method == "POST":
        content = parse_json(request).get("content", "").strip()
        if not content:
            return JsonResponse({"error": "Post can't be empty."}, status=400)
        if len(content) > 280:
            return JsonResponse({"error": "Post is too long (280 max)."}, status=400)
        post = Post.objects.create(author=request.user, content=content)
        return JsonResponse(serialize_post(post, request.user), status=201)

    scope = request.GET.get("scope", "all")
    posts = Post.objects.select_related("author")
    if scope == "following":
        followed_ids = request.user.following.values_list("following_id", flat=True)
        posts = posts.filter(Q(author=request.user) | Q(author_id__in=followed_ids))
    return JsonResponse({"posts": [serialize_post(p, request.user) for p in posts[:50]]})

@require_http_methods(["DELETE"])
def api_post_delete(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)
    try:
        post = Post.objects.get(id=post_id, author=request.user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    post.delete()
    return JsonResponse({"ok": True})

# ---------- Profiles ----------

@ensure_csrf_cookie
def profile_page(request, username):
    if not request.user.is_authenticated:
        return redirect("login-page")
    profile_user = get_object_or_404(User, username=username)
    return render(request, "profile.html", {
        "username": request.user.username,
        "profile_username": profile_user.username,
    })


@require_GET
def api_profile(request, username):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    profile, _ = Profile.objects.get_or_create(user=user)
    posts = user.posts.select_related("author")[:50]
    return JsonResponse({
        "username": user.username,
        "bio": profile.bio,
        "joined": user.date_joined.isoformat(),
        "is_me": user.id == request.user.id,
        "posts_count": user.posts.count(),
        "followers_count": user.followers.count(),
        "following_count": user.following.count(),
        "posts": [serialize_post(p, request.user) for p in posts],
    })


@require_http_methods(["PUT"])
def api_update_me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)
    bio = parse_json(request).get("bio", "").strip()
    if len(bio) > 160:
        return JsonResponse({"error": "Bio is too long (160 max)."}, status=400)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.bio = bio
    profile.save()
    return JsonResponse({"bio": profile.bio})

@require_POST
def api_follow(request, username):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)
    try:
        target = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    if target == request.user:
        return JsonResponse({"error": "You can't follow yourself."}, status=400)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
    return JsonResponse({
        "following": created,
        "followers_count": target.followers.count(),
    })

# ---------- Likes & Comments API ----------

@require_POST
def api_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # already liked, so this click means unlike
    return JsonResponse({"liked": created, "like_count": post.likes.count()})


def serialize_comment(comment, user):
    return {
        "id": comment.id,
        "author": comment.author.username,
        "content": comment.content,
        "created_at": comment.created_at.isoformat(),
        "is_mine": comment.author_id == user.id,
    }


@require_http_methods(["GET", "POST"])
def api_comments(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "POST":
        content = parse_json(request).get("content", "").strip()
        if not content:
            return JsonResponse({"error": "Comment can't be empty."}, status=400)
        if len(content) > 280:
            return JsonResponse({"error": "Comment is too long (280 max)."}, status=400)
        comment = Comment.objects.create(post=post, author=request.user, content=content)
        data = serialize_comment(comment, request.user)
        data["comment_count"] = post.comments.count()
        return JsonResponse(data, status=201)

    comments = post.comments.select_related("author")
    return JsonResponse({"comments": [serialize_comment(c, request.user) for c in comments]})


@require_http_methods(["DELETE"])
def api_comment_delete(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)
    try:
        comment = Comment.objects.get(id=comment_id, author=request.user)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found."}, status=404)
    post = comment.post
    comment.delete()
    return JsonResponse({"ok": True, "comment_count": post.comments.count()})

# ---------- User search ----------

@require_GET
def api_user_search(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required."}, status=401)
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"users": []})

    users = User.objects.filter(username__icontains=q).exclude(id=request.user.id)[:10]
    followed = set(request.user.following.values_list("following_id", flat=True))
    return JsonResponse({
        "users": [
            {"username": u.username, "is_following": u.id in followed}
            for u in users
        ]
    })