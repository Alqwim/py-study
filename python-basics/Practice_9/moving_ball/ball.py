import pygame

class Ball:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 25
        # Начальная позиция — центр экрана
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.color = (255, 0, 0) # Красный
        self.step = 20 # Дистанция одного прыжка

    def move(self, direction):
        if direction == "up":
            # Проверяем, не выйдет ли верхний край шара за границу 0
            if self.y - self.step >= self.radius:
                self.y -= self.step
        elif direction == "down":
            # Проверяем нижнюю границу
            if self.y + self.step <= self.screen_height - self.radius:
                self.y += self.step
        elif direction == "left":
            # Проверяем левую границу
            if self.x - self.step >= self.radius:
                self.x -= self.step
        elif direction == "right":
            # Проверяем правую границу
            if self.x + self.step <= self.screen_width - self.radius:
                self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)