# game_manager.py
import random
from .models import Player, Target_List

class GameManager:
    @staticmethod
    def new_target(player, target_killed):
        # Retrieve the existing target list
        target_list = Target_List.objects.first()

        if target_list:
            # Remove the target_killed from the list
            target_list.target_list.remove(target_killed)
            target_list.save()

            # Get the next target from the modified list
            if target_list.target_list:
                next_target_pk = target_list.target_list[0]
                next_target_player = Player.objects.get(pk=next_target_pk)
                player.set_target(next_target_player)
                

        

    @staticmethod
    def assign_targets():
        available_targets = list(Player.objects.filter(is_playing=True, is_dead=False).values_list('id', flat=True))
        random.shuffle(available_targets)

        obs = Target_List.objects.all()
        obs.delete()
        new_list = Target_List(available_targets)
        new_list.save()

        for idx, player_id in enumerate(available_targets):
            if player_id != available_targets[-1]:
                target_player = Player.objects.get(pk=available_targets[idx + 1])
            else:
                target_player = Player.objects.get(pk=available_targets[0])
            
            Player.objects.get(pk=available_targets[idx]).set_target(target_player)


