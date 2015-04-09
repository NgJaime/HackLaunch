from django.db import models
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from s3 import upload_profile_image, upload_profile_thumbnail
from django_resized import ResizedImageField


class Skill(models.Model):
    name = models.CharField(max_length=64)


class MakerTypes(models.Model):
    name = models.CharField(max_length=64)


class User(AbstractUser):
    minimalProfile = models.BooleanField(default=False)
    nonSocialAuth = models.BooleanField(default=False)

    def getDateJoinedMonth(self):
        return self.date_joined.strftime("%B")

    def getDateJoinedDayMonthYear(self):
        return self.date_joined.strftime("%d/%m/%y")


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    skills = models.ManyToManyField(Skill)
    maker_type = models.ManyToManyField(MakerTypes)

    image = ResizedImageField(size=[230, 230], crop=['middle', 'center'], upload_to=upload_profile_image, blank=True)
    thumbnail = ResizedImageField(size=[50, 50], crop=['middle', 'center'], upload_to=upload_profile_thumbnail, blank=True)

    slug = AutoSlugField(populate_from='get_slug_name', unique=True, always_update=True)

    location = models.CharField(max_length=128, blank=True, null=True)
    summary = models.CharField(max_length=256, blank=True, null=True)

    def get_slug_name(self):
        name = self.user.username
        return name


