from connect import get_connection

def initialize_database():
    conn = get_connection()
    cur = conn.cursor()
    
    # Читаем код из functions.sql
    with open('functions.sql', 'r', encoding='utf-8') as f:
        functions_sql = f.read()
        cur.execute(functions_sql)
    
    # Читаем код из procedures.sql
    with open('procedures.sql', 'r', encoding='utf-8') as f:
        procedures_sql = f.read()
        cur.execute(procedures_sql)
        
    conn.commit()
    print("--- Все функции и процедуры успешно созданы в базе данных! ---")
    cur.close()
    conn.close()

if __name__ == "__main__":
    initialize_database()