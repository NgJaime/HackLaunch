from django.db import models
from autoslug import AutoSlugField
from froala_editor.fields import FroalaField
from django_resized import ResizedImageField
from users.models import User
from datetime import datetime
from taggit.managers import TaggableManager

from projects.s3 import upload_project_image, upload_logo


class Technologies(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Technology'
        verbose_name_plural = 'Technologies'


# class Views(models.Model):
#     project =
#

class   Project(models.Model):
    logo = ResizedImageField(size=[125, 100], crop=['middle', 'center'], upload_to=upload_logo, blank=True, null=True)
    title = FroalaField(options={'inlineMode': True, 'alwaysVisible': True, 'placeholder': 'Name your project',
                                 'blockStyles': {'p': {'margin': '0px;'}}}, blank=True)
    tag_line = FroalaField(options={'inlineMode': True, 'alwaysVisible': True,
                                    'placeholder': 'Provide a tag line for your project.'},
                           plugins=('font_size', 'font_family', 'colors', 'block_styles', 'char_counter'), blank=True)
    pitch = FroalaField(options={'placeholder': 'Create a pitch for your project it can include images, videos and embeded youtube content.',
                                 'saveURL': '/projects/update_project/', 'autosave': True, 'autosaveInterval': 2500},
                        plugins=('font_size', 'font_family', 'colors', 'block_styles', 'video', 'tables', 'lists', 'char_counter', 'urls', 'inline_styles'),
                        blank=True)
    tags = TaggableManager()
    creators = models.ManyToManyField(User, through='ProjectCreator')
    followers = models.ManyToManyField(User, through='Follower', related_name='project_follower')
    technologies = models.ManyToManyField(Technologies, through='ProjectTechnologies', blank=True)

    facebook = models.URLField(blank=True)
    google_plus = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    slug = AutoSlugField(populate_from='get_slug_seed', unique=True, always_update=True)

    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title[3:-4] + ' - ' + str(self.id)

    def get_slug_seed(self):
        if self.is_active:
            return self.title[3:-4]
        else:
            return "new-project"


class Follower(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User, related_name="follower")
    date_followed = models.DateField()

    class Meta:
        unique_together = (("project", "user"),)

    def save(self, *args, **kw):
        self.date_followed = datetime.now()
        super(Follower, self).save(*args, **kw)

    def __unicode__(self):
        return self.project.title + ' - ' + self.user.get_full_name()


class Post(models.Model):
    title = FroalaField(options={'inlineMode': True, 'placeholder': 'Add a title for your new post', 'colorGroups': {'text': 'Text', 'cmd': 'foreColor', 'colors': ['#FFFFFF' 'REMOVE']}})
    post = FroalaField(options={'placeholder': 'Create a post for your project it can include images, videos and embeded youtube content.'},
                       plugins=('font_size', 'font_family', 'colors', 'block_styles', 'video', 'tables', 'lists', 'char_counter', 'urls', 'inline_styles'),
                       blank=True)
    project = models.ForeignKey(Project)
    date_added = models.DateField(blank=True)
    last_updated = models.DateField(blank=True, null=True)
    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title + ' [' + self.author.get_full_name() + ']'

    def save(self, *args, **kw):
        if self.pk is None:
            self.date_added = datetime.now()

        self.last_updated = datetime.now()

        super(Post, self).save(*args, **kw)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project)
    image = ResizedImageField(upload_to=upload_project_image, blank=True)

    def __unicode__(self):
        return self.image.url


class ProjectCreator(models.Model):
    project = models.ForeignKey(Project)
    creator = models.ForeignKey(User)
    # todo place holder bnot displaying
    summary = FroalaField(options={'inlineMode': True, 'alwaysVisible': True, 'placeholder': 'Summarise how this creator has contributed'},
                          plugins=('font_size', 'font_family', 'colors', 'block_styles', 'char_counter'),
                          blank=True)
    date_joined = models.DateField()
    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    awaiting_confirmation = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (("project", "creator"),)

    def __unicode__(self):
        return self.project.title + ' ' + self.creator.get_full_name()

    def save(self, *args, **kw):
        if self.pk is None:
            self.date_joined = datetime.now()

        super(ProjectCreator, self).save(*args, **kw)


class ProjectTechnologies(models.Model):
    project = models.ForeignKey(Project)
    technology = models.ForeignKey(Technologies)
    strength = models.SmallIntegerField(blank=True, null=True)

    date_added = models.DateField()

    class Meta:
        unique_together = (("project", "technology"),)
        verbose_name = 'ProjectTechnology'
        verbose_name_plural = 'ProjectTechnologies'

    def __unicode__(self):
        return self.project.title + ' ' + self.technology.name

    def save(self, *args, **kw):
        if self.pk is None:
            self.date_added = datetime.now()

        super(ProjectTechnologies, self).save(*args, **kw)

