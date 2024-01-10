#Rules for the Algorithm
import random
#each person must be assigned a random target

id_assigner = 0

dict_of_checkers = {}
players = {}
#gives unique player ids
def new_id():
    global id_assigner
    id_assigner += 1
    return id_assigner

names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Isabella", "Sophia", "Jackson", "Mia", "Lucas", 
                "Harper", "Ethan", "Aiden", "Amelia", "Caden", "Charlotte", "Henry", "Ella", "Alexander", 
                "Sebastian", "Grace", "Benjamin", "Avery", "Scarlett", "Daniel", "Madison", "Aria", "David", 
                "Evelyn", "Michael"]

target_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Isabella", "Sophia", "Jackson", "Mia", "Lucas", 
                "Harper", "Ethan", "Aiden", "Amelia", "Caden", "Charlotte", "Henry", "Ella", "Alexander", 
                "Sebastian", "Grace", "Benjamin", "Avery", "Scarlett", "Daniel", "Madison", "Aria", "David", 
                "Evelyn", "Michael"]

    
class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.target = None
        self.is_alive = True
        self.kills = 0
    
    def set_target(self, target):
        self.target = target
    
    def get_killed(self):
        if not self.id in dict_of_checkers:
            dict_of_checkers[self.id] = Checker(self)
        
        dict_of_checkers[self.id].target_confirm()

        if dict_of_checkers[self.id].checking:
            self.is_alive = False

    
    #randomly chooses an alive player as target
    def new_target(self):
        alive_players = [player for player in players.values() if player.is_alive]
        if alive_players:
            return random.choice(alive_players)
        else:
            print("You win!")

    def kill_target(self):
        if not self.target.id in dict_of_checkers:
            dict_of_checkers[self.target.id] = Checker(self.target)
        
        dict_of_checkers[self.target.id].killer_confirm()

        if dict_of_checkers[self.target.id].checking():
            self.target = self.new_target()
            self.kills += 1
            
        

class Checker:
    def __init__(self, target, killer=None):
        self.target = target
        self.target_id = target.id
        self.killer = killer
        self.confirmations = 0
        self.target_confirmed = False
        self.killer_confirmed = False
    
    def target_confirm(self):
        if not self.target_confirmed:
            self.confirmations += 1
            self.target_confirmed = True
            self.checking()
    
    def killer_confirm(self):
        if not self.killer_confirmed:
            self.confirmations += 1
            self.killer_confirmed = True
            self.checking()
    
    #this would be run every time the page loads for a user in actuality
    def checking(self):
        if self.confirmations == 2:
            return True
        return False
            


while True:
    temp_name = random.choice(names)
    names.remove(temp_name)
    

    id = new_id()
    players[id] = Player(temp_name, id)

    if len(names) == 0:
        break
#make it a chain!
available_targets = list(players.keys())

random.shuffle(available_targets)

for idx, player_id in enumerate(available_targets):
    if player_id != available_targets[-1]:
        players[player_id].set_target(players[available_targets[idx + 1]])
        print(f"{players[player_id].name} is hunting {players[available_targets[idx + 1]].name}")
        continue

    players[player_id].set_target(players[available_targets[0]])
    print(f"{players[player_id].name} is hunting {players[available_targets[0]].name}")
    print("Everything done")
    

"""
print(f"The name of the player at id 5 is {players[5].name}")
print(f"Their target is {players[5].target.name}, their id is: {players[5].target.id}")
print("Now we are going to kill that target")
players[players[5].target.id].get_killed()
players[5].kill_target()
print(f"Now the kill count is {players[5].kills} and their new target is {players[5].target.name}")
"""
    

