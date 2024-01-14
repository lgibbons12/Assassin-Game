import json
import os
import random
from .models import Player, Checker

class GameManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TARGETS_JSON_PATH = os.path.join(BASE_DIR, 'static', 'users', 'targets.json')

    @staticmethod
    def win_condition():
        living_players = Player.objects.filter(is_dead=False, is_playing=True)

        if living_players.count() == 1:
            winner = living_players.get()
            winner.is_winner = True
            winner.save()
            return True
        
        return False
            
         
    @staticmethod
    def new_target(player, target_killed):
        print("i was called")
        if GameManager.win_condition():
            return
        
        
        # Retrieve the existing target list
        target_list = GameManager._load_targets()

        if target_list:
            # Remove the target_killed from the list
            pk_to_remove = target_killed.pk
            if not pk_to_remove in target_list:
                return
            index_to_delete = target_list.index(pk_to_remove)
            try:
                next_target_player = Player.objects.get(pk=target_list[index_to_delete + 1])
            except IndexError:
                next_target_player = Player.objects.get(pk=target_list[0])
            player.set_target(next_target_player)
            player.in_waiting = False
            player.save()
            del target_list[index_to_delete]

            # Save the updated target list to the JSON file
            GameManager._save_targets(target_list)

    @staticmethod
    def assign_targets():
        Checker.objects.all().delete()
        for player_instance in Player.objects.all():
            # Set each field to its default value
            player_instance.is_dead = False
            player_instance.target_name = ''
            player_instance.target_pk = None
            player_instance.kills = 0
            player_instance.in_waiting = False
            
            player_instance.is_winner = False

            # Save the changes
            player_instance.save()
        

        available_targets = list(Player.objects.filter(is_playing=True, is_dead=False).values_list('id', flat=True))
        random.shuffle(available_targets)

        # Save the new list of targets to the JSON file
        GameManager._save_targets(available_targets)

        for idx, player_id in enumerate(available_targets):
            if player_id != available_targets[-1]:
                target_player = Player.objects.get(pk=available_targets[idx + 1])
            else:
                target_player = Player.objects.get(pk=available_targets[0])

            player_to_set = Player.objects.get(pk=available_targets[idx])
            player_to_set.set_target(target_player)
            player_to_set.save()

            print(f"{player_to_set.user.name}'s target is {target_player.user.name}")

    @staticmethod
    def _load_targets():
        try:
            with open(GameManager.TARGETS_JSON_PATH, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    @staticmethod
    def _save_targets(targets):
        os.makedirs(os.path.dirname(GameManager.TARGETS_JSON_PATH), exist_ok=True)
        with open(GameManager.TARGETS_JSON_PATH, 'w') as file:
            json.dump(targets, file)