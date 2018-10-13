from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import datetime as dt

# Create your models here.

class Profile(models.Model):
    avatar = models.ImageField(upload_to='images/', blank=True)
    bio = HTMLField()
    contact = HTMLField()
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
    live_link=models.URLField(blank=True)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    user_profile = models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts',blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def search_by_name(cls,search_term):
        posts = cls.objects.filter(name__icontains=search_term)
        return posts

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
    INPUT = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    design=models.IntegerField(choices=INPUT, default=0, blank=True)
    usability=models.IntegerField(choices=INPUT, blank=True)
    content=models.IntegerField(choices=INPUT, blank=True)
    score=models.IntegerField(default=0, blank=True)
    # poster = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
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

