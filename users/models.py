import pycountry

from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.conf import settings
from autoslug import AutoSlugField
from s3 import upload_profile_image, upload_profile_thumbnail


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

    image = ResizedImageField(size=[230, 230], crop=['middle', 'center'], upload_to=upload_profile_image, blank=True)
    thumbnail = ResizedImageField(size=[50, 50], crop=['middle', 'center'], upload_to=upload_profile_thumbnail,
                                  blank=True)

    slug = AutoSlugField(populate_from='get_slug_name', unique=True, always_update=True)

    location = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)
    summary = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return self.user.get_full_name()

    def get_slug_name(self):
        name = self.user.username
        return name

    @models.permalink
    def get_absolute_url(self):
        return ("profile_view", [self.slug])

    def get_full_country_name(self):
        if self.country:
            return pycountry.countries.get(alpha2=self.country).name
        else:
            return None


