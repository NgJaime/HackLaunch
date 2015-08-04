from base.tests import BaseAcceptanceTest

from users.models import User, UserProfile
from events.models import Event
from projects.models import Project

class SitemapTest(BaseAcceptanceTest):
    def setUp(self):
        self.user = User.objects.create_user('test-user')
        self.profile = UserProfile.objects.create(user=self.user)
        self.event = Event.objects.create(name='test-event')
        self.project = Project.objects.create(title='<p>awesome-project</p>', is_active=True)

    def test_sitemap(self):
        response = self.client.get('/sitemap.xml')
        self.assertEquals(response.status_code, 200)

        self.assertTrue('/users/test-user' in response.content)
        self.assertTrue('/events/test-event' in response.content)
        self.assertTrue('/projects/awesome-project' in response.content)
        self.assertTrue('/projects/list/' in response.content)

        self.assertTrue('/terms/' in response.content)
        self.assertTrue('/credits/' in response.content)
