# Define a custom User class to work with django-social-auth
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField

class CustomUser(AbstractUser):
    slug = AutoSlugField(unique=True)
