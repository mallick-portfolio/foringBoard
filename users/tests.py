from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

User = get_user_model()

class UserManagerTests(TestCase):
    def test_create_user(self):
        """Test creating a new user"""
        email = 'tZVtX@example.com'
        password = 'testpass123'
        user = User.objects.create_user(email, password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['7YH6l@example.com', '7YH6l@example.com'],
            ['4F2lR@example.com', '4F2lR@example.com'],
            ['tZVtX@Example.com', 'tZVtX@example.com'],
        ]
        for email, expected in sample_emails:
            user = User.objects.create_user(email, 'testpass123', username=f'test{email}')
            self.assertEqual(user.email, expected)

