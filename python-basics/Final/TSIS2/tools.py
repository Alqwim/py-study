import pygame

def flood_fill(surface, x, y, new_color):
    """
    Алгоритм заливки (Flood Fill).
    Использует стек вместо рекурсии, чтобы избежать вылета программы при заливке больших областей.
    """
    # Получаем цвет пикселя, на который нажали
    target_color = surface.get_at((x, y))
    
    # Если цвет пикселя уже совпадает с выбранным цветом — ничего не делаем
    if target_color == new_color:
        return
    
    width, height = surface.get_size()
    # Стек хранит координаты пикселей, которые нужно закрасить
    stack = [(x, y)]
    
    while stack:
        cx, cy = stack.pop()
        
        # Проверяем, не вышли ли мы за границы холста
        if cx < 0 or cx >= width or cy < 0 or cy >= height:
            continue
        
        # Если текущий пиксель имеет исходный цвет — перекрашиваем его
        if surface.get_at((cx, cy)) == target_color:
            surface.set_at((cx, cy), new_color)
            
            # Добавляем в стек всех соседей (справа, слева, сверху, снизу)
            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))

def get_square(start_pos, end_pos):
    """Рассчитывает параметры квадрата на основе движения мыши"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    # Находим самую длинную сторону, чтобы сделать фигуру равносторонней
    side = max(abs(x2 - x1), abs(y2 - y1))
    # Возвращаем координаты и размеры (с учетом направления движения мыши)
    return (x1, y1, side if x2 > x1 else -side, side if y2 > y1 else -side)

def get_right_triangle(start_pos, end_pos):
    """Возвращает три точки для построения прямоугольного треугольника"""
    # Точки: Начало (старт), Угол (вертикаль от старта, горизонталь от конца), Конец (мышь)
    return [start_pos, (start_pos[0], end_pos[1]), end_pos]

def get_equilateral_triangle(start_pos, end_pos):
    """Возвращает точки для построения равностороннего треугольника"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    width = x2 - x1
    # Высота равностороннего треугольника: (sqrt(3)/2) * сторона
    height = int((3**0.5 / 2) * width)
    return [(x1 + width // 2, y1), (x1, y1 + height), (x2, y1 + height)]

def get_rhombus(start_pos, end_pos):
    """Возвращает четыре точки (вершины) ромба"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    w, h = x2 - x1, y2 - y1
    # Центры сторон воображаемого прямоугольника образуют ромб
    return [
        (x1 + w // 2, y1),      # Верхняя точка
        (x2, y1 + h // 2),      # Правая точка
        (x1 + w // 2, y2),      # Нижняя точка
        (x1, y1 + h // 2)       # Левая точка
    ]