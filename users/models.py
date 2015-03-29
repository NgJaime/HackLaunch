from django.db import models
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from s3 import upload_image
from django_resized import ResizedImageField


class Skill(models.Model):
    name = models.CharField(max_length=64)


class User(AbstractUser):
    minimalProfile = models.BooleanField(default=False)
    nonSocialAuth = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    skills = models.ManyToManyField(Skill)

    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to=upload_image, blank=True)
    thumbnail = models.URLField()

    slug = AutoSlugField(unique=True)

    location = models.CharField(max_length=128, blank=True, null=True)
    summary = models.CharField(max_length=256, blank=True, null=True)
