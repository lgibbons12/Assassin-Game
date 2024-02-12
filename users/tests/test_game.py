# users/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import Player, Checker, CustomUser
from users.game import GameManager
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Player, Checker  # Import your Player and Checker models
import random
import json
class YourAppTestCase(TestCase):
    def setUp(self):
        self.players = []

        for i in range(1, 11):
            # Try to get an existing user or create a new one
            user, created = get_user_model().objects.get_or_create(
                username=f'testuser{i}',
                defaults={
                    'password': f'testpassword{i}',
                    'first_name': f'John{i}',
                    'last_name': f'Doe{i}',
                }
            )

            # Try to get an existing player or create a new one
            player, player_created = Player.objects.get_or_create(user=user)

            # Append the player to the list
            self.players.append(player)

    def test_assign_targets(self):
        GameManager().assign_targets()
        # Initial targets.json content
        initial_targets = GameManager._load_targets()

        for _ in range(10):
            # Run assign_targets with new_game=False
            GameManager.assign_targets(new_game=False)

            # Updated targets.json content
            updated_targets = GameManager._load_targets()

            # Check if both lists have the same elements
            self.assertCountEqual(initial_targets, updated_targets)

        # You can also check specific positions if needed
        # self.assertEqual(initial_targets[0], updated_targets[1])

        # Additional assertions or checks as needed
        # ...

        # Clean up any changes made during the test
        

        # Reset the players if needed
       

        # Additional cleanup steps if needed
        # ...

    def test_follow_through(self):
        GameManager().assign_targets()

        while len(Player.objects.filter(is_dead=False, is_playing=True)) > 1:
            player = random.choice(Player.objects.filter(is_dead=False, is_playing=True))
            target = Player.objects.get(pk=player.target_pk)
            
            player.kill_target()
            target.get_killed()

            target_checkers = Checker.objects.filter(confirmations=2, action_performed=False)

            for checker in target_checkers:
                checker.checking()
        
        self.assertTrue(GameManager.win_condition())
        
    
    def test_with_discovery(self):
        GameManager().assign_targets()
        thing = 0
        while len(Player.objects.filter(is_dead=False, is_playing=True)) > 1:
            player = random.choice(Player.objects.filter(is_dead=False, is_playing=True))
            if thing % 4 == 0:
                player.discovered()
            else:
                player = random.choice(Player.objects.filter(is_dead=False, is_playing=True))

                target = Player.objects.get(pk=player.target_pk)
                if target.is_dead:
                    GameManager().new_target(player, target)
                    target = Player.objects.get(pk=player.target_pk)
                player.kill_target()
                target.get_killed()

                target_checkers = Checker.objects.filter(confirmations=2, action_performed=False)

                for checker in target_checkers:
                    checker.checking()
            
            thing += 1
        
        self.assertTrue(GameManager.win_condition())
        

    def test_with_self_defense(self):
        GameManager().assign_targets()

        

        while len(Player.objects.filter(is_dead = False, is_playing=True)) > 1:
            player = random.choice(Player.objects.filter(is_dead = False, is_playing = True))
            
            self_defensed = Player.objects.filter(is_dead=False, target_pk = player.pk).first()
            # Check if target player exists and is alive
            if self_defensed is None or self_defensed.is_dead:
                GameManager()._refresh_targets()
                continue  # Restart the loop to get a valid target player
        

            player.self_defense_killed()
            self_defensed.self_defense_died()
            target_checkers = Checker.objects.filter(confirmations=2, action_performed=False)

            for checker in target_checkers:
                checker.checking()
        
        self.assertTrue(GameManager().win_condition())
        

        
    # Add more test methods as needed for other views and game logic
