from datetime import datetime, timedelta
from random import randint
from django.test import TestCase
from django.utils import timezone

# Create your tests here.

class ProjectsModelTests(TestCase):
    """
    Validate if the Project Model is working correctly
    """
    def setUp(self):
        """Model to test"""
        headline: str = 'a long string, but not so long'
        example_text: str = 'a string '*400
        title: str = 'Project test example'
        pub_date: datetime = timezone.now()

        project_test: Project = Project(title, headline, example_text, pub_date)
        project.save()

    def test_project_model_is_created_sucesfully(self):
        """
        Test verify if the project object was created correctly
        """
        self.assertIs(self.project.example_text, str)
        self.assertIs(self.project.title, str)
        self.assertIs(self.project.pub_date, datetime)

    def test_project_model_title_max_text_length(self):
        """
        If the project's model title is longger than 50 characters, must returns
        a forms.ValidationError
        """
        with self.assertRaises(ValueError):
            self.project.title = 'i'*randint(50, 100)

    def test_project_model_title_min_text_length(self):
        """
        If the project's model title is less than 5 characters. must raise ValueError
        """
        with self.assertRaises(ValueError):
            self.project.title = 'i'*randint(0, 5)

    def test_project_method_with_recently_pub_date(self):
        """
        If the "pub_date" is recently, the method must return a True value
        """
        self.assertEqual(self.project.was_published_recently(), True)

    def test_project_method_with_past_pub_date(self):
        """
        If the "pub_date" is greater than 1 week in the past, the method must return a False value
        """
        self.project.pub_date = timezone.now() - timedelta(7)
        self.assertEqual(self.project.was_published_recently(), False)

    def test_project_method_with_future_pub_date(self):
        """
        If the "pub_date" is greater than 1 week in the future, the method must return a False value
        """
        self.project.pub_date = timezone.now() + timedelta(7)
        self.assertEqual(self.project.was_published_recently(), False)

    def test_headline_attribute_must_be_less_or_equal_than_100(self):
        """
        If the headline chars are greater than 100, must raise a ValueError
        """
        with self.assertRaises(ValueError):
            self.project.headline = 'i'*randint(101, 150)

    def test_project_content_text_length_is_more_than_200_chars(self):
        """
        If the "content_text" length is less than 200, must work correctly
        """
        self.project.content_text = "a"*250
        self.assertGreaterEqual(len(self.project_content_text), 200)

    def test_project_content_text_length_is_more_than_200_chars(self):
        """
        If the "content_text" length is less than 200, must work correctly
        """
        with self.assertRaises(ValueError):
            self.project.title = 'i'*randint(0, 200)

class TagsModelTests(TestCase):
    """
    Validate if the Project Model is working correctly
    """
    def setUp(self):
        """Model to test"""
        title: str = 'Tag title example'
        tag = Tag(title)

        # Saving the tag
        tag.save()

    def test_tag_was_created_sucesfully(self):
        """
        Validate if the tag object model can be created correctly
        """
        self.assertEqual(self.tag.title, str)
 
    def test_tag_title_is_not_longer(self):
        """
        If the tag's title is too long it must raise a ValueError
        """
        with self.assertRaises(ValueError):
            self.tag.title = 'a'*randint(16, 20)

    def test_tag_title_is_not_too_short(self):
        """
        Validate the tag length, if is shorter than 3, must raise a ValueError
        """
        with self.assertRaises(ValueError):
            self.tag.title = 'a'*randint(0, 3)

class ProjectTagsTests(TestCase):
    """
    Validate if the project tags works correctly
    """
    def setUp(self):
        """Model to test"""
        headline: str = 'a long string, but not so long'
        example_text: str = 'a string '*400
        title: str = 'Project test example'
        pub_date: datetime = timezone.now()

        project_test: Project = Project(title, headline, example_text, pub_date)
        project.save()

        tag1 = Tag(title='News')
        tag2 = Tag(title='Latin America')
        tag3 = Tag(title='Social Media')

        project.Tag.add((tag1,tag2,tag3,))