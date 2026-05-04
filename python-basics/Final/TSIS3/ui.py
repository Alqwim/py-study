import pygame

# Константы цветов для UI
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (255, 50, 50)

class UI:
    """Класс для управления интерфейсом и кнопками."""
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 50, bold=True)

    def draw_text(self, text, x, y, color=WHITE, center=False, big=False):
        """Универсальный метод для вывода текста на экран."""
        surf = self.big_font.render(str(text), True, color) if big else self.font.render(str(text), True, color)
        rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
        self.screen.blit(surf, rect)

    def button(self, text, x, y, w, h, inactive_color, active_color, action=None):
        """Создает интерактивную кнопку, реагирующую на наведение и клик."""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, w, h)
        
        # Если мышка над кнопкой — подсвечиваем её
        if rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, active_color, rect, border_radius=12)
            if click[0] == 1: # Левый клик
                pygame.time.delay(150) # Пауза для предотвращения спама кликов
                return action() if action else True
        else:
            pygame.draw.rect(self.screen, inactive_color, rect, border_radius=12)
            
        self.draw_text(text, x + w/2, y + h/2, WHITE, center=True)
        return False

    def main_menu(self, user_name):
        """Экран главного меню."""
        self.screen.fill((20, 20, 30))
        self.draw_text("TURBO RACER", 200, 80, GOLD, center=True, big=True)
        self.draw_text(f"Pilot: {user_name}", 200, 150, WHITE, center=True)
        
        # Список кнопок и их действий
        res = self.button("PLAY", 100, 220, 200, 50, (0, 100, 0), (0, 180, 0), lambda: "GAME")
        if not res: res = self.button("LEADERBOARD", 100, 290, 200, 50, (50, 50, 50), (80, 80, 80), lambda: "LEADERBOARD")
        if not res: res = self.button("SETTINGS", 100, 360, 200, 50, (50, 50, 50), (80, 80, 80), lambda: "SETTINGS")
        if not res: res = self.button("EXIT", 100, 430, 200, 50, (100, 0, 0), (180, 0, 0), lambda: "EXIT")
        return res

    def settings_screen(self, settings):
        """Экран настроек сложности, цвета и звука."""
        self.screen.fill((30, 30, 35))
        self.draw_text("SETTINGS", 200, 80, GOLD, center=True, big=True)
        
        # Кнопка переключения звука
        if self.button(f"SOUND: {'ON' if settings['sound'] else 'OFF'}", 100, 180, 200, 45, (70, 70, 70), (100, 100, 100)):
            settings['sound'] = not settings['sound']
            return "UPDATE"

        # Кнопка выбора цвета
        if self.button(f"COLOR: {settings['color']}", 100, 250, 200, 45, (70, 70, 70), (100, 100, 100)):
            cols = ['Red', 'Green', 'Blue', 'Yellow', 'White']
            settings['color'] = cols[(cols.index(settings['color']) + 1) % len(cols)]
            return "UPDATE"

        # Кнопка выбора сложности
        if self.button(f"DIFF: {settings['difficulty']}", 100, 320, 200, 45, (70, 70, 70), (100, 100, 100)):
            diffs = ['Easy', 'Medium', 'Hard']
            settings['difficulty'] = diffs[(diffs.index(settings['difficulty']) + 1) % len(diffs)]
            return "UPDATE"

        if self.button("BACK TO MENU", 100, 450, 200, 45, (150, 50, 50), (200, 50, 50)):
            return "MENU"
        return None

    def leaderboard_screen(self, data):
        """Отображение топ-10 игроков."""
        self.screen.fill((10, 10, 10))
        self.draw_text("TOP 10 PILOTS", 200, 50, GOLD, center=True, big=True)
        for i, entry in enumerate(data[:10]):
            self.draw_text(f"{i+1}. {entry['name']} - {entry['score']}", 50, 120 + i*35)
        return "MENU" if self.button("BACK", 150, 520, 100, 40, (50, 50, 50), (150, 0, 0)) else None

    def game_over(self, score, dist, coins):
        """Экран после столкновения."""
        overlay = pygame.Surface((400, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) # Затемнение фона
        self.screen.blit(overlay, (0, 0))
        
        self.draw_text("CRASHED!", 200, 150, RED, center=True, big=True)
        self.draw_text(f"Total Score: {score}", 200, 220, GOLD, center=True)
        
        res = self.button("RETRY", 100, 330, 200, 50, (0, 100, 0), (0, 180, 0), lambda: "GAME")
        if not res: res = self.button("MENU", 100, 400, 200, 50, (50, 50, 50), (80, 80, 80), lambda: "MENU")
        return res