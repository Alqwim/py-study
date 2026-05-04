import pygame
import datetime
import os
import tools # Убедись, что tools.py с функциями get_right_triangle и get_equilateral_triangle рядом

# Константы
WIDTH, HEIGHT = 1200, 800
CANVAS_WIDTH = 950
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
BLUE_UI = (0, 120, 215)

# Палитра
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
COLOR_NAMES = ["F1", "F2", "F3", "F4", "F5"]

class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame Paint Ultra Pro")
        
        self.canvas = pygame.Surface((CANVAS_WIDTH, HEIGHT))
        self.canvas.fill(WHITE)
        
        self.clock = pygame.time.Clock()
        self.tool = "pencil"
        self.color = BLACK
        self.thickness = 2
        self.drawing = False
        self.start_pos = None
        
        self.font_main = pygame.font.SysFont("Arial", 16)
        self.font_bold = pygame.font.SysFont("Arial", 18, bold=True)
        
        self.text_active = False
        self.text_content = ""
        self.text_pos = (0, 0)
        self.color_rects = []

    def draw_sidebar(self):
        sidebar_rect = pygame.Rect(CANVAS_WIDTH, 0, WIDTH - CANVAS_WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, sidebar_rect)
        
        y_offset = 20
        title = self.font_bold.render("ИНСТРУМЕНТЫ", True, WHITE)
        self.screen.blit(title, (CANVAS_WIDTH + 20, y_offset))
        
        # Полный список инструментов (Задания 10-11)
        controls = [
            ("P", "Карандаш"), ("L", "Линия"), ("R", "Прямоуг."),
            ("Q", "Квадрат"), ("C", "Круг"), ("W", "Ромб"),
            ("G", "Прямоуг. Δ"), ("H", "Равностор. Δ"),
            ("T", "Текст"), ("F", "Заливка"), ("E", "Ластик"),
            ("", ""),
            ("1,2,3", "Толщина"), ("Ctrl+S", "Сохранить")
        ]
        
        y_offset += 30
        for key, desc in controls:
            if key == "": y_offset += 5; continue
            k_txt = self.font_bold.render(key, True, BLUE_UI)
            d_txt = self.font_main.render(f" - {desc}", True, LIGHT_GRAY)
            self.screen.blit(k_txt, (CANVAS_WIDTH + 15, y_offset))
            self.screen.blit(d_txt, (CANVAS_WIDTH + 15 + k_txt.get_width(), y_offset))
            y_offset += 22

        # Палитра
        y_offset += 20
        pygame.draw.line(self.screen, LIGHT_GRAY, (CANVAS_WIDTH + 10, y_offset), (WIDTH - 10, y_offset))
        y_offset += 15
        self.screen.blit(self.font_bold.render("ЦВЕТА", True, WHITE), (CANVAS_WIDTH + 20, y_offset))
        y_offset += 30
        
        self.color_rects = []
        for i, col in enumerate(COLORS):
            rect = pygame.Rect(CANVAS_WIDTH + 20, y_offset, 25, 25)
            if self.color == col and self.tool != "eraser":
                pygame.draw.rect(self.screen, WHITE, rect.inflate(4, 4), 2)
            pygame.draw.rect(self.screen, col, rect)
            name_txt = self.font_main.render(COLOR_NAMES[i], True, LIGHT_GRAY)
            self.screen.blit(name_txt, (CANVAS_WIDTH + 55, y_offset + 3))
            self.color_rects.append((rect, col))
            y_offset += 35

        # Статус
        status_y = HEIGHT - 60
        info = f"Инструмент: {self.tool.upper()} | {self.thickness}px"
        self.screen.blit(self.font_main.render(info, True, WHITE), (CANVAS_WIDTH + 15, status_y))
        cur_col_rect = pygame.Rect(CANVAS_WIDTH + 15, status_y + 25, 100, 15)
        pygame.draw.rect(self.screen, self.color, cur_col_rect)

    def draw_shape_to(self, surf, tool, start, end, color, thick):
        x1, y1 = start; x2, y2 = end
        if tool == "line": pygame.draw.line(surf, color, start, end, thick)
        elif tool == "rect": pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1)), thick)
        elif tool == "circle": pygame.draw.circle(surf, color, start, int(((x2-x1)**2 + (y2-y1)**2)**0.5), thick)
        elif tool == "square": pygame.draw.rect(surf, color, tools.get_square(start, end), thick)
        elif tool == "r_tri": pygame.draw.polygon(surf, color, tools.get_right_triangle(start, end), thick)
        elif tool == "e_tri": pygame.draw.polygon(surf, color, tools.get_equilateral_triangle(start, end), thick)
        elif tool == "rhombus": pygame.draw.polygon(surf, color, tools.get_rhombus(start, end), thick)

    def run(self):
        while True:
            self.screen.fill(WHITE)
            self.screen.blit(self.canvas, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); return

                if event.type == pygame.KEYDOWN:
                    # Цвета F1-F5
                    f_keys = {pygame.K_F1:0, pygame.K_F2:1, pygame.K_F3:2, pygame.K_F4:3, pygame.K_F5:4}
                    if event.key in f_keys:
                        self.color = COLORS[f_keys[event.key]]
                        if self.tool == "eraser": self.tool = "pencil"

                    # Инструменты (Добавлены G и H для треугольников)
                    keys = {pygame.K_p: "pencil", pygame.K_l: "line", pygame.K_r: "rect", 
                            pygame.K_c: "circle", pygame.K_f: "fill", pygame.K_t: "text", 
                            pygame.K_e: "eraser", pygame.K_q: "square", pygame.K_w: "rhombus",
                            pygame.K_g: "r_tri", pygame.K_h: "e_tri"}
                    if event.key in keys:
                        self.tool = keys[event.key]
                        if self.tool == "eraser": self.color = WHITE
                    
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        self.thickness = {pygame.K_1: 2, pygame.K_2: 5, pygame.K_3: 10}[event.key]
                    
                    if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        # 1. Получаем путь к папке, где лежит текущий файл paint.py
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        
                        # 2. Определяем путь к папке assets рядом с paint.py
                        assets_dir = os.path.join(current_dir, "assets")
                        
                        # 3. Создаем папку assets, если её нет
                        if not os.path.exists(assets_dir):
                            os.makedirs(assets_dir)
                        
                        # 4. Генерируем имя файла с таймстампом
                        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"art_{timestamp}.png"
                        
                        # 5. Полный путь для сохранения
                        save_path = os.path.join(assets_dir, filename)
                        
                        # 6. Сохраняем холст
                        pygame.image.save(self.canvas, save_path)
                        print(f"Файл успешно сохранен по пути: {save_path}")

                    if self.text_active:
                        if event.key == pygame.K_RETURN:
                            txt = self.font_main.render(self.text_content, True, self.color)
                            self.canvas.blit(txt, self.text_pos); self.text_active = False
                        elif event.key == pygame.K_ESCAPE: self.text_active = False
                        elif event.key == pygame.K_BACKSPACE: self.text_content = self.text_content[:-1]
                        else: self.text_content += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_ui = False
                    for rect, col in self.color_rects:
                        if rect.collidepoint(event.pos):
                            self.color = col; clicked_ui = True; break
                    
                    if not clicked_ui and event.pos[0] < CANVAS_WIDTH:
                        if self.tool == "fill": tools.flood_fill(self.canvas, *event.pos, self.color)
                        elif self.tool == "text": self.text_active = True; self.text_pos = event.pos; self.text_content = ""
                        else: self.drawing = True; self.start_pos = event.pos

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.drawing and self.tool not in ["pencil", "eraser"]:
                        self.draw_shape_to(self.canvas, self.tool, self.start_pos, event.pos, self.color, self.thickness)
                    self.drawing = False

            # Карандаш
            if self.drawing and self.tool in ["pencil", "eraser"]:
                curr = pygame.mouse.get_pos()
                if curr[0] < CANVAS_WIDTH:
                    pygame.draw.line(self.canvas, self.color, self.start_pos, curr, self.thickness)
                    self.start_pos = curr

            # Live Preview
            if self.drawing and self.tool not in ["pencil", "eraser", "fill", "text"]:
                if mouse_pos[0] < CANVAS_WIDTH:
                    self.draw_shape_to(self.screen, self.tool, self.start_pos, mouse_pos, self.color, self.thickness)

            if self.text_active:
                self.screen.blit(self.font_main.render(self.text_content + "|", True, self.color), self.text_pos)

            self.draw_sidebar()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    PaintApp().run()