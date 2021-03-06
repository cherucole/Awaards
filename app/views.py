from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework import status
from .permissions import *
from .serializer import *
from rest_framework import status
from .permissions import IsAdminOrReadOnly


import datetime as dt
from django.http import HttpResponse,Http404,HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from .email import *

# Create your views here.

# @login_required(login_url='/accounts/login/')
def homepage(request):
    posts = Post.all_posts()
    profile = Profile.get_all_profiles()
    ratings=Ratings.objects.all()
    current_user = request.user
    # if request.method == 'POST':
    #     form = RatingsForm(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.user = current_user
    #         comment.save()
    #     return redirect('homepage')
    #
    # else:
    #     form=RatingsForm
    # last = len(posts.ratings.all())
    context =  {
        # 'last':last,
        "profile": profile,
        # "form": form,
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
    return render(request, 'upload.html', {"form": form})

@login_required(login_url='/accounts/login/')
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
    return render(request, 'new_profile.html', {"form": form})


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
            post_ratings = Ratings.objects.filter(post_rated=post)
            post_design_ratings = [pr.design for pr in post_ratings]
            print (post_design_ratings)
            design_avg=0
            for value in post_design_ratings:
                design_avg += value
            print (design_avg/len(post_design_ratings))
            design_score= (design_avg/len(post_design_ratings))

            post_usability_ratings = [pr.usability for pr in post_ratings]
            print (post_usability_ratings)
            usability_avg=0
            for value in post_usability_ratings:
                usability_avg += value
            print (usability_avg/len(post_usability_ratings))
            usability_score= (usability_avg/len(post_usability_ratings))

            post_content_ratings = [pr.content for pr in post_ratings]
            print (post_content_ratings)
            content_avg = 0
            for value in post_content_ratings:
                content_avg += value
            print (content_avg / len(post_content_ratings))
            content_score = (content_avg / len(post_content_ratings))


            score =(design_score + usability_score + content_score)/3

            rating.score =score
            rating.save()

            score=rating.score
            print ("last score=" + str(score))

            return redirect('homepage')
    else:
        form = RatingsForm()
        return render(request,'index.html',{"user":current_user,"ratings_form":form})

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
    post = Post.objects.get(id=post_id)
    profile = Profile.get_all_profiles()
    ratings = Ratings.objects.all()
    current_user = request.user
    if request.method == 'POST':
        form = RatingsForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.save()
        return redirect('homepage')

    else:
        form = RatingsForm
    context = {
        "profile": profile,
        "form": form,
        "post": post,
        "ratings": ratings,
    }
    return render (request, 'post.html', {'post':post, 'post_id': post.id, "form": form})

class Postlist(APIView):
    def get(self, request, format=None):
        all_post = Post.objects.all()
        serializers = PostSerializer(all_post, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = PostSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (IsAdminOrReadOnly,)

class PostDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        post = self.get_post(pk)
        serializers = PostSerializer(post)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        post = self.get_post(pk)
        serializers = PostSerializer(post, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_post(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)