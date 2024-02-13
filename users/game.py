import json
import os
import random
from .models import Player, Checker, AgentGroup
from django.db.models import F
spy_callsigns = [
    "Ace",
    "Agent",
    "Alpha",
    "Angel",
    "Apollo",
    "Archer",
    "Arrow",
    "Athena",
    "Atlas",
    "Aurora",
    "Banshee",
    "Baron",
    "Basilisk",
    "Bishop",
    "Blade",
    "Blaze",
    "Blitz",
    "Blizzard",
    "Bond",
    "Bravo",
    "Breeze",
    "Bullet",
    "Cain",
    "Calypso",
    "Cannon",
    "Capricorn",
    "Casper",
    "Castle",
    "Chaos",
    "Charlie",
    "Chase",
    "Checkmate",
    "Cheetah",
    "Cherry",
    "Cipher",
    "Claw",
    "Cobra",
    "Colt",
    "Comet",
    "Copper",
    "Crash",
    "Cricket",
    "Crow",
    "Cruise",
    "Crux",
    "Cyan",
    "Cyclops",
    "Dagger",
    "Daredevil",
    "Dash",
    "Delta",
    "Deuce",
    "Diamond",
    "Diva",
    "Doom",
    "Dragon",
    "Drake",
    "Dream",
    "Drift",
    "Echo",
    "Eclipse",
    "Edge",
    "Elixir",
    "Ember",
    "Enigma",
    "Eve",
    "Falcon",
    "Fang",
    "Fate",
    "Felix",
    "Fenix",
    "Finn",
    "Firefly",
    "Flame",
    "Flash",
    "Flint",
    "Flora",
    "Frost",
    "Fury",
    "Gale",
    "Gemini",
    "Ghost",
    "Glacier",
    "Glider",
    "Glow",
    "Gold",
    "Grace",
    "Griffin",
    "Grim",
    "Halo",
    "Hammer",
    "Harley",
    "Hawk",
    "Haze",
    "Helios",
    "Hercules",
    "Hex",
    "Honey",
    "Hunter",
    "Hydra",
    "Ice",
    "Indigo",
    "Inferno",
    "Iris",
    "Ivy",
    "Jade",
    "Jazz",
    "Jester",
    "Jet",
    "Jinx",
    "Joker",
    "Juno",
    "Justice",
    "Karma",
    "King",
    "Knight",
    "Laser",
    "Leo",
    "Libra",
    "Lightning",
    "Loki",
    "Lotus",
    "Lucky",
    "Luna",
    "Mace",
    "Mamba",
    "Mantis",
    "Marble",
    "Mars",
    "Matrix",
    "Max",
    "Maya",
    "Mercury",
    "Meteor",
    "Midnight",
    "Mist",
    "Mocha",
    "Moon",
    "Muse",
    "Nebula",
    "Neon",
    "Nero",
    "Nexus",
    "Nighthawk",
    "Nightmare",
    "Ninja",
    "Nova",
    "Omega",
    "Onyx",
    "Orion",
    "Oscar",
    "Ozone",
    "Panda",
    "Panther",
    "Phoenix",
    "Pilot",
    "Pixie",
    "Pluto",
    "Polaris",
    "Pulse",
    "Pyro",
    "Quartz",
    "Queen",
    "Racer",
    "Radar",
    "Rage",
    "Rain",
    "Ranger",
    "Raven",
    "Rebel",
    "Red",
    "Reed",
    "Reign",
    "Rex",
    "Ricochet",
    "Rider",
    "Ripley",
    "Riptide",
    "Rocket",
    "Rogue",
    "Romeo",
    "Rose",
    "Ruby",
    "Rush",
    "Saber",
    "Sage",
    "Sapphire",
    "Scorpio",
    "Scout",
    "Shadow",
    "Shark",
    "Silver",
    "Skylar",
    "Skyline",
    "Slash",
    "Slate",
    "Smokey",
    "Snake",
    "Snow",
    "Solo",
    "Sonic",
    "Spark",
    "Sparrow",
    "Spike",
    "Spirit",
    "Spitfire",
    "Splash",
    "Spring",
    "Star",
    "Steel",
    "Stella",
    "Sting",
    "Storm",
    "Striker",
    "Stryker",
    "Sugar",
    "Sun",
    "Surge",
    "Swift",
    "Switch",
    "Tango",
    "Taurus",
    "Tempest",
    "Terra",
    "Thor",
    "Thunder",
    "Tiger",
    "Titan",
    "Torch",
    "Tracer",
    "Trinity",
    "Trip",
    "Trixie",
    "Troy",
    "Turbo",
    "Twilight",
    "Typhoon",
    "Valkyrie",
    "Vapor",
    "Vega",
    "Venom",
    "Venus",
    "Vex",
    "Viper",
    "Virgo",
    "Vixen",
    "Volt",
    "Vortex",
    "Wasp",
    "Whisper",
    "Wild",
    "Wing",
    "Wolf",
    "Wraith",
    "X-Ray",
    "Zane",
    "Zara",
    "Zeus",
    "Ziggy",
    "Zion",
    "Zodiac",
    "Zoe",
    "Zone",
    "Zoom",
    "Zorro"
]

class GameManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TARGETS_JSON_PATH = os.path.join(BASE_DIR, 'static', 'users', 'targets.json')

    @staticmethod
    def win_condition():
        living_groups = AgentGroup.objects.filter(is_playing=True, is_out = False)

        if living_groups.count() == 1:
            winner = living_groups.get()
            winner.is_winner = True
            winner.save()
            return 1
        
        living_players = Player.objects.filter(is_dead=False, is_playing=True)

        if living_players.count() == 1:
            winner = living_players.get()
            winner.is_winner = True
            winner.save()
            return 2
        
        return 0
    
    @staticmethod
    def new_group_target(group, group_killed):
        if GameManager.win_condition() != 0:
            return
        

        target_list = GameManager._load_targets()

        if target_list:
            pk_to_remove = group_killed.pk
            try:
                index_to_delete = target_list.index(pk_to_remove)
            except:
                #GameManager._refresh_targets()
                return
            try:
                next_target_group = AgentGroup.objects.get(pk=target_list[index_to_delete + 1])
            except IndexError:
                next_target_group = AgentGroup.objects.get(pk=target_list[0])
            group.set_target(next_target_group)
            group.save()
            del target_list[index_to_delete]

            # Save the updated target list to the JSON file
            GameManager._save_targets(target_list)

    @staticmethod
    def new_target(player, target_killed):
        
        if GameManager.win_condition() != 0:
            return
        
        
        # Retrieve the existing target list
        target_list = GameManager._load_targets()

        if target_list:
            # Remove the target_killed from the list
            pk_to_remove = target_killed.pk
            try:
                index_to_delete = target_list.index(pk_to_remove)
            except:
                #GameManager._refresh_targets()
                #this is a big change i made that could mess things up
                return
            try:
                next_target_player = Player.objects.get(pk=target_list[index_to_delete + 1])
            except IndexError:
                next_target_player = Player.objects.get(pk=target_list[0])
            player.set_target(next_target_player)
            player.save()
            del target_list[index_to_delete]

            # Save the updated target list to the JSON file
            GameManager._save_targets(target_list)

            #GameManager._refresh_targets()
    

    @staticmethod
    def _refresh_targets():
         # Get all alive players
        alive_players = Player.objects.filter(is_playing=True, is_dead=False)

        # Get the target list
        target_list = GameManager._load_targets()

        # Create sets of target_pks and pks
        current_targets_set = set(target_list)
        alive_players_set = set(alive_players.values_list('pk', flat=True))

        

        def reset(t_list):
            # Assign targets sequentially
            for idx in t_list:
                player = Player.objects.get(pk=idx)
                if idx < len(t_list) - 1:
                    target_player = Player.objects.get(pk=t_list[idx + 1])
                else:
                    target_player = Player.objects.get(pk=t_list[0])

                player.set_target(target_player)
                player.save()

        if len(current_targets_set) == len(alive_players_set):
            # All alive players have a target, everything is okay
            return
        elif len(current_targets_set) > len(alive_players_set):
            # There are players without alive targets
            dead_pk_in_loop = current_targets_set - alive_players_set
            
            for dead_pk in dead_pk_in_loop:
                dead_player = Player.objects.get(pk=dead_pk)
                player = Player.objects.filter(target_pk=dead_pk).first()
                if player is not None:
                    GameManager.new_target(player, dead_player)
            
            #reset(target_list)

        elif len(current_targets_set) < len(alive_players_set):
            #there are more alive players than the current target set
            out_of_loop_pks = alive_players_set - current_targets_set

            for ool_pk in out_of_loop_pks:

                last_player = Player.objects.get(pk=target_list[-1])
                target_list.append(ool_pk)
                ool_player = Player.objects.get(pk=ool_pk)
                
                last_player.set_target(ool_player)
                ool_player.set_target(target_list[0])
                
            # Save the updated target list
            #reset(target_list)

        
        GameManager._save_targets(target_list)

           
    @staticmethod
    def assign_group_targets(new_game = True):
        if new_game:
            Checker.objects.all().delete()
        
            for player_instance in Player.objects.filter(is_playing=True):
                    # Set each field to its default value
                    player_instance.is_dead = False
                    player_instance.target_name = ''
                    player_instance.target_pk = None
                    player_instance.kills = 0
                    player_instance.in_waiting = False
                    player_instance.have_eliminated_today = False
                    player_instance.is_winner = False

                    # Save the changes
                    player_instance.save()
            for group_instance in AgentGroup.objects.all():
                group_instance.is_out = False
                group_instance.target_group_name = ''
                group_instance.target_group_pk = None
                group_instance.kills = 0
                group_instance.is_winner = False

        else:
            for player_instance in Player.objects.filter(is_playing=True, is_dead=False):
                player_instance.target_name = ''
                player_instance.target_pk = None
                player_instance.have_eliminated_today = False
                player_instance.in_waiting = False

                player_instance.save()
            
            for group_instance in AgentGroup.objects.filter(is_playing = True, is_out = False):
                group_instance.target_group_name = ''
                group_instance.target_group_pk = None
                

        available_targets = list(AgentGroup.objects.filter(is_playing=True, is_out = False).values_list('id', flat=True))
        random.shuffle(available_targets)
        

        GameManager._save_targets(available_targets)

        for idx, group_id in enumerate(available_targets):
            if group_id != available_targets[-1]:
                target_group = AgentGroup.objects.get(pk=available_targets[idx+1])
            else:
                target_group = AgentGroup.objects.get(pk=available_targets[0])

            group_to_set = AgentGroup.objects.get(pk=available_targets[idx])
            group_to_set.set_target(target_group)
            
            group_to_set.save()
    @staticmethod
    def assign_targets(new_game = True):
        for obj in AgentGroup.objects.all():
            obj.is_out = True
            obj.save()
        if new_game:
            Checker.objects.all().delete()
            for player_instance in Player.objects.filter(is_playing=True):
                # Set each field to its default value
                player_instance.is_dead = False
                player_instance.target_name = ''
                player_instance.target_pk = None
                player_instance.kills = 0
                player_instance.in_waiting = False
                player_instance.have_eliminated_today = False
                player_instance.is_winner = False

                # Save the changes
                player_instance.save()
        
        else:
            for player_instance in Player.objects.filter(is_playing=True, is_dead=False):
                player_instance.target_name = ''
                player_instance.target_pk = None
                player_instance.have_eliminated_today = False
                player_instance.in_waiting = False

                player_instance.save()
        

        available_targets = list(Player.objects.filter(is_playing=True, is_dead=False).values_list('id', flat=True))
        random.shuffle(available_targets)
        random.shuffle(spy_callsigns)

        # Save the new list of targets to the JSON file
        GameManager._save_targets(available_targets)

        for idx, player_id in enumerate(available_targets):
            if player_id != available_targets[-1]:
                target_player = Player.objects.get(pk=available_targets[idx + 1])
            else:
                target_player = Player.objects.get(pk=available_targets[0])

            player_to_set = Player.objects.get(pk=available_targets[idx])
            player_to_set.set_target(target_player)
            player_to_set.agent_selection(spy_callsigns[idx])
            player_to_set.save()

            

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