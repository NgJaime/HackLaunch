from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from users.models import UserProfile
from events.models import Event

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['home', 'terms', 'credits']

    def location(self, item):
        return reverse(item)


class ProfileSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return UserProfile.objects.all()


class EventsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.75
    protocol = 'https'

    def items(self):
        return Event.objects.all()
