from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestAuthentication(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.existing_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
        )

    def test_login_page_status_code(self):
        '''Verify that the login page loads successfully with a 200 OK status.'''

        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_signup_page_status_code(self):
        '''Verify that the signup page loads successfully with a 200 OK status.'''

        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_valid_signup_creates_new_user_and_redirects(self):
        '''Verify that a valid signup redirects, creates a new account and logs in the new user.'''

        new_user = {
            'username': 'new_testuser',
            'email': 'new_test@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
        }

        response = self.client.post(reverse('users:signup'), data=new_user)

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='new_testuser').exists())

        # Verify that user is logged in after a successful sign up
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, User.objects.get(username='new_testuser'))

    def test_invalid_signup_does_not_create_new_user(self):
        '''Verify that invalid signup doesn't create or login a new user and gives an error.'''

        new_user = {
            'username': 'new_testuser',
            'email': 'new_test@example.com',
            'password1': 'Password123!',
            'password2': 'Wrong_Password123!',
        }

        response = self.client.post(reverse('users:signup'), data=new_user)

        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

        self.assertFalse(User.objects.filter(username='new_testuser').exists())

        # Verify that no user is authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_valid_login_authenticates_the_user_and_redirects(self):
        '''Verify that user gets authenticated and redirected after a successful sign in.'''

        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }

        response = self.client.post(reverse('users:login'), login_data)

        self.assertRedirects(response, reverse('home'))

        # Verify that user is logged in after a successful sign in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, self.existing_user)

    def test_invalid_login_does_not_authenticate_the_user(self):
        '''Verify that user doesn't get authenticated after invalid login and form raises an error.'''

        login_data = {
            'username': 'not_existing_testuser',
            'password': 'password123'
        } 

        response = self.client.post(reverse('users:login'), login_data)

        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

        # Verify that the password was not served on the frontend
        self.assertNotIn('value="password123"', response.content.decode())

        # Verify that no user is authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_logs_the_user_out_and_redirects(self):
        '''Verify that user gets redirected and logged out after a signout.'''

        self.client.login(username = 'testuser', password = 'password123')

        response = self.client.post(reverse('users:logout'))
        self.assertRedirects(response, reverse('users:login'))

        # Verify that no user is authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_authenticated_user_is_redirected_from_login_page(self):
        '''Verify that authenticated user can't access login page'''

        self.client.login(username = 'testuser', password = 'password123')

        response = self.client.get(reverse('users:login'))

        self.assertRedirects(response, reverse('home'))

    def test_authenticated_user_is_redirected_from_signup_page(self):
        '''Verify that authenticated user can't access signup page'''

        self.client.login(username = 'testuser', password = 'password123')

        response = self.client.get(reverse('users:signup'))

        self.assertRedirects(response, reverse('home'))