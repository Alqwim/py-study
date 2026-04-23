import pygame
import sys

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint: Pro Edition")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Начальные настройки
current_color = BLACK
# Инструменты: pen, rect, circle, eraser, square, right_tri, equ_tri, rhombus
current_tool = "pen" 
drawing = False
start_pos = None

font = pygame.font.SysFont("Verdana", 14)

base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(WHITE)

def get_points(tool, start, end):
    """Рассчитывает точки для полигонов"""
    x1, y1 = start
    x2, y2 = end
    
    if tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        sx = x1 if x2 > x1 else x1 - side
        sy = y1 if y2 > y1 else y1 - side
        return [sx, sy, side, side] # Возвращаем Rect data

    elif tool == "right_tri":
        return [(x1, y1), (x1, y2), (x2, y2)]

    elif tool == "equ_tri":
        height = (y2 - y1)
        return [(x1 + (x2 - x1) / 2, y1), (x1, y2), (x2, y2)]

    elif tool == "rhombus":
        return [(x1 + (x2 - x1) / 2, y1), (x2, y1 + (y2 - y1) / 2), 
                (x1 + (x2 - x1) / 2, y2), (x1, y1 + (y2 - y1) / 2)]
    return []

def show_menu():
    msg = f"Tool: {current_tool.upper()} | [P]en [R]ect [S]quare [T]right_Tri [G]equ_Tri [B]hombus [E]raser"
    text = font.render(msg, True, BLACK)
    pygame.draw.rect(screen, (200, 200, 200), [0, 0, WIDTH, 25])
    screen.blit(text, (10, 5))

# --- ГЛАВНЫЙ ЦИКЛ ---
while True:
    screen.blit(base_layer, (0, 0))
    show_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Выбор цвета
            if event.key == pygame.K_1: current_color = RED
            if event.key == pygame.K_2: current_color = GREEN
            if event.key == pygame.K_3: current_color = BLUE
            if event.key == pygame.K_4: current_color = BLACK
            
            # Выбор инструмента
            if event.key == pygame.K_p: current_tool = "pen"
            if event.key == pygame.K_r: current_tool = "rect"
            if event.key == pygame.K_c: current_tool = "circle"
            if event.key == pygame.K_e: current_tool = "eraser"
            if event.key == pygame.K_s: current_tool = "square"
            if event.key == pygame.K_t: current_tool = "right_tri"
            if event.key == pygame.K_g: current_tool = "equ_trii"
            if event.key == pygame.K_b: current_tool = "rhombus"

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos
            
            if current_tool == "rect":
                pygame.draw.rect(base_layer, current_color, [start_pos[0], start_pos[1], end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]], 2)
            elif current_tool == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(base_layer, current_color, start_pos, radius, 2)
            elif current_tool == "square":
                r_data = get_points("square", start_pos, end_pos)
                pygame.draw.rect(base_layer, current_color, r_data, 2)
            elif current_tool in ["right_tri", "equ_tri", "rhombus"]:
                pts = get_points(current_tool, start_pos, end_pos)
                pygame.draw.polygon(base_layer, current_color, pts, 2)

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == "pen":
                    pygame.draw.circle(base_layer, current_color, event.pos, 3)
                elif current_tool == "eraser":
                    pygame.draw.circle(base_layer, WHITE, event.pos, 20)

    # Предпросмотр
    if drawing and start_pos:
        curr = pygame.mouse.get_pos()
        if current_tool == "rect":
            pygame.draw.rect(screen, current_color, [start_pos[0], start_pos[1], curr[0]-start_pos[0], curr[1]-start_pos[1]], 2)
        elif current_tool == "circle":
            radius = int(((curr[0]-start_pos[0])**2 + (curr[1]-start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, radius, 2)
        elif current_tool == "square":
            pygame.draw.rect(screen, current_color, get_points("square", start_pos, curr), 2)
        elif current_tool in ["right_tri", "equ_tri", "rhombus"]:
            pygame.draw.polygon(screen, current_color, get_points(current_tool, start_pos, curr), 2)

    pygame.display.flip()