import csv
import sys
# Импортируем напрямую, так как файлы в одной папке
try:
    from connect import get_connection
except ImportError:
    print("Ошибка: Не найден файл connect.py в текущей директории.")
    sys.exit(1)

def create_table():
    """Создает таблицу, если она еще не существует."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        phone VARCHAR(20) NOT NULL
    )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("--- Таблица готова к работе ---")

def insert_from_csv(file_path):
    """Загружает данные из CSV файла."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Пропускаем заголовок
            rows = [tuple(row) for row in reader]
            cur.executemany("INSERT INTO contacts (name, phone) VALUES (%s, %s)", rows)
        conn.commit()
        cur.close()
        conn.close()
        print(f"--- Успешно импортировано из {file_path} ---")
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")

def insert_manual(name, phone):
    """Добавляет контакт вручную."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print(f"--- Контакт {name} добавлен ---")

def update_contact(target_name, new_name=None, new_phone=None):
    """Обновляет имя или телефон по текущему имени контакта."""
    conn = get_connection()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE contacts SET name=%s WHERE name=%s", (new_name, target_name))
    if new_phone:
        # Если имя тоже менялось, обновляем по новому имени, иначе по старому
        current_name = new_name if new_name else target_name
        cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, current_name))
    conn.commit()
    cur.close()
    conn.close()
    print(f"--- Данные контакта {target_name} обновлены ---")

def search_contacts(name=None, phone_prefix=None):
    """Поиск по фильтрам (имя или префикс телефона)."""
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT name, phone FROM contacts WHERE TRUE"
    params = []
    if name:
        query += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if phone_prefix:
        query += " AND phone LIKE %s"
        params.append(f"{phone_prefix}%")
    
    cur.execute(query, tuple(params))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def delete_contact(name=None, phone=None):
    """Удаляет контакт по имени или номеру телефона."""
    conn = get_connection()
    cur = conn.cursor()
    if name:
        cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
    elif phone:
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"--- Контакт удален ---")

def main_menu():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Импорт из CSV")
        print("2. Добавить контакт вручную")
        print("3. Обновить контакт")
        print("4. Поиск (по имени/телефону)")
        print("5. Удалить контакт")
        print("0. Выход")
        
        choice = input("Выберите действие: ")

        if choice == '1':
            path = input("Введите путь к CSV (например, contacts.csv): ")
            insert_from_csv(path)
        
        elif choice == '2':
            name = input("Имя: ")
            phone = input("Телефон: ")
            insert_manual(name, phone)
        
        elif choice == '3':
            target = input("Имя контакта, который нужно изменить: ")
            n_name = input("Новое имя (оставьте пустым, если не меняется): ")
            n_phone = input("Новый телефон (оставьте пустым, если не меняется): ")
            update_contact(target, n_name if n_name else None, n_phone if n_phone else None)
        
        elif choice == '4':
            print("1. Поиск по имени")
            print("2. Поиск по префиксу телефона")
            sub = input("> ")
            if sub == '1':
                name = input("Введите имя: ")
                print(search_contacts(name=name))
            else:
                pref = input("Введите префикс (напр. +7707): ")
                print(search_contacts(phone_prefix=pref))
        
        elif choice == '5':
            name = input("Введите имя для удаления (или оставьте пустым): ")
            phone = input("Введите телефон для удаления (если имя пустое): ")
            delete_contact(name if name else None, phone if phone else None)
        
        elif choice == '0':
            break

if __name__ == "__main__":
    main_menu()