# main.py
import pygame
import sys
import db
import json
from game import Game
from config import WIDTH, HEIGHT, BLOCK_SIZE

# Инициализация библиотеки Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Shield Snake")
clock = pygame.time.Clock()
font_sm = pygame.font.SysFont("Arial", 22)

def draw_t(text, x, y, col=(255,255,255), center=False):
    """Вспомогательная функция для быстрого рисования текста на экране"""
    img = font_sm.render(text, True, col)
    r = img.get_rect(topleft=(x,y))
    if center: r.center = (x,y)
    screen.blit(img, r)

def settings_screen():
    """Экран настроек: здесь можно менять цвет и сетку"""
    g = Game() 
    colors = [("Green", [0,255,0]), ("Blue", [0,0,255]), ("Red", [255,0,0]), ("Purple", [150,0,150])]
    c_idx = 0
    run = True
    while run:
        screen.fill((40,40,40))
        draw_t("SETTINGS", WIDTH//2, 100, center=True)
        draw_t(f"Color: {colors[c_idx][0]} (Press C to change)", WIDTH//2, 200, colors[c_idx][1], True)
        draw_t(f"Grid: {'ON' if g.settings['grid'] else 'OFF'} (Press G to toggle)", WIDTH//2, 250, center=True)
        draw_t("Press B to Save & Back", WIDTH//2, 400, center=True)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c: # Листаем цвета
                    c_idx = (c_idx + 1) % len(colors)
                    g.settings["snake_color"] = colors[c_idx][1]
                if e.key == pygame.K_g: # Переключаем сетку
                    g.settings["grid"] = not g.settings["grid"]
                if e.key == pygame.K_b: # Сохраняем и выходим
                    g.save_settings()
                    run = False
        pygame.display.flip()

def main_menu():
    """Главное меню с вводом имени игрока"""
    user = ""
    while True:
        screen.fill((20,20,30))
        draw_t("SUPER SHIELD SNAKE", WIDTH//2, 100, (0,255,0), True)
        draw_t(f"Enter Name: {user}", WIDTH//2, 200, center=True)
        draw_t("ENTER: Start | O: Settings | L: Leaderboard", WIDTH//2, 350, center=True)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and user: return user # Начинаем игру
                elif e.key == pygame.K_o: settings_screen() # В настройки
                elif e.key == pygame.K_l: leaderboard_screen() # В таблицу рекордов
                elif e.key == pygame.K_BACKSPACE: user = user[:-1] # Удаление буквы
                else: 
                    if len(user) < 10 and e.unicode.isalnum(): user += e.unicode
        pygame.display.flip()

def leaderboard_screen():
    """Экран со списком ТОП-10 рекордов"""
    scores = db.get_leaderboard()
    run = True
    while run:
        screen.fill((10,10,10))
        draw_t("LEADERBOARD", WIDTH//2, 50, center=True)
        for i, r in enumerate(scores):
            draw_t(f"{i+1}. {r[0]} - {r[1]} pts (Level {r[2]})", 250, 100 + i*35)
        draw_t("Press B to go Back", WIDTH//2, 520, (150,150,150), center=True)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_b: run = False
        pygame.display.flip()

def run_game(user):
    """Основной игровой процесс"""
    pid = db.get_or_create_player(user)
    pb = db.get_personal_best(pid)
    game_obj = Game()
    
    while True:
        # Рассчитываем скорость в зависимости от уровня и бонусов
        speed = game_obj.base_speed + (game_obj.level * 2)
        if game_obj.active_powerup == "SPEED": speed += 8
        if game_obj.active_powerup == "SLOW": speed = max(5, speed-6)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                # Управление (запрещаем поворот на 180 градусов)
                if e.key == pygame.K_UP and game_obj.direction != "DOWN": game_obj.direction = "UP"
                if e.key == pygame.K_DOWN and game_obj.direction != "UP": game_obj.direction = "DOWN"
                if e.key == pygame.K_LEFT and game_obj.direction != "RIGHT": game_obj.direction = "LEFT"
                if e.key == pygame.K_RIGHT and game_obj.direction != "LEFT": game_obj.direction = "RIGHT"
        
        # Обновляем логику
        if not game_obj.update():
            # Если вернулось False — сохраняем рекорд в базу и выходим
            db.save_game(pid, game_obj.score, game_obj.level)
            return game_obj.score, game_obj.level, pb

        # --- РИСОВАНИЕ ---
        screen.fill((0,0,0))
        
        # Рисуем сетку
        if game_obj.settings["grid"]:
            for i in range(0, WIDTH, BLOCK_SIZE): pygame.draw.line(screen, (30,30,30), (i,0), (i,HEIGHT))
            for i in range(0, HEIGHT, BLOCK_SIZE): pygame.draw.line(screen, (30,30,30), (0,i), (WIDTH,i))
            
        # Рисуем змею
        for s in game_obj.snake: 
            pygame.draw.rect(screen, game_obj.settings["snake_color"], (s[0], s[1], BLOCK_SIZE-1, BLOCK_SIZE-1))
            
        # Рисуем еду (зеленая) и яд (красный)
        pygame.draw.rect(screen, (0,255,0), (game_obj.food[0], game_obj.food[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, (150,0,0), (game_obj.poison[0], game_obj.poison[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Рисуем препятствия (серые блоки)
        for o in game_obj.obstacles: 
            pygame.draw.rect(screen, (100,100,100), (o[0], o[1], BLOCK_SIZE, BLOCK_SIZE))
            
        # Рисуем бонус (круг), если он есть
        if game_obj.powerup:
            # Цвет круга зависит от типа бонуса (Щит — голубой, остальное — желтое)
            c = (255,255,0) if game_obj.powerup_type != "SHIELD" else (0,255,255)
            pygame.draw.circle(screen, c, (game_obj.powerup[0]+10, game_obj.powerup[1]+10), 8)
            
        # Информация на экране
        draw_t(f"Score: {game_obj.score} | Lvl: {game_obj.level} | Best: {pb}", 10, 10)
        if game_obj.has_shield: draw_t("SHIELD ACTIVE", 650, 10, (0,255,255))
        
        pygame.display.flip()
        clock.tick(speed)

def game_over_screen(s, l, pb):
    """Экран смерти: можно нажать R, чтобы быстро переиграть"""
    while True:
        screen.fill((60,0,0))
        draw_t("GAME OVER", WIDTH//2, 200, center=True)
        draw_t(f"Score: {s} | Level: {l} | Your Best: {pb}", WIDTH//2, 280, center=True)
        draw_t("R: Retry | M: Main Menu | Q: Quit", WIDTH//2, 400, center=True)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return "RETRY"
                if e.key == pygame.K_m: return "MENU"
                if e.key == pygame.K_q: pygame.quit(); sys.exit()
        pygame.display.flip()

if __name__ == "__main__":
    # Сначала создаем нужные таблицы в БД
    db.create_tables()
    while True:
        # 1. Меню (получаем имя)
        u = main_menu()
        playing = True
        while playing:
            # 2. Играем
            score, lvl, pb = run_game(u)
            # 3. Game Over (ждем выбора игрока)
            act = game_over_screen(score, lvl, pb)
            if act == "MENU": playing = False # Возврат в меню ввода имени