from django.test import TestCase

from django.core.urlresolvers import resolve
from .views import index

class MainPageTests(TestCase):

    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEquals(main_page.func, index)

    def test_returns_proper_status_code(self):
        index = self.client.get('/')
        self.assertEquals(index.status_code, 200)

    def test_uses_index_html_template(self):
        index = self.client.get('/')
        self.assertTemplateUsed(index, 'public_main.html')

    # def test_index_handles_loggedin_user(self):
    #     self.assertTemplateUsed(resp, '')
