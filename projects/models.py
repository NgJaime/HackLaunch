from django.db import models
from autoslug import AutoSlugField
from froala_editor.fields import FroalaField
from django.contrib.postgres.fields import ArrayField
from users.models import User


class Tags(models.Model):
    tag = models.CharField(max_length=64)


class Technologies(models.Model):
    name = models.CharField(max_length=128)

#
# class Views(models.Model):
#     project =
#
# class Followers


class Project(models.Model):
    logo = FroalaField(options={'inlineMode': True, 'placeholder': 'Add a logo'},
                       plugins=('image'))
    title = FroalaField(options={'inlineMode': True, 'alwaysVisible': True, 'placeholder': 'Name your project'})
    tag_line = FroalaField(options={'inlineMode': True, 'alwaysVisible': True, 'placeholder': 'Provide a tag line for your project.'},
                           plugins=('font_size', 'font_family', 'colors', 'block_styles', 'char_counter'))
    pitch = FroalaField(options={'placeholder': 'Create a pitch for your project it can include images, videos and embeded youtube content.'},
                        plugins=('font_size', 'font_family', 'colors', 'block_styles', 'video', 'tables', 'lists', 'char_counter', 'urls', 'inline_styles'))
    posts = ArrayField(FroalaField())
    tags = models.ManyToManyField(Tags)

    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)

    creators = models.ManyToManyField(User, through='ProjectCreators')
    technologies = models.ManyToManyField(Technologies, through='ProjectTechnologies')

    facebook = models.URLField()
    google_plus = models.URLField()
    instagram = models.URLField()
    pinterest = models.URLField()
    twitter = models.URLField()



class ProjectCreators(models.Model):
    project = models.ForeignKey(Project)
    creator = models.ForeignKey(User)
    summary = FroalaField(options={'inlineMode': True, 'alwaysVisible': True, 'placeholder': 'Name your project'},
                          plugins=('font_size', 'font_family', 'colors', 'block_styles', 'char_counter'))
    date_joined = models.DateField()


class ProjectTechnologies(models.Model):
    project = models.ForeignKey(Project)
    technologies = models.ForeignKey(Technologies)
    strength = models.SmallIntegerField()

    date_joined = models.DateField()

