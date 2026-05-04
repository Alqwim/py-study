import pygame
import random

WIDTH, HEIGHT = 400, 600
LANES = [60, 160, 260, 360] # Центры четырех полос движения

class Player(pygame.sprite.Sprite):
    """Класс главного героя (машины игрока)."""
    def __init__(self, color_name):
        super().__init__()
        # Пытаемся применить цвет из настроек
        try: color = pygame.Color(color_name)
        except: color = pygame.Color("Red")
        
        self.image = pygame.Surface((45, 80))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(200, 500))
        self.base_speed = 7  # Скорость поворота
        self.speed = 7       # Текущая скорость (может меняться в лужах)
        self.has_shield = False

    def move(self):
        """Обработка нажатий клавиш для движения влево/вправо."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    """Класс машины противника."""
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 75))
        self.image.fill((200, 0, 0)) # Враги всегда красные
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))
        self.speed = speed

    def update(self):
        """Враги просто едут вниз."""
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.kill()

class Coin(pygame.sprite.Sprite):
    """Класс золотой монетки."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (12, 12), 12) # Золотой цвет
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))

    def update(self, road_speed):
        self.rect.y += road_speed
        if self.rect.top > HEIGHT: self.kill()

class PowerUp(pygame.sprite.Sprite):
    """Класс бонусов: Щит (бирюзовый) или Ремонт (розовый)."""
    def __init__(self, kind):
        super().__init__()
        self.kind = kind # 'shield' или 'repair'
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        if kind == 'shield':
            pygame.draw.circle(self.image, (0, 255, 255), (15, 15), 15)
        else: # ремонт
            pygame.draw.circle(self.image, (255, 0, 255), (15, 15), 15)
            pygame.draw.rect(self.image, (255, 255, 255), [12, 5, 6, 20]) # Белый крестик
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))

    def update(self, road_speed):
        self.rect.y += road_speed
        if self.rect.top > HEIGHT: self.kill()

class Hazard(pygame.sprite.Sprite):
    """Класс препятствий: Масло (черное) или Лужа (коричневая)."""
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((70, 50), pygame.SRCALPHA)
        if kind == 'oil':
            pygame.draw.ellipse(self.image, (20, 20, 20), [0, 0, 70, 50])
        else: # slow
            pygame.draw.ellipse(self.image, (139, 69, 19, 150), [0, 0, 70, 50])
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))

    def update(self, road_speed):
        self.rect.y += road_speed
        if self.rect.top > HEIGHT: self.kill()

class DynamicBarrier(pygame.sprite.Sprite):
    """Препятствие, которое движется из стороны в сторону."""
    def __init__(self, road_speed):
        super().__init__()
        self.image = pygame.Surface((80, 25))
        self.image.fill((100, 50, 0))
        self.rect = self.image.get_rect(center=(random.randint(100, 300), -100))
        self.move_dir = random.choice([-3, 3])

    def update(self, road_speed):
        self.rect.y += road_speed
        self.rect.x += self.move_dir
        if self.rect.left < 0 or self.rect.right > WIDTH: self.move_dir *= -1
        if self.rect.top > HEIGHT: self.kill()

class NitroStrip(pygame.sprite.Sprite):
    """Синяя стрелка, дающая ускорение."""
    def __init__(self, road_speed):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        # Рисуем полигон в форме стрелки
        pygame.draw.polygon(self.image, (0, 0, 255), [(20, 0), (40, 30), (30, 30), (30, 60), (10, 60), (10, 30), (0, 30)])
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))

    def update(self, road_speed):
        self.rect.y += road_speed
        if self.rect.top > HEIGHT: self.kill()