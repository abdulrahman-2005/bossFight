import random
from engine import Engine, ACTIONS

random_names = ["lofy", "hikaru", "fancify", "sniper", "lucifer", "majid", "dffg", "kilogram", "Newtown", "ronaldo", "karmastav", "jerk", "horror", "the 1", "the 2", "the 3"]
def create_random_slug():
    return random.choice(random_names) + "_" + str(random.randint(0, 1000))

class m:
    def __init__(self, health, attack, defense, luck):
        lucky = random.random() * (luck/100)
        self.luck = lucky
        self.health = health*(1+lucky)
        self.attack = attack*(1+lucky)
        self.defense = defense*(1+lucky)
        self.name = create_random_slug()
    
    
    def display(self):
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Luck: {self.luck}")
    
    def get_data(self):
        return [self.name, self.health, self.attack, self.defense, self.luck]

class Dead:
    def __init__(self, dead_player):
        self.name = dead_player.name
        self.health = 0
        self.attack = 0
        self.defense = 0
        self.luck = 0
    
class Player(m):
    def __init__(self, health, attack, defense, luck, name="Player",engine_type="random_pick"):
        super().__init__(health, attack, defense, luck)
        self.engine = None
        self.engine_type = engine_type
        self.name = name
    
    def enter_game(self, game):
        self.game = game
        self.engine = self.game.ENGINE.get(self.engine_type)

    def action(self):
        if self.engine == None:
            action = random.choice(ACTIONS)
        else:
            action = self.engine(self)

        if action == "attack":
            stage = {
                "name": "Attack",
                "description": f"{self.name} [Attacking]",
                "amount": self.attack
            }
        elif action == "defense":
            stage = {
                "name": "Defense",
                "description": f"{self.name} [Defending]",
                "amount": self.defense
            }
        elif action == "upgrade":
            stage = {
                "name": "Upgrade",
                "description": f"{self.name} [Upgrading]",
                "amount": self.luck
            }
        self.game.stage[self.name] = stage