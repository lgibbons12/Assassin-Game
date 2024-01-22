import json
import os
import random
from .models import Player, Checker

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
            player.save()
            del target_list[index_to_delete]

            # Save the updated target list to the JSON file
            GameManager._save_targets(target_list)

    @staticmethod
    def assign_targets(new_game = True):
        Checker.objects.all().delete()
        if new_game:
            for player_instance in Player.objects.all():
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