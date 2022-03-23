from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APITestCase

from .models import User
from rest_framework.authtoken.models import Token


class UserRegisterTestCase(APITestCase):

    def test_register_user(self):
        initial_user_count = User.objects.count()
        user_attrs = {
            'username': 'testcaseuser',
            'password': 'Password1',
            'is_admin': False
        }
        response = self.client.post('/api/user/register/',
                                    user_attrs, format='json')
        if response.data['status_code'] != 201:
            print(response.data)
        self.assertEqual(
            User.objects.count(),
            initial_user_count + 1
        )
        self.assertEqual(response.data['result']['username'],
                         user_attrs['username'])
        self.assertEqual(response.data['result']['is_admin'],
                         user_attrs['is_admin'])
        try:
            token = Token.objects.get(key=response.data['token'])
        except ObjectDoesNotExist:
            token = None
        self.assertNotEqual(token, None)
        self.assertEqual(
            response.data['result']['id'],
            token.user_id
        )


class UserLoginTestCase(APITestCase):

    def test_login_user(self):
        User.objects.create_user(username='testcaseuser',
                                 password='Password1',
                                 is_admin=False)
        user_attrs = {
            'username': 'testcaseuser',
            'password': 'Password1',
        }
        response = self.client.post('/api/user/login/',
                                    user_attrs, format='json')
        if response.data['status_code'] != 200:
            print(response.data)
        self.assertEqual(response.data['result']['username'],
                         user_attrs['username'])
        try:
            token = Token.objects.get(key=response.data['token'])
        except ObjectDoesNotExist:
            token = None
        self.assertNotEqual(token, None)
        self.assertEqual(
            response.data['result']['id'],
            token.user_id
        )


class UserLogoutTestCase(APITestCase):

    def test_logout_user(self):
        user = User.objects.create_user(username='testcaseuser',
                                        password='Password1',
                                        is_admin=False)
        user_attrs = {
            'username': 'testcaseuser',
            'password': 'Password1',
        }
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post('/api/user/logout/')
        if response.data['status_code'] != 200:
            print(response.data)
        self.assertEqual(response.data['result']['username'],
                         user_attrs['username'])
        try:
            token = Token.objects.get(user_id=user.id)
        except ObjectDoesNotExist:
            token = None
        self.assertEqual(token, None)
