from django.db import models
from autoslug import AutoSlugField
from froala_editor.fields import FroalaField
from django.contrib.postgres.fields import ArrayField
from users.models import User
from datetime import datetime


class Tags(models.Model):
    tag = models.CharField(max_length=64)

    def __unicode__(self):
        return self.tag


class Technologies(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


# class Views(models.Model):
#     project =
#
# class Followers


class Project(models.Model):
    logo = FroalaField(options={'inlineMode': True, 'placeholder': 'Add a logo'},
                       plugins=('image'), blank=True)
    title = FroalaField(options={'inlineMode': True, 'alwaysVisible': True, 'placeholder': 'Name your project',
                                 'blockStyles': {'p': {'margin': '0px;'}}}, blank=True)
    tag_line = FroalaField(options={'inlineMode': True, 'alwaysVisible': True,
                                    'placeholder': 'Provide a tag line for your project.'},
                           plugins=('font_size', 'font_family', 'colors', 'block_styles', 'char_counter'), blank=True)
    pitch = FroalaField(options={'placeholder': 'Create a pitch for your project it can include images, videos and embeded youtube content.'},
                        plugins=('font_size', 'font_family', 'colors', 'block_styles', 'video', 'tables', 'lists', 'char_counter', 'urls', 'inline_styles'),
                        blank=True)
    posts = ArrayField(FroalaField(), blank=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True)

    slug = AutoSlugField(populate_from='get_slug_seed', unique=True, always_update=True)

    creators = models.ManyToManyField(User, through='ProjectCreators')
    technologies = models.ManyToManyField(Technologies, through='ProjectTechnologies', blank=True)

    facebook = models.URLField(blank=True)
    google_plus = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_slug_seed(self):
        if self.is_active:
            return self.title
        else:
            return "new-project"


class ProjectCreators(models.Model):
    project = models.ForeignKey(Project)
    creator = models.ForeignKey(User)
    summary = FroalaField(options={'inlineMode': True, 'alwaysVisible': True, 'placeholder': 'Name your project'},
                          plugins=('font_size', 'font_family', 'colors', 'block_styles', 'char_counter'),
                          blank=True)
    date_joined = models.DateField()
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = (("project", "creator"),)

    def __unicode__(self):
        return self.project.title + ' ' + self.creator.get_full_name()

    def save(self, *args, **kw):
        if self.pk is None:
            self.date_joined = datetime.now()

        super(ProjectCreators, self).save(*args, **kw)


class ProjectTechnologies(models.Model):
    project = models.ForeignKey(Project)
    technology = models.ForeignKey(Technologies)
    strength = models.SmallIntegerField(blank=True, null=True)

    date_added = models.DateField()

    class Meta:
        unique_together = (("project", "technology"),)

    def __unicode__(self):
        return self.project.title + ' ' + self.technology.name

    def save(self, *args, **kw):
        if self.pk is None:
            self.date_added = datetime.now()

        super(ProjectTechnologies, self).save(*args, **kw)
