from django.shortcuts import render, redirect
from .models import Post, Comment
from django.urls import reverse
from .forms import PostForm

# Create your views here.


def home(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "home.html", context)


def details(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == "POST":
        comment = Comment.objects.create(
            content=request.POST["comment"], post=post, user=request.user
        )
        comment.save()
        return redirect(reverse("details", kwargs={"slug": post.slug}))
    context = {
        "post": post,
    }
    return render(request, "details.html", context)


def write(request):
    post_form = PostForm()
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse("details", kwargs={"slug": post.slug}))
    context = {"post_form": post_form}
    return render(request, "write.html", context)


def edit(request, slug):
    post = Post.objects.get(slug=slug)
    post_form = PostForm(instance=post)

    if request.user != post.author:
        return redirect("home")

    if request.method == "POST":
        if request.user == post.author:
            post_form = PostForm(request.POST, request.FILES, instance=post)
            if post_form.is_valid():
                post_form.save()
                return redirect(reverse("details", kwargs={"slug": post.slug}))
    context = {"post_form": post_form}
    return render(request, "edit.html", context)


def delete(request, slug):
    post = Post.objects.get(slug=slug)

    if request.user != post.author:
        return redirect("home")

    post.delete()
    return redirect("home")
