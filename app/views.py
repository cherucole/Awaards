from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework import status
from .permissions import *

import datetime as dt
from django.http import HttpResponse,Http404,HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from .email import *

# Create your views here.

@login_required(login_url='/accounts/login/')
def homepage(request):
    posts = Post.all_posts()
    profile = Profile.get_all_profiles()
    ratings=Ratings.objects.all()
    current_user = request.user
    if request.method == 'POST':
        form = RatingsForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.save()
        return redirect('homepage')

    else:
        form=RatingsForm
    context =  {
        "profile": profile,
        "form": form,
        "posts":posts ,
        "ratings":ratings,
    }
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login/')
def add_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_profile = current_user
            post.save()
        return redirect('homepage')

    else:
        form = UploadForm()
    return render(request, 'images/upload.html', {"form": form})


def profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_info = Profile.get_profile(profile.id)
    except:
        profile_info = Profile.filter_by_id(profile.id)
    posts = Post.get_profile_image(profile.id)
    title = f'@{profile.username}'
    return render(request, 'profile.html', {'title':title, 'profile':profile, 'profile_info':profile_info, 'posts':posts})


@login_required(login_url='/accounts/login/')
def add_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('homepage')

    else:
        form = NewProfileForm()
    return render(request, 'images/new_profile.html', {"form": form})


# @login_required(login_url='/accounts/login/')
# def search_results(request):
#     current_user = request.user
#     if 'username' in request.GET and request.GET["username"]:
#         search_term = request.GET.get("username")
#         profiles = Profile.find_profile(search_term)
#         message = search_term
#
#         return render(request,'images/search_profile.html',{"message":message,
#                                              "profiles":profiles,
#                                              "user":current_user,
#                                              "username":profiles})
#     else:
#         message = "You haven't searched for any user"
#         return render(request,'images/search_profile.html',{"message":message})



def like(request,operation,pk):
    image = get_object_or_404(Post,pk=pk)
    if operation == 'like':
        image.likes += 1
        image.save()
    elif operation =='unlike':
        image.likes -= 1
        image.save()
    return redirect('homepage')


@login_required(login_url='/accounts/login/')
def rate_post(request,pk):
    [design, usability, content]=[[0],[0],[0]]

    post = get_object_or_404(Post, pk=pk)
    current_user = request.user
    print (current_user)

    print (current_user.id)
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        [design, usability, content] = [[0], [0], [0]]
        # current_user = request.user

        if form.is_valid():
            form.save()
            rating = Ratings.objects.last()
            design=rating.design
            usability=rating.usability
            content=rating.content
            rating.post_rated = post
            # rating.poster = current_user
            rating.save()


            print (design, usability, content)

            # design_all=Ratings.objects.all()
            # for rating in design_all:
            #     print (rating.design)


# ********************************************
            post_ratings = Ratings.objects.filter(post_rated=post)
            post_design_ratings = [pr.design for pr in post_ratings]
            print (post_design_ratings)


            return redirect('homepage')
    else:
        form = RatingsForm()
        return render(request,'comment.html',{"user":current_user,"comment_form":form})

def search_results(request):

    if 'post' in request.GET and request.GET["post"]:
        search_term = request.GET.get("post")
        posts_results = Post.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"posts": posts_results})

    else:
        message = "Please enter a search term"
        return render(request, 'search.html',{"message":message})

def get_individual_post(request, post_id):

    try:
        post = Post.objects.get(id=post_id)
    except DoesNotExist:
        raise Http404()
    return render (request, 'post.html', {'post':post, 'post_id': post.id})



# def article(request, article_id):
#     try:
#         article = Article.objects.get(id=article_id)
#     except DoesNotExist:
#         raise Http404()
#     return render(request, 'all-news/article.html', {'article': article, 'article_id': article.id})