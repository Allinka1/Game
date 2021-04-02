from datetime import datetime
from random import randint

from exceptions import EnemyDown, GameOver
import settings


class Enemy:

    def __init__(self, level):
        self.level = level
        self.lives = level

    @staticmethod
    def select_attack():
        return randint(1, 3)

    def decrease_lives(self):
        self.lives -= 1
        if self.lives == 0:
            raise EnemyDown


class Player:

    def __init__(self, name):
        self.name = name
        self.lives = settings.LIVES
        self.score = 0
        self.allowed_attacks = settings.ALLOWED_ATTACKS

    @staticmethod
    def fight(attack, defence):
        if attack == 1 and defence == 2 or attack == 2 and defence == 3:
            return 1
        elif attack == defence:
            return 0
        else:
            return -1

    @staticmethod
    def sort_score():
        result = []
        file = open('./scores.txt', 'r')
        for line in file:
            result.append(line.split('|'))
        file.close()
        result.sort(key=lambda i: i[2], reverse=True)
        file = open('./scores.txt', 'w')
        for item in result:
            if (result.index(item) + 1) <= 10:
                item[0] = str(result.index(item) + 1)
                file.write("|".join(item))
        file.close()

    def decrease_lives(self):
        self.lives -= 1
        if self.lives == 0:
            print('Enemy win! :(')
            print(f'Your score is {self.score}')
            file = open('./scores.txt', 'a')
            file.write(f'0 | {self.name} | {self.score} | {datetime.today()} \n')
            file.close()
            self.sort_score()
            raise GameOver

    @staticmethod
    def show_statistics(player, enemy):
        print(f'Your lives: {player.lives} | '
              f'Enemy lives: {enemy.lives} | '
              f'Enemy level: {enemy.level}')
        print('_' * 50)

    @staticmethod
    def validate_attack(user_value):
        if user_value > 3 or user_value < 1:
            raise ValueError

    def attack(self, enemy_obj):
        attack = int(input(
            'Choose a character for attack: 1 - wizard, 2 - warrior, 3 - robber.'
            ' Please enter the number of the character you have chosen: '))
        self.validate_attack(attack)
        result = self.fight(attack, enemy_obj.select_attack())
        if result == 0:
            print("It's a draw!")
        elif result == 1:
            print("You attacked successfully!")
            enemy_obj.decrease_lives()
            self.score += 1
        else:
            print("You missed!")
        self.show_statistics(self, enemy_obj)

    def defence(self, enemy_obj):
        attack = int(input(
            'Choose a character for defence: 1 - wizard, 2 - warrior, 3 - robber.'
            ' Please enter the number of the character you have chosen: '))
        self.validate_attack(attack)
        result = self.fight(enemy_obj.select_attack(), attack)
        if result == 0:
            print("It's a draw!")
        elif result == 1:
            print("Enemy attacked successfully!")
            self.decrease_lives()
            self.score -= 1
        else:
            print("Enemy missed!")
        self.show_statistics(self, enemy_obj)
