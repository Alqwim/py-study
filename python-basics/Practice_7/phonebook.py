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
            next(reader)
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
    """Обновляет данные контакта."""
    conn = get_connection()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE contacts SET name=%s WHERE name=%s", (new_name, target_name))
    if new_phone:
        current_name = new_name if new_name else target_name
        cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, current_name))
    conn.commit()
    cur.close()
    conn.close()
    print(f"--- Данные контакта {target_name} обновлены ---")

def search_contacts(name=None, phone_prefix=None, reverse=False):
    """
    Поиск по фильтрам с выбором направления сортировки.
    reverse=False: А-Я (ASC)
    reverse=True: Я-А (DESC)
    """
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
    
    # Выбираем направление сортировки
    order = "DESC" if reverse else "ASC"
    query += f" ORDER BY name {order}"
    
    cur.execute(query, tuple(params))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def delete_contact(name=None, phone=None):
    """Удаляет контакт."""
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
        print("4. Список контактов / Поиск")
        print("5. Удалить контакт")
        print("0. Выход")
        
        choice = input("Выберите действие: ")

        if choice == '1':
            path = input("Введите путь к CSV: ")
            insert_from_csv(path)
        
        elif choice == '2':
            name = input("Имя: ")
            phone = input("Телефон: ")
            insert_manual(name, phone)
        
        elif choice == '3':
            target = input("Имя контакта для изменения: ")
            n_name = input("Новое имя (Enter чтобы пропустить): ")
            n_phone = input("Новый телефон (Enter чтобы пропустить): ")
            update_contact(target, n_name if n_name else None, n_phone if n_phone else None)
        
        elif choice == '4':
            print("\nНастройки отображения:")
            print("1. По алфавиту (А-Я)")
            print("2. В обратном порядке (Я-А)")
            order_choice = input("> ")
            is_reverse = True if order_choice == '2' else False

            print("\nФильтр:")
            print("1. Показать всех")
            print("2. Поиск по имени")
            print("3. Поиск по номеру")
            filter_choice = input("> ")

            results = []
            if filter_choice == '2':
                n = input("Введите имя: ")
                results = search_contacts(name=n, reverse=is_reverse)
            elif filter_choice == '3':
                p = input("Введите префикс: ")
                results = search_contacts(phone_prefix=p, reverse=is_reverse)
            else:
                results = search_contacts(reverse=is_reverse)
            
            # Вывод результата
            print(f"\n{'Имя':<20} | {'Телефон':<15}")
            print("-" * 40)
            for r_name, r_phone in results:
                print(f"{r_name:<20} | {r_phone:<15}")
        
        elif choice == '5':
            name = input("Введите имя для удаления: ")
            delete_contact(name if name else None)
        
        elif choice == '0':
            break

if __name__ == "__main__":
    main_menu()