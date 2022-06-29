from datetime import datetime, timedelta
from random import randint
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Project, Tag

# Create your tests here.

def create_project(days: datetime=0) -> Project:
    """
    Create object models to use in our test If the pub_date needs to be in the past use days parameters as a negative number, it is in the future use a positive number.
    """
    headline: str = 'a long string, but not so long'
    example_text: str = 'a string '*400
    title: str = 'Project test example'
    pub_date: datetime = timezone.now() + timedelta(days)

    project: Project = Project.objects.create(title=title, headline=headline, content_text=example_text, pub_date=pub_date)
    project.save()

    return project

def create_tag(title: str) -> Tag:
    tag = Tag(tag_name=title)
    tag.save()

    return tag

def create_project_tags(project: Project, tags: list[Tag]) -> Project:
    """
    Create a tag object, using two parameters:
    - project: Project Model
    - text: str
    """
    for tag in tags:
        project.tag_set.add(tag)

    return project


class ProjectsModelTests(TestCase):
    """
    Validate if the Project Model is working correctly
    """
    #def setUp(self):
    #    """Model to test"""
    #    project = create_project(days=0)

    def test_project_model_is_created_sucesfully(self):
        """
        Test verify if the project object was created correctly
        """
        project = create_project(days=0)
        self.assertIsInstance(project, Project)

#    def test_project_model_title_max_text_length(self):
#        """
#        If the project's model title is longger than 50 characters, must returns
#        a forms.ValidationError
#        """
#        project = create_project(days=0)
#        project.title = 'i'*randint(51, 100)
#
#    def test_project_model_title_min_text_length(self):
#        """
#        If the project's model title is less than 5 characters. must raise ValueError
#        """
#        project = create_project(days=0)
#        with self.assertRaises(ValueError):
#            project.title = 'i'*randint(0, 5)

    def test_project_method_with_recently_pub_date(self):
        """
        If the "pub_date" is recently, the method must return a True value
        """
        project = create_project(days=0)
        self.assertEqual(project.was_published_recently(), True)

    def test_project_method_with_past_pub_date(self):
        """
        If the "pub_date" is greater than 1 week in the past, the method must return a False value
        """
        project = create_project(days=-7)
        self.assertEqual(project.was_published_recently(), False)

    def test_project_method_with_future_pub_date(self):
        """
        If the "pub_date" is greater than 1 week in the future, the method must return a False value
        """
        project = create_project(days=7)
        self.assertEqual(project.was_published_recently(), False)

#    def test_headline_attribute_must_be_less_or_equal_than_100(self):
#        """
#        If the headline chars are greater than 100, must raise a ValueError
#        """
#        project = create_project(days=0)
#        with self.assertRaises(ValueError):
#            project.headline = 'i'*randint(101, 150)
#
#    def test_project_content_text_length_is_more_than_200_chars(self):
#        """
#        If the "content_text" length is less than 200, must work correctly
#        """
#        project = create_project(days=0)
#        project.content_text = "a"*250
#        self.assertGreaterEqual(len(project.content_text), 200)
#
#    def test_project_content_text_length_is_more_than_200_chars(self):
#        """
#        If the "content_text" length is less than 200, must work correctly
#        """
#        project = create_project(days=0)
#        with self.assertRaises(ValueError):
#            project.title = 'i'*randint(0, 200)

class TagsModelTests(TestCase):
    """
    Validate if the Project Model is working correctly
    """
    #def setUp(self):
    #    """Model to test"""
    #   tag = create_tag('an title example')

    def test_tag_was_created_sucesfully(self):
        """
        Validate if the tag object model can be created correctly
        """
        tag = create_tag('an title example')
        self.assertIsInstance(tag, Tag)

    def test_tag_title_is_a_string(self):
        """Validate if the tag title attribute is a string value"""
        tag = create_tag('an title example')
        self.assertIs(type(tag.tag_name), str)

class ProjectTagsTests(TestCase):
    """
    Validate if the project tags works correctly
    """
    #def setUp(self):
    #    """Model to test"""
    #    project = create_project(days=-1)
    #
    #    tags = [create_tag('a random tag') for i in range(0, 3)]
    #    project = create_project_tags(project=project, tags=tags)

    def test_verify_if_project_only_receive_tags_models(self):
        """
        The project model only can receive a Tag model, if another data type is got must raise a TypeError
        """
        project = create_project(days=0)
        with self.assertRaises(TypeError):
            project.tag_set.add(project)

    def test_project_return_all_the_tags_correctly(self):
        """
        The project model must return all the tags, and return them.
        """
        project = create_project(days=0)
        self.assertIsInstance(project, Project)
        self.assertQuerysetEqual(project.tag_set.all(), [])

class HomeViewTests(TestCase):
    """
    Test all the project views
    """
    def test_home_page_request_has_a_OK_status_code_response(self):
        """
        If the server gets a request to get the main page, must return a status code
        200.
        """
        
        # project = create_project()
        # tags = [create_tag(f'tag{i}') for i in range(0, 3)]
        # create_project_tags(project, tags)

        response = self.client.get(reverse('main:home'))

        self.assertEqual(response.status_code, 200)

    def test_home_page_with_one_past_and_one_future_project(self):
        """
        If the project contains one past and one future project, it only musts returns the
        past projects.
        """
        project = create_project(-5)
        future_project = create_project(5)
        tags = [create_tag('a random tag') for i in range(0, 3)]
        project = create_project_tags(project, tags)
        future_project = create_project_tags(future_project, tags)

        response = self.client.get(reverse('main:home'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_projects_list'],
            [project]
        )

    def test_home_page_services_section_with_many_projects(self):
        """
        If the services secction contains more than 1 project must be displayed only the past or recently projects
        """
        project_list: list[Project] = [create_project(0 - i) for i in range(0, 3)]
        tags = [create_tag(f'a random tag{i}') for i in range(0, 3)]

        project_list = [create_project_tags(project, tags) for project in project_list]
        response = self.client.get(reverse('main:home'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_projects_list'],
            project_list
        )

class ProjectsViewTests(TestCase):

    def test_project_page_request_has_OK_response(self):
        """
        The project page must have a 200 status code response
        """
        response = self.client.get(reverse('main:projects'))
        self.assertEqual(response.status_code, 200)

    def test_project_page_display_all_recently_and_past_projects(self):
        """
        If there're many projects must display all the past and recently
        projects.
        """
        project_list: list[Project] = [create_project(0 - i) for i in range(0, 3)]
        tags = [create_tag(f'a random tag{i}') for i in range(0, 3)]

        project_list = [create_project_tags(project, tags) for project in project_list]

        response = self.client.get(reverse('main:projects'))
        
        self.assertQuerysetEqual(
            response.context['latest_projects_list'],
            project_list
        )
