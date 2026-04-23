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
current_tool = "pen" # Инструменты: pen, rect, circle, eraser
drawing = False
start_pos = None

# Шрифт для меню
font = pygame.font.SysFont("Verdana", 15)

# Создаем основной слой для рисования (чтобы фигуры не исчезали)
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(WHITE)

def show_menu():
    """Отображает текущий инструмент и цвет"""
    msg = f"Tool: {current_tool.upper()} | Color: {current_color} | [R]-Rect [C]-Circle [P]-Pen [E]-Eraser [1-4]-Colors"
    text = font.render(msg, True, BLACK)
    pygame.draw.rect(screen, (200, 200, 200), [0, 0, WIDTH, 25])
    screen.blit(text, (10, 5))

# --- ГЛАВНЫЙ ЦИКЛ ---
while True:
    # Отрисовка базового слоя и меню
    screen.blit(base_layer, (0, 0))
    show_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Выбор цвета клавишами 1-4
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: current_color = RED
            if event.key == pygame.K_2: current_color = GREEN
            if event.key == pygame.K_3: current_color = BLUE
            if event.key == pygame.K_4: current_color = BLACK
            
            # Выбор инструмента клавишами
            if event.key == pygame.K_r: current_tool = "rect"
            if event.key == pygame.K_c: current_tool = "circle"
            if event.key == pygame.K_p: current_tool = "pen"
            if event.key == pygame.K_e: current_tool = "eraser"

        # Логика мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos # Запоминаем точку начала

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            # Когда отпускаем мышь, рисуем финальную фигуру на основном слое
            end_pos = event.pos
            
            if current_tool == "rect":
                width = end_pos[0] - start_pos[0]
                height = end_pos[1] - start_pos[1]
                pygame.draw.rect(base_layer, current_color, [start_pos[0], start_pos[1], width, height], 2)
            
            elif current_tool == "circle":
                radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5)
                pygame.draw.circle(base_layer, current_color, start_pos, radius, 2)

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                mouse_pos = event.pos
                if current_tool == "pen":
                    # Рисуем линию на базовом слое (непрерывное рисование)
                    pygame.draw.circle(base_layer, current_color, mouse_pos, 3)
                
                elif current_tool == "eraser":
                    # Ластик — это просто рисование белым цветом
                    pygame.draw.circle(base_layer, WHITE, mouse_pos, 20)

    # Предпросмотр фигуры (пока мышь зажата, рисуем "фантом" на экране)
    if drawing and start_pos:
        current_pos = pygame.mouse.get_pos()
        if current_tool == "rect":
            width = current_pos[0] - start_pos[0]
            height = current_pos[1] - start_pos[1]
            pygame.draw.rect(screen, current_color, [start_pos[0], start_pos[1], width, height], 2)
        elif current_tool == "circle":
            radius = int(((current_pos[0] - start_pos[0])**2 + (current_pos[1] - start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, current_color, start_pos, radius, 2)

    pygame.display.flip()