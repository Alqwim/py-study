import pygame
import time
import random
import os

# --- АВТОМАТИЧЕСКАЯ НАСТРОЙКА ПАПКИ ---
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20 

WHITE = (255, 255, 255)
RED   = (213, 50, 80)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD  = (255, 215, 0)
PURPLE = (160, 32, 240)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake: Weight & Timer Edition')
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("Verdana", 20)
score_font = pygame.font.SysFont("Verdana", 20)

# --- ФУНКЦИЯ ЗАГРУЗКИ ИЗОБРАЖЕНИЙ ---
def load_img(name, size, color=(255, 0, 0)):
    path = os.path.join("img", name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))
    except:
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (size//2, size//2), size//2)
        return surf

head_img = load_img("snake_head.png", BLOCK_SIZE, GREEN)
body_img = load_img("snake_body.png", BLOCK_SIZE, (0, 200, 0))
# Базовые картинки для разных типов еды
food_imgs = {
    1: load_img("apple.png", BLOCK_SIZE, RED),        # Обычная
    3: load_img("rare.png", BLOCK_SIZE, PURPLE),      # Редкая
    5: load_img("gold.png", BLOCK_SIZE, GOLD)         # Золотая
}

try:
    bg_img = pygame.image.load(os.path.join("img", "background1.png")).convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
except:
    bg_img = None

# --- КЛАСС ЕДЫ ---
class Food:
    def __init__(self, snake_list):
        self.spawn(snake_list)

    def spawn(self, snake_list):
        # 1. Рандомный вес: 1 (70%), 3 (20%), 5 (10%)
        chance = random.random()
        if chance < 0.7: self.weight = 1
        elif chance < 0.9: self.weight = 3
        else: self.weight = 5

        # 2. Рандомная позиция
        while True:
            self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            if [self.x, self.y] not in snake_list:
                break
        
        # 3. Таймер исчезновения (от 5 до 10 секунд)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(5000, 10000) 

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def draw(self):
        # Эффект мигания, если осталось меньше 2 секунд
        remaining = self.lifetime - (pygame.time.get_ticks() - self.spawn_time)
        if remaining < 2000 and (remaining // 200) % 2 == 0:
            return # Пропускаем отрисовку для эффекта мигания
        
        img = food_imgs[self.weight]
        screen.blit(img, (self.x, self.y))

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def show_stats(score, level, speed, food_timer):
    pygame.draw.rect(screen, (0, 0, 0), [5, 5, 450, 30])
    timer_sec = max(0, food_timer // 1000)
    value = score_font.render(f"Score: {score} Lvl: {level} Spd: {speed} Food: {timer_sec}s", True, WHITE)
    screen.blit(value, [10, 10])

def draw_snake(snake_list):
    for i, x in enumerate(snake_list):
        img = head_img if i == len(snake_list) - 1 else body_img
        screen.blit(img, (x[0], x[1]))

# --- ОСНОВНОЙ ЦИКЛ ---
def game_loop():
    game_over = False
    game_close = False

    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1
    score = 0
    level = 1
    base_speed = 10
    
    # Создаем объект еды
    current_food = Food(snake_list)

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            msg = font_style.render("Game Over! C-Play Again or Q-Quit", True, RED)
            screen.blit(msg, [WIDTH / 6, HEIGHT / 2])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: game_over = True; game_close = False
                    if event.key == pygame.K_c: game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0: x1_change, y1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0: x1_change, y1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0: y1_change, x1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and y1_change == 0: y1_change, x1_change = BLOCK_SIZE, 0

        # Движение
        x1 += x1_change
        y1 += y1_change

        # Стены
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0: game_close = True

        # Фон
        if bg_img: screen.blit(bg_img, (0, 0))
        else: screen.fill((40, 40, 40))

        # ПРОВЕРКА ТАЙМЕРА ЕДЫ
        if current_food.is_expired():
            current_food.spawn(snake_list)

        current_food.draw()

        # Змея
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake: del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head: game_close = True

        draw_snake(snake_list)
        
        current_speed = base_speed + (level * 2)
        rem_time = current_food.lifetime - (pygame.time.get_ticks() - current_food.spawn_time)
        show_stats(score, level, current_speed, rem_time)

        pygame.display.update()

        # ПРОВЕРКА: СЪЕЛ ЕДУ
        if x1 == current_food.x and y1 == current_food.y:
            score += current_food.weight        # Добавляем разный вес
            length_of_snake += 1                # Растем всегда на 1 (можно сделать +current_food.weight)
            
            # Повышаем уровень
            level = (score // 5) + 1 
            
            current_food.spawn(snake_list)      # Создаем новую еду

        clock.tick(current_speed)

    pygame.quit()
    quit()

game_loop()