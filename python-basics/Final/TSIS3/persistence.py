import json
import os

# Пути к файлам данных
SCORE_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

def get_leaderboard():
    """Загружает список лучших игроков из JSON-файла."""
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, "r") as f:
        # Читаем и сортируем по убыванию очков
        data = json.load(f)
        return sorted(data, key=lambda x: x['score'], reverse=True)

def save_score(name, score, distance):
    """Сохраняет новый результат в таблицу лидеров."""
    data = get_leaderboard()
    data.append({"name": name, "score": score, "distance": int(distance)})
    with open(SCORE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_settings():
    """Загружает настройки (звук, цвет, сложность) или создает стандартные."""
    default = {"sound": True, "color": "Red", "difficulty": "Medium"}
    if not os.path.exists(SETTINGS_FILE):
        return default
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    """Записывает текущие настройки в JSON-файл."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)