import pygame
import sys
import os
from ball import Ball

# Фиксация рабочей папки
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Red Ball")

WHITE = (255, 255, 255)

# Создаем объект шара
ball = Ball(WIDTH, HEIGHT)

clock = pygame.time.Clock()

def main():
    running = True
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Обработка одиночных нажатий (как в условии: "каждое нажатие")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move("up")
                elif event.key == pygame.K_DOWN:
                    ball.move("down")
                elif event.key == pygame.K_LEFT:
                    ball.move("left")
                elif event.key == pygame.K_RIGHT:
                    ball.move("right")

        # Отрисовка
        ball.draw(screen)

        pygame.display.flip()
        
        # Ограничение FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()