"""Unit tests for the Tag Model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import Tag
from django.db.utils import IntegrityError

class TagModelTestCase(TestCase):
    """Unit tests for the Tag Model"""


    def setUp(self):
        self.tag = Tag(name="UniqueTag")
        self.tag.save()
    
    def test_tag_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="UniqueTag")
    
    def test_tag_str_method(self):
        self.assertEqual(str(self.tag), 'UniqueTag')
    
    def test_colour_field_default_value(self):
        self.assertEqual(self.tag.colour, "#61D0FF")
    
    def test_valid_colour(self):
        tag = Tag.objects.create(name="UniqueTag2", colour="#777777")
        tag.full_clean()
        tag.save()
        self.assertEqual(tag.colour,"#777777")
    
    def test_invalid_colour_length(self):
        with self.assertRaises(ValidationError):
            tag = Tag.objects.create(name="UniqueTag2", colour="#2345678")
            tag.full_clean()