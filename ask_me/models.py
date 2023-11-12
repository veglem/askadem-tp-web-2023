from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class ProfileManager(models.Manager):
#     def get_top_users(self):
#         return self.order_by('-likes')[:5]
#
#     def get_user_by_username(self, username):
#         try:
#             user = self.objects.get(user__username=username)
#         except ObjectDoesNotExist:
#             user = None
#
#         return user
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     likes = models.IntegerField(default=0)
#
#     objects = ProfileManager()
#
#     def __str__(self):
#         return f'{self.user.username}'
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=15)
#
#
# class Question(models.Model):
#     author = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     body = models.CharField(max_length=2000)
#     tags = models.ManyToManyField(Tag, blank=True, related_name='questions')
#     likes = models.IntegerField(default=0)
#     creation_date = models.DateTimeField(auto_now_add=True)
#
