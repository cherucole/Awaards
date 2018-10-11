from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import datetime as dt

# Create your models here.

class Profile(models.Model):
    bio = HTMLField()
    avatar = models.ImageField(upload_to='images/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def save_profile(self):
        self.save()

    @classmethod
    def get_profile(cls, id):
        profile = Profile.objects.get(user=id)
        return profile

    @classmethod
    def get_all_profiles(cls):
        profile = Profile.objects.all()
        return profile

    @classmethod
    def find_profile(cls, search_term):
        profile = Profile.objects.filter(user__username__icontains=search_term)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user=id).first()
        return profile

    class Meta:
        ordering = ['user']


class Post(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/', blank=True)
    description = HTMLField(blank=True)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    user_profile = models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts',blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def one_post(cls, id):
        post=Post.objects.filter(id=id)
        return post


    @classmethod
    def all_posts(cls):
        posts = cls.objects.all()
        return posts


    @classmethod
    def get_user_posts(cls, profile_id):
        images=Post.objects.filter(profile_id=id)

    @classmethod
    def get_profile_image(cls, profile):
        posts = Post.objects.filter(user_profile__pk=profile)
        return posts

    @classmethod
    def get_post_by_id(cls,id):
        post = Post.objects.filter(id = Post.id)
        return post

    @classmethod
    def get_all_profiles(cls):
        profile = Profile.objects.all()
        return profile

class Ratings(models.Model):
    design=models.IntegerField(default=0)
    usability=models.IntegerField(default=0)
    content=models.IntegerField(default=0)
    score=models.IntegerField(default=0)
    poster = models.ForeignKey(User,on_delete=models.CASCADE, blank=True)
    post_rated = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='ratings',null=True)

    def save_comment(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Ratings.objects.filter(post_id=id).all()
        return ratings

#     @classmethod
#     def get_all_comments(cls):
#         comments = Comment.objects.all()
#         return comments
#
#     def __str__(self):
#         return self.comment

class Likes(models.Model):
	post = models.IntegerField()
	liker = models.CharField(max_length=20)


class Follow(models.Model):
    users = models.ManyToManyField(User, related_name='follow')
    current_user = models.ForeignKey(User, related_name='c_user', null=True)

    @classmethod
    def follow(cls, current_user, new):
        friends, created = cls.objects.get_or_create(current_user=current_user)
        friends.users.add(new)

    @classmethod
    def unfollow(cls, current_user, new):
        friends, created = cls.objects.get_or_create(current_user=current_user)
        friends.users.remove(new)