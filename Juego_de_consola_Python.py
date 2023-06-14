from pynput import keyboard
import os
import threading
import time
import random

WIDTH = 120
HEIGHT = 27
position = WIDTH // 2
running = True
ship = '|==^==|'
obstacles = []
enemies = []
player_projectiles = []
enemy_projectiles = []

def draw():
    global position, obstacles, enemies, player_projectiles, enemy_projectiles
    while running:
        os.system('cls')
        field = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

        for enemy in enemies:
            enemy_pos, enemy_ship = enemy
            for i, char in enumerate(enemy_ship):
                field[0][enemy_pos + i] = char

        for projectile in player_projectiles:
            x, y = projectile
            field[y][x] = '^'

        for projectile in enemy_projectiles:
            x, y = projectile
            field[y][x] = '*'

        for obstacle in obstacles:
            x, y = obstacle
            field[y][x] = 'X'

        for i, char in enumerate(ship):
            field[HEIGHT-1][position + i] = char

        for row in field:
            print(''.join(row))

        time.sleep(0.1)

def on_press(key):
    global position, player_projectiles
    if key == keyboard.Key.left and position > 1:
        position -= 2
    elif key == keyboard.Key.right and position < WIDTH - len(ship) - 1:
        position += 2
    elif key == keyboard.Key.space:
        player_projectiles.append([position + len(ship) // 2, HEIGHT - 2])
    elif key == keyboard.Key.esc:
        global running
        running = False

listener = keyboard.Listener(on_press=on_press)
listener.start()

draw_thread = threading.Thread(target=draw)
draw_thread.start()

start_time = time.time()

while running:
    current_time = time.time()

    if random.random() < 0.3:
        obstacles.append([random.randint(0, WIDTH-1), 0])

    for obstacle in obstacles:
        obstacle[1] += 1

        if obstacle[1] == HEIGHT - 1 and position <= obstacle[0] < position + len(ship):
            running = False
    obstacles = [obstacle for obstacle in obstacles if obstacle[1] < HEIGHT]

    for enemy in enemies:
        enemy_pos, _ = enemy
        if enemy_pos < position:
            enemy_pos += 2
        elif enemy_pos > position:
            enemy_pos -= 2

        if random.random() < 0.1:
            enemy_projectiles.append([enemy_pos + len(ship) // 2, 1])

        enemy[0] = enemy_pos

    for projectile in player_projectiles:
        projectile[1] -= 1

        for enemy in enemies:
            enemy_pos, enemy_ship = enemy
            if (
                [projectile[0], projectile[1] + 1] in enemy_projectiles and
                enemy_pos <= projectile[0] < enemy_pos + len(enemy_ship)
            ):
                player_projectiles.remove(projectile)
                enemies.remove(enemy)
                break

    player_projectiles = [projectile for projectile in player_projectiles if projectile[1] >= 0]

    for projectile in enemy_projectiles:
        projectile[1] += 1

        if (
            projectile[1] == HEIGHT - 1 and
            position <= projectile[0] < position + len(ship)
        ):
            running = False

    enemy_projectiles = [projectile for projectile in enemy_projectiles if projectile[1] < HEIGHT]

    if current_time - start_time >= 5:
        if len(enemies) == 0:
            enemies.append([0, '|===|'])
        elif len(enemies) == 1:
            enemies.append([0, '|===|'])
        elif len(enemies) == 2:
            enemies.append([WIDTH - len(ship), '|===|'])

    time.sleep(0.1)

total_time = int(current_time - start_time)
print(f"\nJuego terminado. Puntaje total: {total_time}.")
