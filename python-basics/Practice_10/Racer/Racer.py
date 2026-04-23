import pygame, sys
from pygame.locals import *
import random, time
import os

# --- АВТОМАТИЧЕСКАЯ НАСТРОЙКА ПАПКИ ---
# Этот блок заставляет скрипт искать файлы в той папке, где он сам находится
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()

# Основные параметры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)
RED = (255, 0, 0)

# Настройка экрана
DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer: Ultra 1000000% Edition")
FramePerSec = pygame.time.Clock()

# Шрифты
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

# --- ФУНКЦИЯ ЗАГРУЗКИ ИЗОБРАЖЕНИЙ ---
def load_img(name, scale=None):
    path = os.path.join("img", name)
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except:
        # Если картинка не найдена, создаем цветной квадрат, чтобы игра не вылетала
        print(f"Внимание: Файл {name} не найден в папке img/")
        surf = pygame.Surface(scale if scale else (50, 50))
        surf.fill((255, 0, 255)) # Розовый цвет ошибки
        return surf

# Предзагрузка фона
bg_image = load_img("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_y = 0

# --- КЛАССЫ ---

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = load_img("Enemy.png", (50, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = -100
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = load_img("Player.png", (50, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-7, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(7, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_img("coin.png", (35, 35))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# --- СОЗДАНИЕ ОБЪЕКТОВ ---
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группировка спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Событие увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# --- ИГРОВОЙ ЦИКЛ ---
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 1. Анимированный фон (бесконечная дорога)
    DISPLAYSURFACE.blit(bg_image, (0, bg_y))
    DISPLAYSURFACE.blit(bg_image, (0, bg_y - SCREEN_HEIGHT))
    bg_y += SPEED
    if bg_y >= SCREEN_HEIGHT:
        bg_y = 0

    # 2. Отрисовка UI
    score_txt = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_txt = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURFACE.blit(score_txt, (10, 10))
    DISPLAYSURFACE.blit(coins_txt, (SCREEN_WIDTH - 110, 10))

    # 3. Движение и отрисовка всех сущностей
    for entity in all_sprites:
        DISPLAYSURFACE.blit(entity.image, entity.rect)
        entity.move()

    # 4. Сбор монет
    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += 1
        C1.spawn() # Монетка мгновенно прыгает наверх

    # 5. Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)
        DISPLAYSURFACE.fill(RED)
        msg = font_big.render("GAME OVER", True, WHITE)
        DISPLAYSURFACE.blit(msg, (30, 250))
        res = font_small.render(f"Total Coins: {COIN_SCORE}", True, WHITE)
        DISPLAYSURFACE.blit(res, (130, 350))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)