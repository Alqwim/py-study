# main.py
import pygame
import sys
import db
import json
from game import Game
from config import WIDTH, HEIGHT, BLOCK_SIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font_sm = pygame.font.SysFont("Arial", 22)

def draw_t(text, x, y, col=(255,255,255), center=False):
    img = font_sm.render(text, True, col)
    r = img.get_rect(topleft=(x,y))
    if center: r.center = (x,y)
    screen.blit(img, r)

def settings_screen():
    g = Game() # Для доступа к текущим настройкам
    colors = [("Green", [0,255,0]), ("Blue", [0,0,255]), ("Red", [255,0,0])]
    c_idx = 0
    run = True
    while run:
        screen.fill((40,40,40))
        draw_t("SETTINGS", WIDTH//2, 100, center=True)
        draw_t(f"Color: {colors[c_idx][0]} (Press C)", WIDTH//2, 200, colors[c_idx][1], True)
        draw_t(f"Grid: {'ON' if g.settings['grid'] else 'OFF'} (Press G)", WIDTH//2, 250, center=True)
        draw_t("Press B to Save & Back", WIDTH//2, 400, center=True)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    c_idx = (c_idx + 1) % len(colors)
                    g.settings["snake_color"] = colors[c_idx][1]
                if e.key == pygame.K_g: g.settings["grid"] = not g.settings["grid"]
                if e.key == pygame.K_b:
                    g.save_settings()
                    run = False
        pygame.display.flip()

def main_menu():
    user = ""
    while True:
        screen.fill((20,20,30))
        draw_t("SNAKE GAME", WIDTH//2, 100, (0,255,0), True)
        draw_t(f"Name: {user}", WIDTH//2, 200, center=True)
        draw_t("ENTER: Play | O: Settings | L: Leaders", WIDTH//2, 350, center=True)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and user: return user
                elif e.key == pygame.K_o: settings_screen()
                elif e.key == pygame.K_l: leaderboard_screen()
                elif e.key == pygame.K_BACKSPACE: user = user[:-1]
                else: 
                    if len(user) < 10: user += e.unicode
        pygame.display.flip()

def leaderboard_screen():
    scores = db.get_leaderboard()
    run = True
    while run:
        screen.fill((10,10,10))
        draw_t("LEADERS", WIDTH//2, 50, center=True)
        for i, r in enumerate(scores):
            draw_t(f"{i+1}. {r[0]} - {r[1]} pts", 250, 100 + i*30)
        draw_t("Press B", WIDTH//2, 500, center=True)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_b: run = False
        pygame.display.flip()

def run_game(user):
    pid = db.get_or_create_player(user)
    pb = db.get_personal_best(pid)
    g = Game()
    while True:
        speed = g.base_speed + (g.level * 2)
        if g.active_powerup == "SPEED": speed += 8
        if g.active_powerup == "SLOW": speed = max(5, speed-6)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and g.direction != "DOWN": g.direction = "UP"
                if e.key == pygame.K_DOWN and g.direction != "UP": g.direction = "DOWN"
                if e.key == pygame.K_LEFT and g.direction != "RIGHT": g.direction = "LEFT"
                if e.key == pygame.K_RIGHT and g.direction != "LEFT": g.direction = "RIGHT"
        
        if not g.update():
            db.save_game(pid, g.score, g.level)
            return g.score, g.level, pb

        screen.fill((0,0,0))
        if g.settings["grid"]:
            for i in range(0, WIDTH, BLOCK_SIZE): pygame.draw.line(screen, (30,30,30), (i,0), (i,HEIGHT))
            for i in range(0, HEIGHT, BLOCK_SIZE): pygame.draw.line(screen, (30,30,30), (0,i), (WIDTH,i))
        for s in g.snake: pygame.draw.rect(screen, g.settings["snake_color"], (s[0], s[1], BLOCK_SIZE-1, BLOCK_SIZE-1))
        pygame.draw.rect(screen, (0,255,0), (g.food[0], g.food[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, (150,0,0), (g.poison[0], g.poison[1], BLOCK_SIZE, BLOCK_SIZE))
        for o in g.obstacles: pygame.draw.rect(screen, (100,100,100), (o[0], o[1], BLOCK_SIZE, BLOCK_SIZE))
        if g.powerup:
            c = (255,255,0) if g.powerup_type != "SHIELD" else (0,255,255)
            pygame.draw.circle(screen, c, (g.powerup[0]+10, g.powerup[1]+10), 8)
        draw_t(f"Score: {g.score} | Lvl: {g.level}", 10, 10)
        pygame.display.flip()
        clock.tick(speed)

def game_over_screen(s, l, pb):
    while True:
        screen.fill((60,0,0))
        draw_t("GAME OVER", WIDTH//2, 200, center=True)
        draw_t(f"Score: {s} | Best: {pb}", WIDTH//2, 280, center=True)
        draw_t("R: Retry | M: Menu | Q: Quit", WIDTH//2, 400, center=True)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return "R"
                if e.key == pygame.K_m: return "M"
                if e.key == pygame.K_q: pygame.quit(); sys.exit()
        pygame.display.flip()

if __name__ == "__main__":
    db.create_tables()
    while True:
        u = main_menu()
        playing = True
        while playing:
            score, lvl, pb = run_game(u)
            act = game_over_screen(score, lvl, pb)
            if act == "M": playing = False