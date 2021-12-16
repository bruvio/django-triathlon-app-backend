from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@testemail.com', password='testpass'):
    """Creates a user for testing"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'test@testemail.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that email for new user is normalized"""
        email = 'test@TESTEMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        """Test creating a new super user from the command line"""
        user = get_user_model().objects.create_superuser(
            'test@testemail.com',
            'password123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_activity_str(self):
        """Test the activity string representation"""
        activity = models.Activity.objects.create(
            user=sample_user(),
            distance=5,
            time_hours=0,
            time_minutes=23,
            time_seconds=52,
            elevation=73,
            sport='run',
            date='2022-01-01',
            start_time='12:00',
            title='My first run',
            description='This is my first run',
            type='workout',
            effort=5,
        )

        self.assertEqual(str(activity), activity.title)

    @patch('uuid.uuid4')
    def test_activity_filename_uuid(self, mock_uuid):
        """Test image is saved in correct location"""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = models.activity_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/activity/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
