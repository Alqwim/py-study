import pygame
import sys
import os
from player import MusicPlayer

# Фиксация рабочей папки
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

WIDTH, HEIGHT = 600, 450 # Немного увеличил высоту для прогресс-бара
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Music Player")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
GRAY = (200, 200, 200)

font = pygame.font.SysFont("Arial", 22)
title_font = pygame.font.SysFont("Arial", 28, bold=True)

player = MusicPlayer("music")

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_progress_bar(x, y, w, h, progress_percent):
    """Рисует полосу прогресса"""
    # Рамка (фон)
    pygame.draw.rect(screen, GRAY, (x, y, w, h))
    # Заполнение (прогресс)
    pygame.draw.rect(screen, GREEN, (x, y, w * progress_percent, h))
    # Контур
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        
        draw_text("MUSIC PLAYER CONTROLS", title_font, BLACK, 50, 40)
        draw_text("P - Play / Pause", font, BLACK, 50, 100)
        draw_text("S - Stop", font, BLACK, 50, 140)
        draw_text("N - Next Track", font, BLACK, 50, 180)
        draw_text("B - Previous Track", font, BLACK, 50, 220)
        
        # Инфо о треке
        status_text = "STATUS: PLAYING" if player.is_playing else "STATUS: STOPPED"
        draw_text(status_text, font, GREEN if player.is_playing else BLACK, 50, 280)
        draw_text(f"NOW: {player.get_current_track_name()}", font, BLACK, 50, 310)

        # РАБОТА С ПРОГРЕССОМ
        curr, total, percent = player.get_progress()
        draw_progress_bar(50, 360, 500, 20, percent)
        
        # Таймер текстом (например, 01:23 / 03:45)
        if total > 0:
            time_str = f"{int(curr)//60:02}:{int(curr)%60:02} / {int(total)//60:02}:{int(total)%60:02}"
            draw_text(time_str, font, BLACK, 50, 390)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: player.play()
                if event.key == pygame.K_s: player.stop()
                if event.key == pygame.K_n: player.next_track()
                if event.key == pygame.K_b: player.prev_track()
                if event.key == pygame.K_q: running = False

        pygame.display.flip()
        clock.tick(30) # Ограничиваем FPS для экономии ресурсов

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()