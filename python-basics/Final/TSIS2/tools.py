import pygame

def flood_fill(surface, x, y, new_color):
    """Алгоритм заливки на основе стека (чтобы не было RecursionError)"""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    width, height = surface.get_size()
    stack = [(x, y)]
    
    while stack:
        cx, cy = stack.pop()
        if cx < 0 or cx >= width or cy < 0 or cy >= height:
            continue
        if surface.get_at((cx, cy)) != target_color:
            continue
        
        surface.set_at((cx, cy), new_color)
        stack.append((cx + 1, cy))
        stack.append((cx - 1, cy))
        stack.append((cx, cy + 1))
        stack.append((cx, cy - 1))

def get_square(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    side = max(abs(x2 - x1), abs(y2 - y1))
    return (x1, y1, side if x2 > x1 else -side, side if y2 > y1 else -side)

def get_right_triangle(start_pos, end_pos):
    return [start_pos, (start_pos[0], end_pos[1]), end_pos]

def get_equilateral_triangle(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    width = x2 - x1
    height = int((3**0.5 / 2) * width)
    return [(x1 + width // 2, y1), (x1, y1 + height), (x2, y1 + height)]

def get_rhombus(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    w, h = x2 - x1, y2 - y1
    return [
        (x1 + w // 2, y1),      # верх
        (x2, y1 + h // 2),      # право
        (x1 + w // 2, y2),      # низ
        (x1, y1 + h // 2)       # лево
    ]