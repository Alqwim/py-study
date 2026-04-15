import pygame
import sys
import os
from player import MusicPlayer

# Фиксация рабочей папки
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Music Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)

font = pygame.font.SysFont("Arial", 22)
title_font = pygame.font.SysFont("Arial", 28, bold=True)

# Загружаем плеер
player = MusicPlayer("music")

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def main():
    running = True
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
        draw_text(f"NOW: {player.get_current_track_name()}", font, BLACK, 50, 320)

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

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()