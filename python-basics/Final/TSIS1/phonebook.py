import json
import csv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from connect import get_connection

# Функция для получения правильного пути к файлам относительно папки со скриптом
def get_full_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)

# --- ИМПОРТ / ЭКСПОРТ ДАННЫХ ---

def import_csv(file_path="contacts.csv"):
    """ Читает CSV файл и вызывает SQL процедуры для заполнения таблиц """
    path = get_full_path(file_path)
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 1. Создаем группу и контакт
                cur.execute("CALL move_to_group(%s, %s)", (row['name'], row.get('group', 'Other')))
                # 2. Обновляем email и дату
                email = row.get('email') if row.get('email') else None
                birthday = row.get('birthday') if row.get('birthday') else None
                cur.execute("CALL update_contact(%s, %s, %s)", (row['name'], email, birthday))
                # 3. Добавляем номер телефона
                cur.execute("CALL add_phone(%s, %s, %s)", (row['name'], row['phone'], row.get('phone_type', 'mobile')))
        conn.commit()
        print("\n✅ Импорт из CSV успешно завершен!")
    except Exception as e:
        print(f"Ошибка CSV: {e}")
        conn.rollback()
    finally:
        cur.close(); conn.close()

def export_json(filename="contacts.json"):
    """ Выгружает ВСЕ контакты из базы в JSON файл """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor) # Используем словарь для удобства JSON
    cur.execute("SELECT * FROM search_contacts('')")
    data = cur.fetchall()
    with open(get_full_path(filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Данные сохранены в {filename}")
    cur.close(); conn.close()

def import_json(filename="contacts.json"):
    """ Читает JSON и обновляет базу, спрашивая пользователя о дубликатах """
    path = get_full_path(filename)
    if not os.path.exists(path):
        print("❌ Файл JSON не найден! Сначала сделайте экспорт.")
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        for c in data:
            # Проверяем наличие контакта в базе
            cur.execute("SELECT id FROM contacts WHERE name = %s", (c['name'],))
            if cur.fetchone():
                choice = input(f"⚠️ {c['name']} уже существует. Перезаписать данные? (y/n): ").lower()
                if choice != 'y': continue
                cur.execute("CALL delete_contact(%s)", (c['name'],)) # Удаляем старое перед перезаписью
            
            # Записываем новые данные
            cur.execute("CALL move_to_group(%s, %s)", (c['name'], c['group_name']))
            cur.execute("CALL update_contact(%s, %s, %s)", (c['name'], c['email'], c['birthday']))
            
            # Разбираем строку телефонов обратно на номера и типы
            for p_str in c['phones'].split(', '):
                if '(' in p_str:
                    p_num = p_str.split(' (')[0]
                    p_type = p_str.split(' (')[1].replace(')', '')
                    cur.execute("CALL add_phone(%s, %s, %s)", (c['name'], p_num, p_type))
        conn.commit()
        print("✅ Данные из JSON успешно загружены!")
    except Exception as e:
        print(f"Ошибка JSON: {e}"); conn.rollback()
    finally:
        cur.close(); conn.close()

# --- МЕНЮ УПРАВЛЕНИЯ (CRUD) ---

def manage_contacts():
    """ Меню для ручного создания, изменения или удаления записей """
    print("\n1. Добавить | 2. Изменить | 3. Удалить")
    cmd = input(">> ")
    conn = get_connection(); cur = conn.cursor()
    
    name = input("Имя контакта: ")
    if cmd in ['1', '2']:
        group = input("Группа: ")
        email = input("Email: ")
        bday = input("Дата рождения (ГГГГ-ММ-ДД): ")
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        cur.execute("CALL update_contact(%s, %s, %s)", (name, email, bday))
        print("✅ Контакт обработан!")
    elif cmd == '3':
        cur.execute("CALL delete_contact(%s)", (name,))
        print("❌ Контакт удален из базы.")
    
    conn.commit(); cur.close(); conn.close()

def paginated_view():
    """ Просмотр списка с пагинацией, сортировкой и фильтрами """
    limit = 3
    offset = 0
    
    print("\nНастройка отображения:")
    sort_choice = input("Сортировка (1-имя, 2-ДР, 3-ID): ")
    sort_map = {'1': 'name', '2': 'birthday', '3': 'id'}
    sort_col = sort_map.get(sort_choice, 'id')
    f_group = input("Фильтр по группе (Enter - все): ")

    while True:
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s, %s, %s)", (limit, offset, sort_col, f_group))
        rows = cur.fetchall()
        
        print("\n" + "="*60 + "\nТЕКУЩИЙ СПИСОК\n" + "="*60)
        if not rows: print("[Нет данных для отображения]")
        for r in rows:
            print(f"🆔 {r[0]} | 👤 {r[1]} | 👥 Группа: {r[4]}")
            print(f"   📧 Почта: {r[2]} | 🎂 ДР: {r[3]}")
            print(f"   📞 Телефоны: {r[5]}")
            print("-" * 40)
        
        move = input("\n[n]ext - вперед, [p]rev - назад, [q]uit - меню: ").lower()
        if move == 'n': offset += limit
        elif move == 'p': offset = max(0, offset - limit)
        elif move == 'q': break
        cur.close(); conn.close()

# --- ГЛАВНЫЙ ЦИКЛ ПРОГРАММЫ ---

def main_menu():
    while True:
        print("\n=== ГЛАВНОЕ МЕНЮ (TSIS 1) ===")
        print("1. Найти контакт")
        print("2. Список (Пагинация)")
        print("3. Экспорт в JSON")
        print("4. Импорт из CSV")
        print("5. Импорт из JSON")
        print("6. Управление (Add/Edit/Del)")
        print("0. Выход")
        
        choice = input(">> ")
        if choice == '1':
            q = input("Введите имя, почту или телефон: ")
            conn = get_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM search_contacts(%s)", (q,))
            results = cur.fetchall()
            if not results: print("Ничего не найдено.")
            for r in results:
                print(f"\n👤 {r['name']} [{r['group_name']}]\n📧 {r['email']} | 🎂 {r['birthday']}\n📞 {r['phones']}")
            cur.close(); conn.close()
        elif choice == '2': paginated_view()
        elif choice == '3': export_json()
        elif choice == '4': import_csv()
        elif choice == '5': import_json()
        elif choice == '6': manage_contacts()
        elif choice == '0': break

if __name__ == "__main__":
    main_menu()