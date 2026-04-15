import pygame
import sys
import os
from clock import MickeyClock

# Автоматически переходим в папку скрипта
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# Установим размер окна побольше, например 1000x1000, чтобы циферблат влез целиком
WIDTH, HEIGHT = 1000, 1000 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

WHITE = (255, 255, 255)

# Загружаем фон (тело Микки)
try:
    # Загружаем с convert_alpha(), чтобы работала прозрачность (если она есть)
    mickey_bg = pygame.image.load("images/mickey_body.png").convert_alpha()
    # Подгоним размер фона под окно
    mickey_bg = pygame.transform.scale(mickey_bg, (WIDTH, HEIGHT))
except Exception as e:
    mickey_bg = None
    print(f"Фон mickey_body.png не найден: {e}")

# Создаем объект часов (центр должен совпадать с центром циферблата на картинке)
# Если картинка квадратная, центр будет в (WIDTH // 2, HEIGHT // 2)
clock_logic = MickeyClock(screen, (WIDTH // 2, HEIGHT // 2), "images/mickey_hand.png")

clock = pygame.time.Clock()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Сначала очищаем экран (белым цветом)
        screen.fill(WHITE)
        
        # 2. Потом рисуем тело Микки
        if mickey_bg:
            screen.blit(mickey_bg, (0, 0))

        # 3. И только потом рисуем стрелки ПОВЕРХ тела
        clock_logic.update()

        pygame.display.flip()
        
        # Ограничение FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()