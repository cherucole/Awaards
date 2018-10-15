from django.test import TestCase
from .models import *

# Create your tests here.

class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(id = 1, username='cheru')
        self.profile = Profile.objects.create(user = self.user,bio = 'blow away')

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

class ImageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(id = 1, username='cheru')
        self.profile = Profile.objects.create(user = self.user,bio = 'my sample bio')

        self.image = Post.objects.create(user_profile = self.user,
                                          profile = self.profile,
                                          caption ='this is it!',
                                          likes = 0)

    def test_instance(self):
        self.assertTrue(isinstance(self.image,Post))

    def test_all_posts(self):
        self.image.save()
        image = Post.all_posts()
        self.assertTrue(len(image) > 0)

class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id = 1, username='cheru')

        self.comment= Comment.objects.create(poster= self.user, comment='new comment' )

    def test_instance(self):
        self.assertTrue(isinstance(self.comment, Comment))

    def test_save_comment(self):
        self.assertTrue(isinstance(self.comment,Comment))

    def test_get_all_comments(self):
        self.comment.save()
        comment = Comment.get_all_comments()
        self.assertTrue(len(comment) > 0)