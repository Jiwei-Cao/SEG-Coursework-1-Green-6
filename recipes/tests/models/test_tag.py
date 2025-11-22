"""Unit tests for the Tag Model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import Tag
from django.db.utils import IntegrityError

class TagModelTestCase(TestCase):
    """Unit tests for the Tag Model"""

    fixture = 'recipes/tests/fixtures/default_tags.json'

    def setUp(self):
        self.tag = Tag(name="Vegan")
        self.tag.save()
    
    def test_tag_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="Vegan")
    
    def test_tag_str_method(self):
        self.assertEqual(str(self.tag), 'Vegan')