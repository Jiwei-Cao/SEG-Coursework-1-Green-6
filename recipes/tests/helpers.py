from django.urls import reverse
from django.test import TestCase

def reverse_with_next(url_name, next_url):
    """Extended version of reverse to generate URLs with redirects"""
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url


class LogInTester:
    """Class support login in tests."""
 
    def _is_logged_in(self):
        """Returns True if a user is logged in.  False otherwise."""

        return '_auth_user_id' in self.client.session.keys()

class MenuTesterMixin(TestCase):
    """Class to extend tests with tools to check the presents of menu items."""

    menu_urls = [
        reverse('password'), reverse('profile'), reverse('log_out')
    ]

    def assert_menu(self, response):
        """Check that menu is present."""
        html = response.content.decode("utf-8")

        for url in self.menu_urls:
            self.assertIn(f'href="{url}"', html)

    def assert_no_menu(self, response):
        """Check that no menu is present."""
        html = response.content.decode("utf-8")

        for url in self.menu_urls:
            self.assertNotIn(f'<a href="{url}">', html)