import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        # Проверяем наличие папки
        if not os.path.exists(music_folder):
            os.makedirs(music_folder)
        
        # Получаем список файлов
        self.playlist = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav'))]
        self.current_index = 0
        self.is_playing = False

    def play(self):
        if self.playlist:
            track_path = os.path.join(self.music_folder, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play()

    def prev_track(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play()

    def get_current_track_name(self):
        if self.playlist:
            return self.playlist[self.current_index]
        return "No tracks found in /music folder"