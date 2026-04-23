import pygame
import os
from mutagen.mp3 import MP3 # Не забудьте установить: pip install mutagen

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        if not os.path.exists(music_folder):
            os.makedirs(music_folder)
        
        self.playlist = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav'))]
        self.current_index = 0
        self.is_playing = False
        self.duration = 0 

    def play(self):
        if self.playlist:
            track_path = os.path.join(self.music_folder, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_playing = True
            
            # Получаем длительность
            try:
                audio = MP3(track_path)
                self.duration = audio.info.length
            except:
                self.duration = 0

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
        return "No tracks found"

    # ВОТ ЭТОТ МЕТОД НУЖЕН:
    def get_progress(self):
        if not self.is_playing or self.duration <= 0:
            return 0, 0, 0
        
        # get_pos() дает время в мс
        current_pos = pygame.mixer.music.get_pos() / 1000.0
        # Если музыка на паузе или остановлена, get_pos может вернуть -1
        if current_pos < 0: current_pos = 0
        
        percent = min(current_pos / self.duration, 1.0)
        return current_pos, self.duration, percent