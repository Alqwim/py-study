# db.py
import psycopg2
from config import DB_CONFIG

def get_connection():
    conn_str = f"dbname='{DB_CONFIG['dbname']}' user='{DB_CONFIG['user']}' password='{DB_CONFIG['password']}' host='{DB_CONFIG['host']}' port='{DB_CONFIG['port']}' options='-c client_encoding=UTF8'"
    return psycopg2.connect(conn_str)

def create_tables():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id       SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
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
        print(f"DB Error (create_tables): {e}")

def get_or_create_player(username):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        conn.commit()
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return player_id
    except Exception as e:
        print(f"DB Error (get_player): {e}")
        return None

def save_game(player_id, score, level):
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
        print(f"DB Error (save_game): {e}")

def get_leaderboard():
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
        print(f"DB Error (leaderboard): {e}")
        return []

def get_personal_best(player_id):
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
        print(f"DB Error (pb): {e}")
        return 0