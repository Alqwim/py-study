from connect import get_connection

def run_sql_file(filename, cursor):
    print(f"Выполняю {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        sql = f.read()
        # Проверяем, что файл не пустой
        if sql.strip():
            cursor.execute(sql)
        else:
            print(f"Предупреждение: Файл {filename} пуст.")

def initialize_database():
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Важно: сначала schema, потом procedures
        run_sql_file('schema.sql', cur)
        run_sql_file('procedures.sql', cur)
        
        conn.commit()
        print("--- База данных успешно обновлена! ---")
    except Exception as e:
        print(f"Ошибка при обновлении: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    initialize_database()