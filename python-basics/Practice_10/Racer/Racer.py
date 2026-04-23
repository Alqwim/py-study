import pygame
import sys
import random

# Инициализация
pygame.init()

# Константы
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
SPEED = 5  # Фиксированная скорость

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)      # Враг
GREEN = (0, 255, 0)    # Игрок
YELLOW = (255, 255, 0) # Монета
GRAY = (50, 50, 50)    # Дорога

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Primitive Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

# Создание объектов
player = Player()
enemy = Enemy()
coin = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

# Игровые переменные
collected_coins = 0

# Главный цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Логика движения
    player.move()
    enemy.move()
    coin.move()

    # Проверка столкновения с монетой
    if pygame.sprite.spritecollideany(player, coins):
        collected_coins += 1
        coin.reset()

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(player, enemies):
        print(f"Game Over! Монет собрано: {collected_coins}")
        pygame.quit()
        sys.exit()

    # Отрисовка
    screen.fill(GRAY) # Фон-дорога
    
    # Рисуем все объекты
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    # Отображение счетчика монет
    score_text = font.render(f"Coins: {collected_coins}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 110, 20))

    pygame.display.update()
    clock.tick(FPS)