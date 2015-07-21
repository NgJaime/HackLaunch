from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.conf import settings
from django.templatetags.static import static
from django.core.files.temp import NamedTemporaryFile

from django_gravatar.helpers import get_gravatar_url
from autoslug import AutoSlugField
from s3 import upload_profile_image, upload_profile_thumbnail
from urllib2 import urlopen

import pycountry

COUNTRIES = [[c.alpha2, c.name] for c in pycountry.countries]


class Skill(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class MakerTypes(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    nonSocialAuth = models.BooleanField(default=False)

    def getDateJoinedMonth(self):
        return self.date_joined.strftime("%B")

    def getDateJoinedDayMonthYear(self):
        return self.date_joined.strftime("%d/%m/%y")

    def save(self, *args, **kw):
        if self.pk is not None:
            original = User.objects.get(pk=self.pk)
            if original.nonSocialAuth and original.password != self.password:
                self.send_password_changed_email()

        else:
            self.send_welcome_email()

        self.username = self.username.lower()

        super(User, self).save(*args, **kw)

    def send_password_changed_email(self):
        context = {
            'first_name': self.first_name,
            'email': self.email
        }

        html_message = get_template('password_changed_email.html').render(Context(context))
        email = EmailMessage('Your password at HackLaunch has been changed', html_message, to=[self.email],
                             from_email=settings.EMAIL_FROM)
        email.content_subtype = 'html'
        email.send()

    def send_welcome_email(self):
        context = {
            'first_name': self.first_name
        }

        html_message = get_template('welcome_email.html').render(Context(context))
        email = EmailMessage('Welcome to Hacklaunch', html_message, to=[self.email],
                             from_email=settings.SECONDARY_EMAIL_FROM)
        email.content_subtype = 'html'
        email.send()


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    skills = models.ManyToManyField(Skill)
    maker_type = models.ManyToManyField(MakerTypes)

    image = ResizedImageField(size=[250, 250], crop=['middle', 'center'], upload_to=upload_profile_image, blank=True)
    thumbnail = ResizedImageField(size=[50, 50], crop=['middle', 'center'], upload_to=upload_profile_thumbnail,
                                  blank=True)

    slug = AutoSlugField(populate_from='get_slug_name', unique=True, always_update=True)

    location = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)
    summary = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return self.user.get_full_name()

    def save(self, *args, **kw):
        if self.pk is None:
            if self.image is None:
                self.get_gravatar_profile_image()

        super(UserProfile, self).save(*args, **kw)

    def get_slug_name(self):
        name = self.user.username
        return name

    @models.permalink
    def get_absolute_url(self):
        return ("profile_view", [self.slug])

    def get_full_country_name(self):
        if self.country and self.country != u'-1':
            return pycountry.countries.get(alpha2=self.country).name
        else:
            return None

    def get_gravatar_profile_image(self):
        url = get_gravatar_url(self.user.email, size=230)
        image_request_result = urlopen(url)

        temp_file = NamedTemporaryFile(delete=True)
        temp_file.write(image_request_result.read())
        temp_file.flush()

        extension = image_request_result.headers.subtype
        thumbnail_file_name = upload_profile_thumbnail(None, self.user.username + '.' + extension)
        image_file_name = upload_profile_image(None, self.user.username + '.' + extension)

        self.thumbnail.save(thumbnail_file_name, temp_file)
        self.image.save(image_file_name, temp_file)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.user.email:
            self.get_gravatar_profile_image()
            return self.thumbnail.url
        else:
            return static('images/avatar.jpg')




