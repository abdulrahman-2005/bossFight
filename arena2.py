from numpy import average
from engine import Engine, ACTIONS
from tabulate import tabulate
from competetor import Player, Dead
from time import sleep
import random


#TODO player names be [Player]

def get_random_except(players, player):
    while True:
        player_num = players.index(player)
        num = random.randint(0, len(players)-1)
        if num != player_num:
            return num

class Arena:
    def __init__(self, players, wave_freq=11, state="disturputer"):
        self.players = players
        self.wave_freq = int(wave_freq)
        self.turn = 0
        self.ended = False
        self.logs = []
        self.stage = {}
        self.players_amount = len(self.players)
        self.current_players = self.players_amount
        self.players_copy = self.players[:]
        self.delay = True
        self.state = state
        if "user_input" in [player.engine_type for player in self.players]:
            self.delay = False
        self.ENGINE = Engine(self)
        for player in self.players:
            player.enter_game(self)
        self.display()
        print("\n\nBattle Startes...\n---------------\n")
        sleep(2)

    def display(self):
        self.players_data = [player.get_data() for player in self.players]
        print(tabulate(self.players_data, headers=[
              "Name", "Health", "Attack", "Defense", "Luck"], tablefmt="easy"))
        print()

    def next_turn(self):  # sourcery skip: low-code-quality
        self.turn += 1
        self.stage = {}
        # self.player.action()
        # self.boss.action()
        # self.logs.append({
        #     "turn": self.turn,
        #     self.player.name: self.stage[self.player.name]["description"],
        #     self.boss.name: self.stage[self.boss.name]["description"]
        # })
        for player in self.players:
            player.action()

        self.logs.append({"turn": self.turn, **self.stage})

        for value in self.stage.values():
            print(f"{value['description']}")

        for player in self.players:
            if self.stage[player.name]["name"] == "Attack":
                if self.state == "randomizer":
                    self.players[get_random_except(self.players, player)].health -= self.stage[player.name]["amount"]
                else:
                    for player2 in self.players:
                        if player2.name != player.name:
                            player2.health -= self.stage[player.name]["amount"]/(len(self.players)-1)

            elif self.stage[player.name]["name"] == "Defense":
                player.health += self.stage[player.name]["amount"]
            elif self.stage[player.name]["name"] == "Upgrade":
                player.luck += (player.luck *
                                self.stage[player.name]["amount"])/1000
                player.defense += self.stage[player.name]["amount"] * \
                            player.defense
                player.attack += self.stage[player.name]["amount"] * \
                            player.attack
        if self.turn % self.wave_freq == 0:
            print("Wave...")
            for player in self.players:
                if random.random() > .5:
                    try:
                        player.health -= random.randint(1, int(player.health/10))
                    except:
                        pass
                if random.random() > .5:
                    try:
                        player.attack -= random.randint(1, int(player.attack/10))
                    except:
                        pass
                if random.random() > .5:
                    try:
                        player.luck *= .8
                    except Exception:
                        pass
                if random.random() > .5:
                    try:
                        player.defense -= random.randint(1, int(player.defense/10))
                    except:
                        pass
        if self.turn % 15 == 0:
            self.players[random.randint(0, len(self.players)-1)].health = 0
        if self.turn % 50 == 0:
            average_health = average([player.health for player in self.players])
            average_attack = average([player.attack for player in self.players])
            average_defense = average([player.defense for player in self.players])
            average_luck = average([player.luck for player in self.players])
            for player in self.players:
                if player.health < average_health or player.attack < average_attack or player.defense < average_defense or player.luck < average_luck:
                    player.health = 0
                if player.luck < 0:
                    player.health = 0
        for player in self.players:
            if player.health <= 0:
                print(f"[{player.name}] died\n")
                self.players_copy[self.players_copy.index(
                    player)] = Dead(player)
                self.players.remove(player)
                self.current_players -= 1

        if len(self.players) == 1:
            print(f"[{self.players[0].name}] WON THE ARENA")
            self.ended = True
            self.winner = self.players[0]

    def game_loop(self):
        while not self.ended:
            self.next_turn()
            self.display()
            print(f"turn: {self.turn} || alive: {self.current_players}/{self.players_amount}")
            if self.delay:
                sleep(1)

        print("Game ended")

        # for log in self.logs:
        #     print(
        #         f"------------------- Turn {log['turn']} -------------------")
        #     for i in log:
        #         if i != "turn":
        #             print(f"{log[i]['description']}")


def main():
    options = """
  what would You do:
  1. play a dual (YOU vs AI)
  2. play a dual (YOU vs FRIEND) >> localy
  3. play in an arena full of AIs
  4. watch dual (AI vs AI)
  5. watch an arena fight (multiple AIs fight)
  """
    print(options)
    user_choice = input("your choice (1-5): ")
    if user_choice == "1":
        player = Player(100, 12, 12, 12, "user_input")
        level = input("how hard would you like the AI: (1-5): ")
        if level == "1":
            AI = Player(10, 10, 10, 10)
        elif level == "2":
            AI = Player(50, 10, 10, 10)
        elif level == "3":
            AI = Player(100, 10, 10, 15)
        elif level == "4":
            AI = Player(150, 10, 10, 15, "smart")
        elif level == "5":
            AI = Player(200, 25, 25, 5, "smart")
        game = Arena([AI, player])
        game.game_loop()
    elif user_choice == "2":
        p1 = Player(200, 20, 20, 20, "user_input")
        p2 = Player(200, 20, 20, 20, "user_input")
        game = Arena([p1, p2])
        game.game_loop()
    elif user_choice == "3":
        player = Player(200, 15, 15, 15, "user_input")
        am = input("how much AIs: (number)>> ")
        try:
            am = int(am)
            players = [player]
            players.extend(Player(150, 15, 15, 15, "smart") for _ in range(am))
            game = Arena(players)
            game.game_loop()
        except:
            print("Please pick a number")
    elif user_choice == "4":
        ai1 = Player(200, 30, 30, 10, "smart")
        ai2 = Player(200, 30, 30, 10, "smart")
        game = Arena([ai1, ai2])
        game.game_loop()
    elif user_choice == "5":
        am = input("how much AIs: (number)>> ")
        try:
            am = int(am)
            players = [Player(150, 15, 15, 15, "smart") for _ in range(am)]
            game = Arena(players, state="randomizer")
            game.game_loop()
        except Exception as e:
            print(e)
            print("Please pick a number")


if __name__ == "__main__":
    main()
