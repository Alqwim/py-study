import pygame, sys
from pygame.locals import *
import random, time
import os

# --- АВТОМАТИЧЕСКАЯ НАСТРОЙКА ПАПКИ ---
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
GRAY = (50, 50, 50)

# Настройка экрана
DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer: Ultra 1000000% Edition")
FramePerSec = pygame.time.Clock()

# Шрифты
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)

# --- ФУНКЦИЯ ЗАГРУЗКИ ИЗОБРАЖЕНИЙ ---
def load_img(name, scale=None, fallback_color=(255, 0, 255)):
    path = os.path.join("img", name)
    try:
        if not os.path.exists(path):
            raise FileNotFoundError
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except:
        # Если картинка не найдена, создаем заглушку
        surf = pygame.Surface(scale if scale else (50, 50), pygame.SRCALPHA)
        if name == "background.png":
            surf.fill((30, 30, 30)) # Темный асфальт
            pygame.draw.line(surf, WHITE, (200, 0), (200, 600), 5)
        elif "coin" in name:
            pygame.draw.circle(surf, YELLOW, (25, 25), 20)
        else:
            surf.fill(fallback_color)
        return surf

# Предзагрузка фона
bg_image = load_img("background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_y = 0

# --- КЛАССЫ ---

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = load_img("Enemy.png", (50, 90), RED)
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
        self.image = load_img("Player.png", (50, 90), (0, 0, 255))
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
        # Загружаем базовую картинку монеты
        self.original_image = load_img("coin.png", (50, 50), YELLOW)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.value = 1
        self.spawn()

    def spawn(self):
        # Случайный вес: 1 (обычная), 2 (редкая), 5 (супер)
        self.value = random.choice([1, 1, 1, 2, 2, 5])
        
        # Масштабируем: чем дороже монета, тем она больше (или меньше, на ваш вкус)
        # Здесь: 1 -> 30px, 2 -> 45px, 5 -> 60px
        size = 20 + (self.value * 10)
        self.image = pygame.transform.scale(self.original_image, (size, size))
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# --- СОЗДАНИЕ ОБЪЕКТОВ ---
P1 = Player()
E1 = Enemy()
C1 = Coin()

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
            SPEED += 0.1 # Плавное ускорение
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 1. Анимированный фон
    DISPLAYSURFACE.blit(bg_image, (0, bg_y))
    DISPLAYSURFACE.blit(bg_image, (0, bg_y - SCREEN_HEIGHT))
    bg_y += SPEED
    if bg_y >= SCREEN_HEIGHT:
        bg_y = 0

    # 2. Отрисовка UI
    score_txt = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_txt = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    # Подложка для текста, чтобы его было видно на любом фоне
    pygame.draw.rect(DISPLAYSURFACE, WHITE, (5, 5, 120, 60))
    DISPLAYSURFACE.blit(score_txt, (10, 10))
    DISPLAYSURFACE.blit(coins_txt, (10, 35))

    # 3. Движение и отрисовка
    for entity in all_sprites:
        DISPLAYSURFACE.blit(entity.image, entity.rect)
        entity.move()

    # 4. Сбор монет (с учетом веса)
    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += C1.value # Прибавляем вес монеты!
        C1.spawn()

    # 5. Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)
        DISPLAYSURFACE.fill(RED)
        msg = font_big.render("GAME OVER", True, WHITE)
        DISPLAYSURFACE.blit(msg, (30, 250))
        res = font_small.render(f"Total Score: {SCORE} | Coins: {COIN_SCORE}", True, WHITE)
        DISPLAYSURFACE.blit(res, (50, 350))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)