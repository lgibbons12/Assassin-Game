# users/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import Player, Checker
from users.game import GameManager

class GameTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Create a player instance for the test user
        self.player = Player.objects.create(user=self.user)

    def test_home_view(self):
        # Test the home view
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home Page')

    def test_assignment_view(self):
        # Test the assignment view
        response = self.client.get(reverse('assignment'))
        self.assertEqual(response.status_code, 302)  # Redirect to login since user not authenticated

        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('assignment'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Assignment Page')

    '''
    def test_new_target_game_logic(self):
        # Test the new_target game logic
        target_player = Player.objects.create(user=get_user_model().objects.create_user(username='targetuser'))
        GameManager.new_target(self.player, target_player)
        self.assertEqual(self.player.target_pk, target_player.pk)
    '''

    # Add more test methods as needed for other views and game logic
