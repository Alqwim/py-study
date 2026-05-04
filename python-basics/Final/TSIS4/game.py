# game.py
import pygame
import random
import json
import os
from config import WIDTH, HEIGHT, BLOCK_SIZE

class Game:
    def __init__(self):
        self.settings = {
            "snake_color": [0, 255, 0],
            "grid": True,
            "sound": True
        }
        self.load_settings()
        self.reset_game()

    def load_settings(self):
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.settings["snake_color"] = data.get("snake_color", [0, 255, 0])
                        self.settings["grid"] = data.get("grid", True)
                        self.settings["sound"] = data.get("sound", True)
            except:
                self.save_settings()

    def save_settings(self):
        try:
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f)
        except:
            pass

    def reset_game(self):
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.score = 0
        self.level = 1
        self.obstacles = []
        self.food = self.spawn_item()
        self.poison = self.spawn_item()
        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0
        self.active_powerup = None
        self.powerup_end_time = 0
        self.has_shield = False
        self.base_speed = 10

    def spawn_item(self):
        while True:
            x = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            if [x, y] not in self.snake and [x, y] not in self.obstacles:
                return [x, y]

    def generate_obstacles(self):
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level * 2):
                obs = self.spawn_item()
                if abs(obs[0] - self.snake[0][0]) > BLOCK_SIZE * 3:
                    self.obstacles.append(obs)

    def get_auto_turn_pos(self):
        """Вычисляет новую позицию головы при автоповороте"""
        head = self.snake[0]
        # Если шли по горизонтали, пытаемся повернуть по вертикали
        if self.direction in ["LEFT", "RIGHT"]:
            new_head_up = [head[0], head[1] - BLOCK_SIZE]
            if new_head_up[1] >= 0 and new_head_up not in self.obstacles and new_head_up not in self.snake:
                self.direction = "UP"
                return new_head_up
            else:
                self.direction = "DOWN"
                return [head[0], head[1] + BLOCK_SIZE]
        
        # Если шли по вертикали, пытаемся повернуть по горизонтали
        else:
            new_head_right = [head[0] + BLOCK_SIZE, head[1]]
            if new_head_right[0] < WIDTH and new_head_right not in self.obstacles and new_head_right not in self.snake:
                self.direction = "RIGHT"
                return new_head_right
            else:
                self.direction = "LEFT"
                return [head[0] - BLOCK_SIZE, head[1]]

    def update(self):
        now = pygame.time.get_ticks()

        # Таймеры бонусов
        if self.powerup and (now - self.powerup_spawn_time > 8000):
            self.powerup = None
        if not self.powerup and not self.active_powerup and random.random() < 0.01:
            self.powerup = self.spawn_item()
            self.powerup_type = random.choice(["SPEED", "SLOW", "SHIELD"])
            self.powerup_spawn_time = now
        if self.active_powerup and now > self.powerup_end_time:
            self.active_powerup = None

        # Рассчитываем обычный шаг головы
        head = list(self.snake[0])
        if self.direction == "UP": head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN": head[1] += BLOCK_SIZE
        elif self.direction == "LEFT": head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT": head[0] += BLOCK_SIZE

        # Проверка на столкновение
        hit_wall = head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT
        hit_self = head in self.snake
        hit_obs = head in self.obstacles

        # Если есть щит и произошло столкновение (стена или хвост)
        if (hit_wall or hit_self) and self.has_shield:
            self.has_shield = False
            head = self.get_auto_turn_pos() # Меняем направление и голову мгновенно

        # Если щит налетает на препятствие — ломаем его
        elif hit_obs and self.has_shield:
            self.has_shield = False
            self.obstacles.remove(head)
            # Продолжаем движение (голова остается прежней)

        # Если щита нет и мы врезались — конец игры
        elif hit_wall or hit_self or hit_obs:
            return False

        # Двигаем змейку
        self.snake.insert(0, head)

        # Проверка еды
        if head == self.food:
            self.score += 10
            self.food = self.spawn_item()
            if self.score % 30 == 0:
                self.level += 1
                self.generate_obstacles()
        
        # Проверка яда
        elif head == self.poison:
            self.snake.pop()
            if len(self.snake) > 1: self.snake.pop()
            if len(self.snake) <= 1: return False
            self.poison = self.spawn_item()

        # Бонусы
        elif self.powerup and head == self.powerup:
            if self.powerup_type == "SHIELD":
                self.has_shield = True
            else:
                self.active_powerup = self.powerup_type
                self.powerup_end_time = now + 5000
            self.powerup = None
        else:
            self.snake.pop()

        return True