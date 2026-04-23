import pygame
import time
import random
import os

# --- АВТОМАТИЧЕСКАЯ НАСТРОЙКА ПАПКИ ---
# Гарантируем, что Python ищет картинки там же, где лежит сам скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()

# Константы (сетка 20x20)
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20 

# Цвета для текста и эффектов
WHITE = (255, 255, 255)
RED   = (213, 50, 80)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake: Sprite Edition 1000000%')
clock = pygame.time.Clock()

# Шрифты
font_style = pygame.font.SysFont("Verdana", 20)
score_font = pygame.font.SysFont("Verdana", 20)

# --- ФУНКЦИЯ ЗАГРУЗКИ ИЗОБРАЖЕНИЙ ---
def load_img(name, size):
    path = os.path.join("img", name)
    try:
        # convert_alpha() нужен для поддержки прозрачности в PNG
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))
    except Exception as e:
        print(f"Ошибка загрузки {name}: {e}")
        # Если картинка не найдена, создаем цветную заглушку
        surf = pygame.Surface((size, size))
        if "head" in name: surf.fill(GREEN)
        elif "apple" in name: surf.fill(RED)
        else: surf.fill((0, 200, 0))
        return surf

# Предзагрузка всех спрайтов
head_img = load_img("snake_head.png", BLOCK_SIZE)
body_img = load_img("snake_body.png", BLOCK_SIZE)
food_img = load_img("apple.png", BLOCK_SIZE)

# Загрузка твоего фона background1.png
try:
    bg_img = pygame.image.load(os.path.join("img", "background1.png")).convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
except:
    print("Фон background1.png не найден, будет использована заливка.")
    bg_img = None

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def show_stats(score, level, speed):
    """Выводит счетчик и уровень в углу экрана"""
    value = score_font.render(f"Score: {score}  Level: {level}  Speed: {speed}", True, WHITE)
    # Рисуем темную плашку для лучшей видимости текста на фоне
    pygame.draw.rect(screen, (0, 0, 0), [5, 5, 330, 30])
    screen.blit(value, [10, 10])

def draw_snake(snake_list):
    """Рисует змейку: голову и сегменты тела"""
    for i, x in enumerate(snake_list):
        # Последний элемент в списке — это всегда голова
        if i == len(snake_list) - 1:
            screen.blit(head_img, (x[0], x[1]))
        else:
            screen.blit(body_img, (x[0], x[1]))

def get_safe_food_pos(snake_list):
    """Генерирует еду так, чтобы она не упала на змею"""
    while True:
        fx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        fy = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        if [fx, fy] not in snake_list:
            return fx, fy

# --- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ---
def game_loop():
    game_over = False
    game_close = False

    # Начальная позиция
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1

    # Параметры прогрессии
    score = 0
    level = 1
    base_speed = 10
    
    # Создаем первую еду
    foodx, foody = get_safe_food_pos(snake_list)

    while not game_over:

        # Цикл после проигрыша
        while game_close:
            screen.fill(BLACK)
            msg = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
            screen.blit(msg, [WIDTH / 6, HEIGHT / 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop() # Рестарт игры

        # Управление
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Блокировка разворота на 180 градусов
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change, x1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change, x1_change = BLOCK_SIZE, 0

        # ПРОВЕРКА СТОЛКНОВЕНИЯ СО СТЕНОЙ (Wall collision)
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        # Рисуем фон
        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            screen.fill((40, 40, 40))

        # Рисуем еду (apple.png)
        screen.blit(food_img, (foodx, foody))

        # Логика перемещения змеи
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # ПРОВЕРКА СТОЛКНОВЕНИЯ С ТЕЛОМ
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_list)
        
        # Расчет текущей скорости и уровня
        current_speed = base_speed + (level * 2)
        show_stats(score, level, current_speed)

        pygame.display.update()

        # ПРОВЕРКА: Съела ли змея еду
        if x1 == foodx and y1 == foody:
            foodx, foody = get_safe_food_pos(snake_list)
            length_of_snake += 1
            score += 1
            
            # Повышение уровня каждые 3 съеденных яблока
            if score % 3 == 0:
                level += 1

        clock.tick(current_speed)

    pygame.quit()
    quit()

# Погнали!
game_loop()