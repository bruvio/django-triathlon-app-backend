# import tempfile
# import os

# from PIL import Image
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Activity

from activity.serializers import ActivitySerializer

ACTIVITY_URL = reverse('activity:activity-list')


def sample_activity(user, **params):
    """Create and return a sample activity"""
    defaults = {
            'distance': 5,
            'time_hours': 0,
            'time_minutes': 23,
            'time_seconds': 52,
            'elevation': 73,
            'sport': 'run',
            'date': '2022-01-01',
            'start_time': '12:00',
            'title': 'My first run',
            'description': 'This is my first run',
            'type': 'workout',
            'effort': 5,
    }
    defaults.update(params)

    return Activity.objects.create(user=user, **defaults)


class PublicActivityApiTests(TestCase):
    """Test unauthenticated activity API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        response = self.client.get(ACTIVITY_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateActivityApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@testemail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """Test rectreiving a list of activities"""
        sample_activity(user=self.user)
        sample_activity(user=self.user)

        response = self.client.get(ACTIVITY_URL)

        activities = Activity.objects.all().order_by('-id')
        serializer = ActivitySerializer(activities, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """Test retrieving activities for user"""
        user2 = get_user_model().objects.create_user(
            'other@testemail.com',
            'testpass2'
        )
        sample_activity(user=user2)
        sample_activity(user=self.user)

        response = self.client.get(ACTIVITY_URL)

        activities = Activity.objects.filter(user=self.user)
        serializer = ActivitySerializer(activities, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    # def test_create_basic_recipe(self):
    #     """Test creating recipe"""
    #     payload = {
    #         'title': 'Chocolate chesecake',
    #         'time_minutes': 30,
    #         'price': 5.00
    #     }
    #     response = self.client.post(RECIPES_URL, payload)

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     recipe = Recipe.objects.get(id=response.data['id'])

    #     for key in payload.keys():
    #         self.assertEqual(payload[key], getattr(recipe, key))

    # def test_partial_update_recipe(self):
    #     """Test updating a recipe with patch"""
    #     recipe = sample_recipe(user=self.user)
    #     recipe.tags.add(sample_tag(user=self.user))
    #     new_tag = sample_tag(user=self.user, name='Curry')

    #     payload = {'title': 'Chicken Salad', 'tags': [new_tag.id]}
    #     url = detail_url(recipe.id)
    #     self.client.patch(url, payload)

    #     recipe.refresh_from_db()
    #     self.assertEqual(recipe.title, payload['title'])
    #     tags = recipe.tags.all()
    #     self.assertEqual(tags.count(), 1)
    #     self.assertIn(new_tag, tags)

    # def test_full_update_recipe(self):
    #     """Test updating a recipe with put"""
    #     recipe = sample_recipe(user=self.user)
    #     recipe.tags.add(sample_tag(user=self.user))
    #     payload = {
    #         'title': 'Omelette du Fromage',
    #         'time_minutes': 20,
    #         'price': 4.50
    #     }
    #     url = detail_url(recipe.id)
    #     self.client.put(url, payload)

    #     recipe.refresh_from_db()
    #     self.assertEqual(recipe.title, payload['title'])
    #     self.assertEqual(recipe.time_minutes, payload['time_minutes'])
    #     self.assertEqual(recipe.price, payload['price'])
    #     tags = recipe.tags.all()
    #     self.assertEqual(tags.count(), 0)
