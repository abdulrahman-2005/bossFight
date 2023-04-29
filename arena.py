from engine import *
from tabulate import tabulate
from competetor import Player, Dead
import json
from plotter import plotter

class Arena:
    def __init__(self, players):
        self.players = players
        self.turn = 1
        self.ended = False
        self.logs = []
        self.stage = {}
        self.players_amount = len(self.players)
        self.players_copy = self.players[:]
        self.turns = []
        self.helthes = []
        self.attacks = []
        self.defenses = []
        self.lucks = []
        self.names = [player.name for player in self.players]
        
        self.ENGINE = Engine(self)
        for player in self.players:
            player.enter_game(self)
        self.display()

    def display(self):
        self.players_data = []
        for player in self.players:
            self.players_data.append(player.get_data())
        print(tabulate(self.players_data, headers=["Name", "Health", "Attack", "Defense", "Luck"], tablefmt="easy"))
        print()
    def next_turn(self):
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
        
        self.logs.append( { "turn": self.turn, **self.stage } )

        for i in self.stage:
            print(f"{i}: {self.stage[i]['description']}")
        
        for player in self.players:
            if self.stage[player.name]["name"] == "Attack":
                for player2 in self.players:
                    if player2.name != player.name:
                        player2.health -= self.stage[player.name]["amount"]/2
            elif self.stage[player.name]["name"] == "Defense":
                player.health += self.stage[player.name]["amount"]
            elif self.stage[player.name]["name"] == "Upgrade":
                player.luck += (player.luck *self.stage[player.name]["amount"])/1000
                player.defense += self.stage[player.name]["amount"] * player.defense
                player.attack += self.stage[player.name]["amount"] * player.attack

        for player in self.players:
            if player.health <= 0:
                print(f"{player.name} died")
                self.players_copy[self.players_copy.index(player)] = Dead(player)
                self.players.remove(player)
        
        if len(self.players) == 1:
            print(f"{self.players[0].name} won")
            self.ended = True
            self.winner = self.players[0]

    def game_loop(self):
        while not self.ended:
            # sleep(1)
            self.next_turn()
            self.display()
            
            for i in range(self.players_amount):
                self.turns.append(self.turn)
                self.helthes.append([player.health for player in self.players_copy])
                self.attacks.append([player.attack for player in self.players_copy])
                self.defenses.append([player.defense for player in self.players_copy])
                self.lucks.append([player.luck for player in self.players_copy])


        print("Game ended")
        with open("hist.json", "w") as f:
            json.dump({
                "names": self.names,
                "turns": self.turns,
                "health": self.helthes,
                "attack": self.attacks,
                "defense": self.defenses,
                "luck": self.lucks
            }, f)
        for log in self.logs:
            print(f"------------------- Turn {log['turn']} -------------------")
            for i in log:
                if i != "turn":
                    print(f"{i}: {log[i]['description']}")

if __name__ == '__main__':
    players = []
    for i in range(3):
        players.append(Player(200, 10, 10, 10, "smart"))
    arena = Arena(players)
    arena.game_loop()
