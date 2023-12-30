from django.test import TestCase

from lists.views import home_page

class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_used_home_templates(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
