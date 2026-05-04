import json
import csv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from connect import get_connection

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def get_full_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)

# --- ИМПОРТ / ЭКСПОРТ ---

def import_csv(file_path="contacts.csv"):
    path = get_full_path(file_path)
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("CALL move_to_group(%s, %s)", (row['name'], row.get('group', 'Other')))
                email = row.get('email') if row.get('email') else None
                birthday = row.get('birthday') if row.get('birthday') else None
                cur.execute("CALL update_contact(%s, %s, %s)", (row['name'], email, birthday))
                cur.execute("CALL add_phone(%s, %s, %s)", (row['name'], row['phone'], row.get('phone_type', 'mobile')))
        conn.commit()
        print("\n✅ Импорт из CSV завершен!")
    except Exception as e:
        print(f"Ошибка CSV: {e}")
        conn.rollback()
    finally:
        cur.close(); conn.close()

def export_json(filename="contacts.json"):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM search_contacts('')")
    data = cur.fetchall()
    with open(get_full_path(filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Данные экспортированы в {filename}")
    cur.close(); conn.close()

def import_json(filename="contacts.json"):
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
            cur.execute("SELECT id FROM contacts WHERE name = %s", (c['name'],))
            if cur.fetchone():
                choice = input(f"⚠️ {c['name']} уже есть. Перезаписать? (y/n): ").lower()
                if choice != 'y': continue
                cur.execute("CALL delete_contact(%s)", (c['name'],)) # Чистим перед записью
            
            cur.execute("CALL move_to_group(%s, %s)", (c['name'], c['group_name']))
            cur.execute("CALL update_contact(%s, %s, %s)", (c['name'], c['email'], c['birthday']))
            # Восстанавливаем телефоны из строки "+7... (type), +7..."
            for p_str in c['phones'].split(', '):
                if '(' in p_str:
                    p_num = p_str.split(' (')[0]
                    p_type = p_str.split(' (')[1].replace(')', '')
                    cur.execute("CALL add_phone(%s, %s, %s)", (c['name'], p_num, p_type))
        conn.commit()
        print("✅ Импорт из JSON завершен!")
    except Exception as e:
        print(f"Ошибка JSON: {e}"); conn.rollback()
    finally:
        cur.close(); conn.close()

# --- ОСНОВНЫЕ ДЕЙСТВИЯ ---

def manage_contacts():
    print("\n1. Добавить | 2. Изменить | 3. Удалить")
    cmd = input(">> ")
    conn = get_connection(); cur = conn.cursor()
    name = input("Имя контакта: ")
    if cmd == '1' or cmd == '2':
        group = input("Группа: ")
        email = input("Email: ")
        bday = input("ДР (ГГГГ-ММ-ДД): ")
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        cur.execute("CALL update_contact(%s, %s, %s)", (name, email, bday))
        print("✅ Выполнено!")
    elif cmd == '3':
        cur.execute("CALL delete_contact(%s)", (name,))
        print("❌ Удалено.")
    conn.commit(); cur.close(); conn.close()

def paginated_view():
    limit = 3; offset = 0
    sort_choice = input("\nСортировка (1-имя, 2-ДР, 3-ID): ")
    sort_map = {'1': 'name', '2': 'birthday', '3': 'id'}
    sort_col = sort_map.get(sort_choice, 'id')
    f_group = input("Фильтр по группе (Enter - все): ")

    while True:
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s, %s, %s)", (limit, offset, sort_col, f_group))
        rows = cur.fetchall()
        print("\n" + "="*50 + "\nСПИСОК КОНТАКТОВ\n" + "="*50)
        if not rows: print("[Пусто]")
        for r in rows:
            print(f"🆔 {r[0]} | 👤 {r[1]} | 👥 {r[4]}\n   📧 {r[2]} | 🎂 {r[3]}\n   📞 {r[5]}\n" + "-"*30)
        
        move = input("\n[n]ext, [p]rev, [q]uit: ").lower()
        if move == 'n': offset += limit
        elif move == 'p': offset = max(0, offset - limit)
        elif move == 'q': break
        cur.close(); conn.close()

def main_menu():
    while True:
        print("\n=== TSIS 1: FINAL EDITION ===")
        print("1. Поиск | 2. Список (Пагинация) | 3. JSON Экспорт | 4. CSV Импорт | 5. JSON Импорт | 6. Управление | 0. Выход")
        c = input(">> ")
        if c == '1':
            q = input("Запрос: ")
            conn = get_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM search_contacts(%s)", (q,))
            for r in cur.fetchall():
                print(f"\n👤 {r['name']} [{r['group_name']}]\n📧 {r['email']} | 🎂 {r['birthday']}\n📞 {r['phones']}")
            cur.close(); conn.close()
        elif c == '2': paginated_view()
        elif c == '3': export_json()
        elif c == '4': import_csv()
        elif c == '5': import_json()
        elif c == '6': manage_contacts()
        elif c == '0': break

if __name__ == "__main__":
    main_menu()