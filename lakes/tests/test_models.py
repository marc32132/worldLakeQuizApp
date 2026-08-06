from django.test import TestCase
from lakes.models import Lake

class TestLakesModel(TestCase):

    def test_lake_string_representation(self):
        '''Verify correct string data representation.'''

        lake = Lake.objects.create(name='A Lake', country='Poland')

        self.assertEqual(str(lake), 'A Lake')
