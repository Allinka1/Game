from exceptions import EnemyDown, GameOver
from models import Player, Enemy
import settings


def play():
    name = input('Please enter your name: ')
    player = Player(name)
    enemy = Enemy(1)

    while True:
        command = input('Type "start" to start game or "help" to see all commands: ').lower()
        if command not in settings.ALLOWED_COMMANDS:
            continue
        elif command == 'help':
            print(f'Allowed commands: {settings.ALLOWED_COMMANDS}')
            continue
        elif command == 'exit':
            break
        elif command == 'show scores':
            file = open('./scores.txt', 'r')
            for line in file:
                print(line)
            file.close()
            continue

        while True:
            try:
                player.attack(enemy)
                player.defence(enemy)
            except EnemyDown:
                print(f'Your lives: {player.lives} | '
                      f'Enemy lives: {enemy.lives} | '
                      f'Enemy level: {enemy.level}')
                print('*' * 50)
                enemy = Enemy(enemy.level + 1)
                player.score += 5
            except ValueError:
                continue


if __name__ == '__main__':
    try:
        play()
    except GameOver:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        print("Good bye!")
