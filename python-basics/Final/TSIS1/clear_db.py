from connect import get_connection

def clear():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE IF EXISTS phones, contacts, groups CASCADE;")
        conn.commit()
        print("--- База очищена! Таблицы удалены. ---")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    clear()