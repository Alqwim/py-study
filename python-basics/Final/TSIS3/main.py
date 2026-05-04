import pygame
import sys
import random
from racer import Player, Enemy, PowerUp, Coin, Hazard, DynamicBarrier, NitroStrip, WIDTH, HEIGHT
from ui import UI
from persistence import save_score, get_leaderboard, get_settings, save_settings

# Основные цвета
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (255, 50, 50)
CYAN = (0, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TURBO RACER 2026")
clock = pygame.time.Clock()
ui = UI(screen)

def game_loop(user_name):
    """Основной игровой процесс"""
    conf = get_settings() # Загружаем настройки перед началом заезда
    player = Player(conf.get('color', 'Red'))
    
    # Настройка сложности на основе конфига
    diff = conf.get('difficulty', 'Medium')
    if diff == 'Easy':
        spawn_rate = 130
        enemy_speed_bonus = 1
    elif diff == 'Hard':
        spawn_rate = 65
        enemy_speed_bonus = 5
    else: # Medium
        spawn_rate = 90
        enemy_speed_bonus = 3

    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    hazards = pygame.sprite.Group()
    events = pygame.sprite.Group()
    
    distance = 0
    coin_count = 0
    base_speed = 5
    road_speed = 5
    nitro_timer = 0
    nitro_active = False

    running = True
    while running:
        curr_time = pygame.time.get_ticks()
        clock.tick(60)

        # Логика скорости
        if nitro_active:
            if curr_time < nitro_timer:
                road_speed = base_speed * 4 
            else:
                nitro_active = False
                road_speed = base_speed
        else:
            base_speed = 5 + (distance // 2000)
            road_speed = base_speed

        distance += road_speed / 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Генерация объектов (Spawn)
        if random.randint(1, spawn_rate) < 2:
            enemies.add(Enemy(road_speed + enemy_speed_bonus))
        if random.randint(1, 150) < 3:
            coins.add(Coin())
        if random.randint(1, 250) < 2:
            hazards.add(Hazard(random.choice(['oil', 'slow'])))
        if random.randint(1, 500) < 2:
            events.add(DynamicBarrier(road_speed))
        if random.randint(1, 600) < 2:
            powerups.add(PowerUp(random.choice(['shield', 'repair'])))
        if random.randint(1, 800) < 2:
            events.add(NitroStrip(road_speed))

        # Обновление позиций
        player.move()
        enemies.update()
        coins.update(road_speed)
        powerups.update(road_speed)
        hazards.update(road_speed)
        events.update(road_speed)

        # Обработка столкновений
        # 1. Монеты
        if pygame.sprite.spritecollide(player, coins, True):
            coin_count += 1

        # 2. Опасности (Лужи)
        player.speed = player.base_speed # Сброс скорости перед проверкой
        h_hit = pygame.sprite.spritecollideany(player, hazards)
        if h_hit:
            if h_hit.kind == 'oil':
                player.rect.x += random.randint(-40, 40)
            elif h_hit.kind == 'slow':
                player.speed = 1.2
                road_speed = 2.0

        # 3. Бонусы (Щит и Ремонт)
        p_hit = pygame.sprite.spritecollideany(player, powerups)
        if p_hit:
            if p_hit.kind == 'shield':
                player.has_shield = True
            elif p_hit.kind == 'repair':
                player.speed = player.base_speed
            p_hit.kill()

        # 4. События (Нитро и Барьеры)
        for e in events:
            if player.rect.colliderect(e.rect):
                if isinstance(e, NitroStrip):
                    nitro_active = True
                    nitro_timer = curr_time + 2500
                    e.kill()
                elif isinstance(e, DynamicBarrier):
                    if player.has_shield:
                        player.has_shield = False
                        e.kill()
                    else:
                        return int(distance + coin_count * 100), distance, coin_count

        # 5. Враги
        en_hit = pygame.sprite.spritecollideany(player, enemies)
        if en_hit:
            if player.has_shield:
                player.has_shield = False
                en_hit.kill()
            else:
                return int(distance + coin_count * 100), distance, coin_count

        # Отрисовка кадра
        screen.fill((20, 20, 25) if nitro_active else (45, 45, 45))
        
        # Разметка дороги
        for y in range(0, HEIGHT, 40): 
            pygame.draw.rect(screen, WHITE, (WIDTH//2-2, (y + distance*5)%HEIGHT, 4, 20))
        
        hazards.draw(screen)
        events.draw(screen)
        coins.draw(screen)
        powerups.draw(screen)
        enemies.draw(screen)
        screen.blit(player.image, player.rect)
        
        # Интерфейс в игре
        ui.draw_text(f"Score: {int(distance + coin_count*100)}", 10, 10, GOLD)
        if player.has_shield:
            ui.draw_text("SHIELD ACTIVE", 10, 40, CYAN)
        if nitro_active:
            ui.draw_text("NITRO!", WIDTH//2, 100, RED, center=True, big=True)
        
        pygame.display.flip()

def main():
    state = "MENU"
    user_name = "Player1"
    game_results = (0, 0, 0) # total, dist, coins
    
    # Загружаем настройки в память один раз
    current_settings = get_settings()
    
    while True:
        if state == "MENU":
            action = ui.main_menu(user_name)
            if action:
                if action == "EXIT":
                    pygame.quit()
                    sys.exit()
                state = action
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_name = user_name[:-1]
                    elif len(user_name) < 12 and event.unicode.isalnum():
                        user_name += event.unicode

        elif state == "GAME":
            # Запускаем игру и получаем результат
            game_results = game_loop(user_name)
            save_score(user_name, game_results[0], game_results[1])
            state = "GAMEOVER"

        elif state == "SETTINGS":
            # Обработка экрана настроек
            res = ui.settings_screen(current_settings)
            if res == "UPDATE":
                save_settings(current_settings) # Сразу пишем в JSON
            elif res == "MENU":
                state = "MENU"
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif state == "LEADERBOARD":
            res = ui.leaderboard_screen(get_leaderboard())
            if res == "MENU":
                state = "MENU"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif state == "GAMEOVER":
            res = ui.game_over(*game_results)
            if res:
                state = res
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()