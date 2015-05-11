from django.test import TestCase, LiveServerTestCase, Client


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()
