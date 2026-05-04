import pygame

WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 50, bold=True)

    def draw_text(self, text, x, y, color=WHITE, center=False, big=False):
        surf = self.big_font.render(str(text), True, color) if big else self.font.render(str(text), True, color)
        rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
        self.screen.blit(surf, rect)

    def button(self, text, x, y, w, h, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, w, h)
        
        # Проверка наведения мышки
        if rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, active_color, rect, border_radius=12)
            if click[0] == 1: # Если нажата левая кнопка мыши
                pygame.time.delay(150) # Короткая пауза, чтобы не было "дребезга" клика
                if action:
                    return action()
                return True # Возвращаем True, если просто нажали на кнопку
        else:
            pygame.draw.rect(self.screen, inactive_color, rect, border_radius=12)
            
        self.draw_text(text, x + w/2, y + h/2, WHITE, center=True)
        return False

    def settings_screen(self, settings):
        self.screen.fill((30, 30, 35))
        self.draw_text("SETTINGS", 200, 80, GOLD, center=True, big=True)
        
        # Кнопка звука
        sound_label = f"SOUND: {'ON' if settings['sound'] else 'OFF'}"
        if self.button(sound_label, 100, 180, 200, 45, (70, 70, 70), (100, 100, 100)):
            settings['sound'] = not settings['sound']
            return "UPDATE" # Сигнал, что настройки изменились

        # Кнопка цвета машины
        color_label = f"COLOR: {settings['color']}"
        if self.button(color_label, 100, 250, 200, 45, (70, 70, 70), (100, 100, 100)):
            cols = ['Red', 'Green', 'Blue', 'Yellow', 'White']
            current_idx = cols.index(settings['color'])
            settings['color'] = cols[(current_idx + 1) % len(cols)]
            return "UPDATE"

        # Кнопка сложности
        diff_label = f"DIFF: {settings['difficulty']}"
        if self.button(diff_label, 100, 320, 200, 45, (70, 70, 70), (100, 100, 100)):
            diffs = ['Easy', 'Medium', 'Hard']
            current_idx = diffs.index(settings['difficulty'])
            settings['difficulty'] = diffs[(current_idx + 1) % len(diffs)]
            return "UPDATE"

        # Кнопка возврата в меню
        if self.button("BACK TO MENU", 100, 450, 200, 45, (150, 50, 50), (200, 50, 50)):
            return "MENU"
            
        return None

    # Остальные методы (main_menu, leaderboard, game_over) остаются без изменений...
    def main_menu(self, user_name):
        self.screen.fill((20, 20, 30))
        self.draw_text("TURBO RACER", 200, 80, GOLD, center=True, big=True)
        self.draw_text(f"Pilot: {user_name}", 200, 150, WHITE, center=True)
        res = self.button("PLAY", 100, 220, 200, 50, (0, 100, 0), (0, 180, 0), lambda: "GAME")
        if not res: res = self.button("LEADERBOARD", 100, 290, 200, 50, (50, 50, 50), (80, 80, 80), lambda: "LEADERBOARD")
        if not res: res = self.button("SETTINGS", 100, 360, 200, 50, (50, 50, 50), (80, 80, 80), lambda: "SETTINGS")
        if not res: res = self.button("EXIT", 100, 430, 200, 50, (100, 0, 0), (180, 0, 0), lambda: "EXIT")
        return res

    def leaderboard_screen(self, data):
        self.screen.fill((10, 10, 10))
        self.draw_text("TOP 10 PILOTS", 200, 50, GOLD, center=True, big=True)
        for i, entry in enumerate(data[:10]):
            self.draw_text(f"{i+1}. {entry['name']} - {entry['score']}", 50, 120 + i*35)
        return self.button("BACK", 150, 520, 100, 40, (50, 50, 50), (150, 0, 0), lambda: "MENU")

    def game_over(self, score, dist, coins):
        overlay = pygame.Surface((400, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        self.draw_text("CRASHED!", 200, 150, (255, 50, 50), center=True, big=True)
        self.draw_text(f"Score: {score}", 200, 220, GOLD, center=True)
        res = self.button("RETRY", 100, 330, 200, 50, (0, 100, 0), (0, 180, 0), lambda: "GAME")
        if not res: res = self.button("MENU", 100, 400, 200, 50, (50, 50, 50), (80, 80, 80), lambda: "MENU")
        return res