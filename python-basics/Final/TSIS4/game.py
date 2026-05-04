# game.py
import pygame
import random
import json
import os
from config import WIDTH, HEIGHT, BLOCK_SIZE

class Game:
    def __init__(self):
        # Настройки по умолчанию
        self.settings = {
            "snake_color": [0, 255, 0],
            "grid": True,
            "sound": True
        }
        self.load_settings() # Пробуем загрузить настройки из файла
        self.reset_game()    # Устанавливаем стартовые параметры

    def load_settings(self):
        """Загружает настройки из JSON с защитой от ошибок (безопасное чтение)"""
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.settings["snake_color"] = data.get("snake_color", [0, 255, 0])
                        self.settings["grid"] = data.get("grid", True)
                        self.settings["sound"] = data.get("sound", True)
            except:
                self.save_settings() # Если файл битый, перезапишем его

    def save_settings(self):
        """Сохраняет текущие настройки в файл settings.json"""
        try:
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f)
        except:
            pass

    def reset_game(self):
        """Сбрасывает положение змейки, очки и уровень в начало"""
        self.snake = [[100, 100], [80, 100], [60, 100]] # Змейка из 3-х сегментов
        self.direction = "RIGHT" # Начальное движение
        self.score = 0
        self.level = 1
        self.obstacles = [] # Список серых блоков (препятствий)
        self.food = self.spawn_item() # Обычная еда
        self.poison = self.spawn_item() # Ядовитая еда
        
        # Переменные для бонусов
        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0
        
        # Переменные активных эффектов
        self.active_powerup = None
        self.powerup_end_time = 0
        self.has_shield = False # Статус щита
        
        self.base_speed = 10 # Начальная скорость

    def spawn_item(self):
        """Ищет случайную свободную клетку на поле для еды или бонуса"""
        while True:
            x = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            if [x, y] not in self.snake and [x, y] not in self.obstacles:
                return [x, y]

    def generate_obstacles(self):
        """Создает новые препятствия при повышении уровня (с 3-го уровня)"""
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level * 2):
                obs = self.spawn_item()
                # Не ставим препятствие слишком близко к голове змеи
                if abs(obs[0] - self.snake[0][0]) > BLOCK_SIZE * 3:
                    self.obstacles.append(obs)

    def get_auto_turn_pos(self):
        """АВТОПИЛОТ: Вычисляет безопасную клетку для поворота, если щит активен"""
        head = self.snake[0]
        # Если шли по горизонтали — пробуем повернуть вертикально
        if self.direction in ["LEFT", "RIGHT"]:
            new_head_up = [head[0], head[1] - BLOCK_SIZE]
            # Проверяем, не выходим ли за край и нет ли там хвоста/стен
            if new_head_up[1] >= 0 and new_head_up not in self.obstacles and new_head_up not in self.snake:
                self.direction = "UP"
                return new_head_up
            else:
                self.direction = "DOWN"
                return [head[0], head[1] + BLOCK_SIZE]
        # Если шли вертикально — пробуем горизонтально
        else:
            new_head_right = [head[0] + BLOCK_SIZE, head[1]]
            if new_head_right[0] < WIDTH and new_head_right not in self.obstacles and new_head_right not in self.snake:
                self.direction = "RIGHT"
                return new_head_right
            else:
                self.direction = "LEFT"
                return [head[0] - BLOCK_SIZE, head[1]]

    def update(self):
        """Главный расчет логики в каждом кадре"""
        now = pygame.time.get_ticks()

        # Бонус исчезает через 8 сек, если его не подобрали
        if self.powerup and (now - self.powerup_spawn_time > 8000):
            self.powerup = None
        # Шанс появления нового бонуса
        if not self.powerup and not self.active_powerup and random.random() < 0.01:
            self.powerup = self.spawn_item()
            self.powerup_type = random.choice(["SPEED", "SLOW", "SHIELD"])
            self.powerup_spawn_time = now
        # Эффект бонуса (скорость/замедление) длится 5 секунд
        if self.active_powerup and now > self.powerup_end_time:
            self.active_powerup = None

        # Рассчитываем, куда змея хочет пойти
        head = list(self.snake[0])
        if self.direction == "UP": head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN": head[1] += BLOCK_SIZE
        elif self.direction == "LEFT": head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT": head[0] += BLOCK_SIZE

        # Проверка на столкновение
        hit_wall = head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT
        hit_self = head in self.snake
        hit_obs = head in self.obstacles

        # ЛОГИКА ЩИТА ПРИ СТОЛКНОВЕНИИ
        if (hit_wall or hit_self) and self.has_shield:
            self.has_shield = False # Ломаем щит
            head = self.get_auto_turn_pos() # АВТОПОВОРОТ
        elif hit_obs and self.has_shield:
            self.has_shield = False # Ломаем щит
            self.obstacles.remove(head) # РАЗРУШАЕМ ПРЕПЯТСТВИЕ
        elif hit_wall or hit_self or hit_obs:
            return False # Если щита нет — смерть (Game Over)

        # Добавляем новую голову в список сегментов
        self.snake.insert(0, head)

        # Проверка: съели ли мы еду?
        if head == self.food:
            self.score += 10
            self.food = self.spawn_item()
            if self.score % 30 == 0: # Каждый 30 очков — новый уровень
                self.level += 1
                self.generate_obstacles()
        
        # Проверка: съели ли мы яд?
        elif head == self.poison:
            self.snake.pop() # Удаляем хвост (обычное движение)
            if len(self.snake) > 1: self.snake.pop() # Удаляем еще кусок из-за яда
            if len(self.snake) <= 1: return False # Слишком короткая — смерть
            self.poison = self.spawn_item()

        # Проверка: подобрали ли мы бонус?
        elif self.powerup and head == self.powerup:
            if self.powerup_type == "SHIELD":
                self.has_shield = True
            else:
                self.active_powerup = self.powerup_type
                self.powerup_end_time = now + 5000
            self.powerup = None
        else:
            self.snake.pop() # Если ничего не съели — просто убираем хвост (движение)

        return True