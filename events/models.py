from django.db import models
from autoslug import AutoSlugField
from users.models import User

class Event(models.Model):
    users = models.ManyToManyField(User, blank=True)

    name = models.CharField(max_length=128)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)