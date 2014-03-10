from django.test import TestCase

from rollcall.groups.models import Group


class GroupTestCase(TestCase):

    def test_detects_non_quad_format(self):
        group = Group(email='devops@example.com')
        self.assertFalse(group.is_quad_format)

    def test_matches_quad_format(self):
        group = Group(email='foo-bar-baz-discuss@example.com')
        self.assertTrue(group.is_quad_format)

    def test_only_matches_known_list_types(self):
        group = Group(email='foo-bar-baz-bizzle@example.com')
        self.assertFalse(group.is_quad_format)

    def test_matches_split_subject(self):
        group = Group(email='foo-bar-stuff-and-things-discuss@example.com')
        self.assertTrue(group.is_quad_format)
