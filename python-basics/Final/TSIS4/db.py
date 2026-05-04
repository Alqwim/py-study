# db.py
import psycopg2
from config import DB_CONFIG

def get_connection():
    """Создает соединение с базой данных с поддержкой русского языка (UTF8)"""
    conn_str = f"dbname='{DB_CONFIG['dbname']}' user='{DB_CONFIG['user']}' password='{DB_CONFIG['password']}' host='{DB_CONFIG['host']}' port='{DB_CONFIG['port']}' options='-c client_encoding=UTF8'"
    return psycopg2.connect(conn_str)

def create_tables():
    """Создает таблицы 'players' и 'game_sessions', если их еще нет в базе"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Создаем таблицу игроков (уникальные имена)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id       SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
            
            -- Создаем таблицу сессий (рекорды, привязанные к ID игрока)
            CREATE TABLE IF NOT EXISTS game_sessions (
                id            SERIAL PRIMARY KEY,
                player_id     INTEGER REFERENCES players(id),
                score         INTEGER   NOT NULL,
                level_reached INTEGER   NOT NULL,
                played_at     TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка БД при создании таблиц: {e}")

def get_or_create_player(username):
    """Ищет игрока по имени. Если его нет — создает нового. Возвращает его ID."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Пытаемся вставить имя, если занято — ничего не делаем (ON CONFLICT)
        cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        conn.commit()
        # Получаем ID игрока
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return player_id
    except Exception as e:
        print(f"Ошибка БД при поиске игрока: {e}")
        return None

def save_game(player_id, score, level):
    """Записывает результат финальной игры в таблицу сессий"""
    if player_id is None: return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                    (player_id, score, level))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка БД при сохранении игры: {e}")

def get_leaderboard():
    """Запрашивает ТОП-10 лучших результатов всех времен"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at 
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC LIMIT 10
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Ошибка БД при загрузке лидеров: {e}")
        return []

def get_personal_best(player_id):
    """Запрашивает лучший результат конкретного игрока"""
    if player_id is None: return 0
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
        res = cur.fetchone()[0]
        cur.close()
        conn.close()
        return res if res else 0
    except Exception as e:
        print(f"Ошибка БД при получении личного рекорда: {e}")
        return 0