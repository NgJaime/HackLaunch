from base.tests import BaseAcceptanceTest

from users.models import User, UserProfile
from events.models import Event

class SitemapTest(BaseAcceptanceTest):
    def setUp(self):
        self.user = User.objects.create_user('test-user')
        self.profile = UserProfile.objects.create(user=self.user)
        self.event = Event.objects.create(name='test-event')

        self.user.save()
        self.profile.save()
        self.event.save()

    def test_sitemap(self):
        response = self.client.get('/sitemap.xml')
        self.assertEquals(response.status_code, 200)

        self.assertTrue('/profile/test-user' in response.content)
        self.assertTrue('/events/test-event' in response.content)

        self.assertTrue('/terms/' in response.content)
        self.assertTrue('/credits/' in response.content)
