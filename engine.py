import random

ACTIONS = ["attack", "defense", "upgrade"]


class Engine:
    def __init__(self, game):
        self.game = game
        self.engines = {
            "random_pick": self.random_pick,
            "user_input": self.user_input,
            "smart": self.smart_pick
        }
    def user_input(self, player):
        print(f"What do you want to do? [{player.name}]")
        print("1. Attack")
        print("2. Defense")
        print("3. upgrade")
        while True:
            try:
                action = int(input("Enter your choice: "))
                return ACTIONS[action - 1]
            except Exception:
                print("Invalid input")
                continue
        

    def random_pick(self, player):
        print("random pick")
        return random.choice(ACTIONS)

    def smart_pick(self, player):
        players_copy = self.game.players[:]
        players_copy.remove(player)

        health_total = 0
        attack_total = 0
        defense_total = 0

        for player in players_copy:
            health_total += player.health
            attack_total += player.attack
            defense_total += player.defense
        length = len(players_copy)
        health_avg = health_total / length
        attack_avg = attack_total / length
        defense_avg = defense_total / length

        if player.health >= health_avg:
            return "attack"
        elif player.health <= attack_avg:
            return "defense"
        elif player.attack <= defense_avg:
            return "upgrade"
        elif player.health <= health_avg/2:
            return "defense"
        elif player.attack <= attack_avg:
            return "upgrade"
        elif player.health > health_avg:
            return "attack"
        else:
            return "upgrade"
        


    def get(self, engine_type: str):
        try:
            return self.engines[engine_type]
        except KeyError as e:
            raise ValueError("Engine type not found") from e
