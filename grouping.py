class Group:
    def __init__(self, name):
        self.name = name
        self.players = []
    
    def add_player(self, player_name, dicty):
        if player_name in list(dicty.keys()):
            self.players.append(dicty[player_name])
        else:
            raise ValueError("Player does not exist")
    
    def __str__(self):
        x = f"Group {self.name}"
        for player in self.players:
            x += f"\n Player: {player.name}"
        return x
    
names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Isabella", "Sophia", "Jackson", "Mia", "Lucas", 
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

players = {}
for i in range(len(names)):
    players[names[i]] = Player(names[i], i)


shaky = Group("Shaky")
shaky.add_player("Liam", players)
shaky.add_player("Ava", players)

print(shaky)