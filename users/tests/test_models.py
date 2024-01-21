from django.test import TestCase
from users.models import CustomUser, Player, Checker
from django.contrib.auth import get_user_model
from users.game import GameManager

class PlayerModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )

    def test_player_creation(self):
        # Check if a Player instance is created when a new user is created
        self.assertEqual(Player.objects.count(), 1)
        player = Player.objects.get(user=self.user)
        self.assertEqual(player.is_dead, False)
        self.assertEqual(player.target_name, '')
        self.assertEqual(player.target_pk, None)
        self.assertEqual(player.agent_name, None)
        self.assertEqual(player.kills, 0)
        self.assertEqual(player.is_playing, True)
        self.assertEqual(player.is_winner, False)
        self.assertEqual(player.in_waiting, False)

    def test_checker_creation(self):
        # Check if a Checker instance is created when a player is killed
        player = Player.objects.get(user=self.user)
        player.get_killed()

        self.assertEqual(Checker.objects.count(), 1)
        checker = Checker.objects.get(target=player)
        self.assertEqual(checker.killer, None)
        self.assertEqual(checker.confirmations, 1)
        self.assertEqual(checker.target_confirmed, True)
        self.assertEqual(checker.killer_confirmed, False)
        self.assertEqual(checker.action_performed, False)

    def test_checker_checking(self):
        # Check the checking method of Checker
        player1 = Player.objects.get(user=self.user)

        # Create another user
        user2 = get_user_model().objects.create_user(
            username='testuser2',
            password='testpassword',
            first_name='Jane',
            last_name='Doe'
        )
        player2 = Player.objects.get(user=user2)

        # Set up Checker instances
        checker1 = Checker.objects.create(target=player1)
        checker2 = Checker.objects.create(target=player2, killer=player1, target_confirmed=True, killer_confirmed=True)

        # Call the checking method
        gm = GameManager()  # You might need to adjust this if GameManager needs initialization
        result = checker2.checking()

        # Check the result and updated states
        self.assertEqual(result, True)
        self.assertEqual(player1.is_dead, True)
        self.assertEqual(player1.in_waiting, False)
        self.assertEqual(player1.kills, 1)
        self.assertEqual(player2.is_dead, False)
        self.assertEqual(player2.in_waiting, False)
        self.assertEqual(player2.kills, 0)

        # Check if new targets are assigned
        self.assertNotEqual(player1.target_pk, player2.pk)
        self.assertNotEqual(player2.target_pk, player1.pk)
