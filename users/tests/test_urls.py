from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import home, assignment, logout_view, handling, submit_complaint, rules

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('users:home')
        self.assertEquals(resolve(url).func, home)
    
    def test_assignment_url_is_resolved(self):
        url = reverse('users:assignment')
        self.assertEquals(resolve(url).func, assignment)
    
    def test_logout_url_is_resolved(self):
        url = reverse('users:logout')
        self.assertEquals(resolve(url).func, logout_view)
    
    def test_handling_url_is_resolved(self):
        url = reverse('users:handling')
        self.assertEquals(resolve(url).func, handling)
    
    def test_complains_url_is_resolved(self):
        url = reverse('users:complaints')
        self.assertEquals(resolve(url).func, submit_complaint)
    
    def test_rules_url_is_resolved(self):
        url = reverse('users:rules')
        self.assertEquals(resolve(url).func, rules)