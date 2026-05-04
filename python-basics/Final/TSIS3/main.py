import pygame
import sys
import random
from racer import Player, Enemy, PowerUp, Coin, Hazard, DynamicBarrier, NitroStrip, WIDTH, HEIGHT
from ui import UI
from persistence import save_score, get_leaderboard, get_settings, save_settings

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TURBO RACER 2026")
clock = pygame.time.Clock()
ui = UI(screen)

def game_loop(user_name):
    """Функция самого заезда."""
    conf = get_settings() # Берем актуальные настройки
    player = Player(conf.get('color', 'Red'))
    
    # Настраиваем сложность (шанс спавна врагов и их скорость)
    diff = conf.get('difficulty', 'Medium')
    spawn_rate = 130 if diff == 'Easy' else (90 if diff == 'Medium' else 65)
    enemy_speed_bonus = 1 if diff == 'Easy' else (3 if diff == 'Medium' else 5)

    # Группы спрайтов для коллизий и обновлений
    enemies, powerups, coins, hazards, events = [pygame.sprite.Group() for _ in range(5)]
    
    distance, coin_count, base_speed, road_speed = 0, 0, 5, 5
    nitro_timer = 0
    nitro_active = False

    while True:
        curr_time = pygame.time.get_ticks()
        clock.tick(60)

        # Логика скорости и Нитро
        if nitro_active:
            if curr_time < nitro_timer: road_speed = base_speed * 4 
            else: nitro_active = False; road_speed = base_speed
        else:
            base_speed = 5 + (distance // 2000) # Постепенное ускорение со временем
            road_speed = base_speed

        distance += road_speed / 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        # Случайное появление объектов
        if random.randint(1, spawn_rate) < 2: enemies.add(Enemy(road_speed + enemy_speed_bonus))
        if random.randint(1, 150) < 3: coins.add(Coin())
        if random.randint(1, 250) < 2: hazards.add(Hazard(random.choice(['oil', 'slow'])))
        if random.randint(1, 500) < 2: events.add(DynamicBarrier(road_speed))
        if random.randint(1, 600) < 2: powerups.add(PowerUp(random.choice(['shield', 'repair'])))
        if random.randint(1, 800) < 2: events.add(NitroStrip(road_speed))

        # Движение всех объектов
        player.move()
        enemies.update(); coins.update(road_speed); powerups.update(road_speed)
        hazards.update(road_speed); events.update(road_speed)

        # Сбор монеток
        if pygame.sprite.spritecollide(player, coins, True): coin_count += 1

        # Наезд на лужи (замедление или занос)
        player.speed = player.base_speed
        h_hit = pygame.sprite.spritecollideany(player, hazards)
        if h_hit:
            if h_hit.kind == 'oil': player.rect.x += random.randint(-40, 40)
            elif h_hit.kind == 'slow': player.speed, road_speed = 1.2, 2.0

        # Получение бонусов
        p_hit = pygame.sprite.spritecollideany(player, powerups)
        if p_hit:
            if p_hit.kind == 'shield': player.has_shield = True
            elif p_hit.kind == 'repair': player.speed = player.base_speed
            p_hit.kill()

        # Проверка Нитро и Столкновений с барьерами
        for e in events:
            if player.rect.colliderect(e.rect):
                if isinstance(e, NitroStrip):
                    nitro_active, nitro_timer = True, curr_time + 2500
                    e.kill()
                elif isinstance(e, DynamicBarrier):
                    if player.has_shield: player.has_shield = False; e.kill()
                    else: return int(distance + coin_count * 100), distance, coin_count

        # Проверка столкновения с врагами
        en_hit = pygame.sprite.spritecollideany(player, enemies)
        if en_hit:
            if player.has_shield: player.has_shield = False; en_hit.kill()
            else: return int(distance + coin_count * 100), distance, coin_count

        # Рендеринг (Отрисовка)
        screen.fill((20, 20, 25) if nitro_active else (45, 45, 45))
        for y in range(0, HEIGHT, 40): # Рисуем дорожную разметку
            pygame.draw.rect(screen, (255,255,255), (WIDTH//2-2, (y + distance*5)%HEIGHT, 4, 20))
        
        hazards.draw(screen); events.draw(screen); coins.draw(screen)
        powerups.draw(screen); enemies.draw(screen)
        screen.blit(player.image, player.rect)
        
        ui.draw_text(f"Score: {int(distance + coin_count*100)}", 10, 10, (255, 215, 0))
        pygame.display.flip()

def main():
    """Точка входа: управление состояниями приложения."""
    state, user_name = "MENU", "Player1"
    game_results = (0, 0, 0)
    current_settings = get_settings()
    
    while True:
        if state == "MENU":
            action = ui.main_menu(user_name)
            if action:
                if action == "EXIT": pygame.quit(); sys.exit()
                state = action
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: user_name = user_name[:-1]
                    elif len(user_name) < 12 and event.unicode.isalnum(): user_name += event.unicode
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        elif state == "GAME":
            game_results = game_loop(user_name)
            save_score(user_name, game_results[0], game_results[1])
            state = "GAMEOVER"

        elif state == "SETTINGS":
            res = ui.settings_screen(current_settings)
            if res == "UPDATE": save_settings(current_settings)
            elif res == "MENU": state = "MENU"
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        elif state == "LEADERBOARD":
            if ui.leaderboard_screen(get_leaderboard()) == "MENU": state = "MENU"
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        elif state == "GAMEOVER":
            res = ui.game_over(*game_results)
            if res: state = res
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()