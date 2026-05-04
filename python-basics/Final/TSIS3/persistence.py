import json
import os

def load_json(filename, default):
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, 'w') as f:
            json.dump(default, f)
        return default
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except:
            return default

def get_leaderboard():
    return load_json('leaderboard.json', [])

def save_score(name, score, distance):
    lb = get_leaderboard()
    lb.append({"name": name, "score": int(score), "distance": int(distance)})
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    with open('leaderboard.json', 'w') as f:
        json.dump(lb, f, indent=4)

def get_settings():
    return load_json('settings.json', {"sound": True, "color": "Red", "difficulty": "Medium"})

def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)