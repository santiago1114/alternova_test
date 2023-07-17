from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from .models import Type, Genre, Stream
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class GenreViewSetTestCase(TestCase):
    URL_PATH = '/api/v1/genre/'
    def setUp(self):
        self.client = APIClient()
        # Create some initial objects for testing
        Genre.objects.create(name='Science fiction')
        Genre.objects.create(name='Comedy')
        Genre.objects.create(name='Romance')
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = AccessToken.for_user(self.user)
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def test_list_objects(self):
        response = self.client.get(self.URL_PATH, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Assuming two initial objects

    def test_retrieve_object(self):
        obj_id = Genre.objects.first().id
        response = self.client.get(f'{self.URL_PATH}{obj_id}/', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Comedy')

    def test_create_object(self):
        data = {'name': 'Drama'}
        response = self.client.post(self.URL_PATH, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 4)  # One more object should be created

    def test_update_object(self):
        obj_id = Genre.objects.first().id
        data = {'name': 'Action'}
        response = self.client.put(f'{self.URL_PATH}{obj_id}/', data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Action')
        self.assertEqual(Genre.objects.first().name, 'Action')

    def test_partial_update_object(self):
        obj_id = Genre.objects.first().id
        data = {'name': 'Action'}
        response = self.client.patch(f'{self.URL_PATH}{obj_id}/', data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Action')
        self.assertEqual(Genre.objects.first().name, 'Action')

    def test_delete_object(self):
        obj_id = Genre.objects.first().id
        response = self.client.delete(f'{self.URL_PATH}{obj_id}/', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 2)  # One object should be deleted


class TypeViewSetTestCase(TestCase):
    URL_PATH = '/api/v1/type/'
    def setUp(self):
        self.client = APIClient()
        # Create some initial objects for testing
        Type.objects.create(name='Movie')
        Type.objects.create(name='Serie')
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = AccessToken.for_user(self.user)
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def test_list_objects(self):
        response = self.client.get(self.URL_PATH, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming two initial objects

    def test_retrieve_object(self):
        obj_id = Type.objects.first().id
        response = self.client.get(f'{self.URL_PATH}{obj_id}/', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Movie')

    def test_create_object(self):
        data = {'name': 'Movie'}
        response = self.client.post(self.URL_PATH, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Type.objects.count(), 3)  # One more object should be created

    def test_update_object(self):
        obj_id = Type.objects.first().id
        data = {'name': 'Movies'}
        response = self.client.put(f'{self.URL_PATH}{obj_id}/', data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Movies')
        self.assertEqual(Type.objects.first().name, 'Movies')

    def test_partial_update_object(self):
        obj_id = Type.objects.first().id
        data = {'name': 'Movies'}
        response = self.client.patch(f'{self.URL_PATH}{obj_id}/', data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Movies')
        self.assertEqual(Type.objects.first().name, 'Movies')

    def test_delete_object(self):
        obj_id = Type.objects.first().id
        response = self.client.delete(f'{self.URL_PATH}{obj_id}/', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Type.objects.count(), 1)  # One object should be deleted
        

class StreamViewSetTestCase(TestCase):
    URL_PATH = '/api/v1/stream/'
    def setUp(self):
        self.client = APIClient()
        # Create type objects
        self.type1 = Type.objects.create(name='Movie')
        self.type2 = Type.objects.create(name='Serie')
        
        # Create genre objects
        self.genre1 = Genre.objects.create(name='Science fiction')
        self.genre2 = Genre.objects.create(name='Comedy')
        self.genre3 = Genre.objects.create(name='Drama')
        
        # Create some initial objects for testing
        Stream.objects.create(name='Matrix', genre=self.genre1, type=self.type1)
        Stream.objects.create(name='Click', genre=self.genre2, type=self.type1)
        Stream.objects.create(name='The Chosen', genre=self.genre3, type=self.type2)

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = AccessToken.for_user(self.user)
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def test_list_objects(self):
        response = self.client.get(self.URL_PATH, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)  # Assuming 3 initial objects

    def test_retrieve_object(self):
        obj_id = Stream.objects.first().id
        response = self.client.get(f'{self.URL_PATH}{obj_id}/', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Click')

    def test_create_object(self):
        genre_id = Genre.objects.get(name__startswith='Comedy').id
        type_id = Type.objects.get(name__startswith='Movie').id
        data = {'name': 'Shrek', 'genre': genre_id, 'type': type_id}
        response = self.client.post(self.URL_PATH, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stream.objects.count(), 4)  # One more object should be created

    def test_update_object(self):
        obj_id = Stream.objects.first().id
        genre_id = Genre.objects.get(name__startswith='Comedy').id
        type_id = Type.objects.get(name__startswith='Movie').id
        
        data = {'name': 'Shrek 2', 'genre': genre_id, 'type': type_id}
        response = self.client.put(f'{self.URL_PATH}{obj_id}/', data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Shrek 2')

    def test_partial_update_object(self):
        obj_id = Stream.objects.first().id
        genre_id = Genre.objects.get(name__startswith='Drama').id
        
        data = {'name': 'Shrek 2'}
        response = self.client.patch(f'{self.URL_PATH}{obj_id}/', data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Shrek 2')

    def test_delete_object(self):
        obj_id = Stream.objects.first().id
        response = self.client.delete(f'{self.URL_PATH}{obj_id}/', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Stream.objects.count(), 2)  # One object should be deleted