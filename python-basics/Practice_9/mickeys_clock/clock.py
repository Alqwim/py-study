import pygame
import datetime

class MickeyClock:
    def __init__(self, screen, center_pos, hand_image_path):
        self.screen = screen
        self.center_pos = center_pos
        self.original_hand = pygame.image.load(hand_image_path).convert_alpha()
        
    def get_angles(self):
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute

        # 360 / 60 = 6 градусов на секунду/минуту
        sec_angle = -(seconds * 6)
        min_angle = -(minutes * 6)
        
        # На картинке руки скрещены (одна смотрит в одну сторону, вторая — в другую)
        # Нам нужно сдвинуть одну из рук на 180 градусов, чтобы они не накладывались.
        min_angle += 180 

        return min_angle, sec_angle

    def draw_hand(self, angle):
        # Вращаем изображение
        rotated_hand = pygame.transform.rotate(self.original_hand, angle)
        
        # Размещаем повернутое изображение так, чтобы его центр (точка скрещивания рук)
        # оказался в центре экрана.
        new_rect = rotated_hand.get_rect(center=self.center_pos)
        self.screen.blit(rotated_hand, new_rect)

    def update(self):
        min_angle, sec_angle = self.get_angles()
        self.draw_hand(min_angle)
        self.draw_hand(sec_angle)