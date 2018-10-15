from django.test import TestCase
from .models import *

# Create your tests here.

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id = 1, username='cheru')
        self.profile = Profile.objects.create(user = self.user,bio = 'my sample bio', contact='mycontact')

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_save_profile(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_get_all_profiles(self):
        self.profile.save()
        profile = Profile.get_all_profiles()
        self.assertTrue(len(profile) > 0)

    def test_find_profile(self):
        self.profile.save()
        profile = Profile.find_profile('cheru')
        self.assertTrue(len(profile) > 0)

class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id = 1, username='cheru')
        self.profile = Profile.objects.create(user = self.user,bio = 'my sample bio',contact='mycontact')

        self.post= Post.objects.create(name='sample_post',
                                       image='images/', description='desc',
                                       live_link='http://url' )


    def test_instance(self):
        self.assertTrue(isinstance(self.post,Post))

    def test_all_posts(self):
        self.post.save()
        post = Post.all_posts()
        self.assertTrue(len(post) > 0)

    def test_search_post(self):
        self.post.save()
        post = Post.search_by_name('sample_post')
        self.assertTrue(len(post) > 0)
#
# class PostTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(id = 1, username='cheru')
#
#         self.post= Post.objects.create(poster= self.user, name='sample post', image='images/', description='desc', live_link='http://url' )
#
#     def test_instance(self):
#         self.assertTrue(isinstance(self.post, Post))
#
#     def test_save_post(self):
#         self.assertTrue(isinstance(self.post,Post))
#
#     def test_all_posts(self):
#         self.post.save()
#         post = Post.all_posts()
#         self.assertTrue(len(post) > 0)