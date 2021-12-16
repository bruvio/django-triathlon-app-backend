import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Activity(models.Model):
    """Activity object"""

    ACTIVITY_CHOICES = (
        ('run', 'Run'),
        ('bike', 'Bike'),
        ('swim', 'Swim'),
    )

    ACTIVITY_TYPES = {
        ('race', 'Race'),
        ('workout', 'Workout'),
        ('wu', 'Warm Up'),
        ('cd', 'Cool Down'),
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    distance = models.DecimalField(max_digits=4, decimal_places=2)
    time_hours = models.IntegerField()
    time_minutes = models.IntegerField()
    time_seconds = models.IntegerField()
    elevation = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sport = models.CharField(choices=ACTIVITY_CHOICES, default="run", max_length=255)  # noqa: E501
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default='12:00')
    title = models.CharField(max_length=255, default="My Workout"+str(timezone.now))  # noqa: E501
    description = models.CharField(max_length=10000, blank=True)
    type = models.CharField(choices=ACTIVITY_TYPES, default='workout', max_length=255)  # noqa: E501
    effort = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])  # noqa: E501
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
