import psycopg2
from connect import get_connection

def call_search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    # Вызываем функцию из базы
    cur.execute("SELECT * FROM search_pattern(%s::text)", (pattern,))
    rows = cur.fetchall()
import psycopg2
from connect import get_connection

def call_search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_pattern(%s::text)", (pattern,))
    rows = cur.fetchall()
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")
    cur.close()
    conn.close()

def call_insert_or_update(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s::text, %s::text)", (name, phone))
    conn.commit()
    print("--- Успешно обновлено/добавлено ---")
    cur.close()
    conn.close()

def call_insert_many():
    print("\n--- Массовое добавление ---")
    names_raw = input("Введите имена через запятую: ")
    phones_raw = input("Введите телефоны через запятую: ")

    names = [n.strip() for n in names_raw.split(",") if n.strip()]
    phones = [p.strip() for p in phones_raw.split(",") if p.strip()]

    if len(names) != len(phones):
        print("Ошибка: количество имен и телефонов не совпадает!")
        return

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL insert_many_users(%s::text[], %s::text[])", (names, phones))
        conn.commit()
        if conn.notices:
            for notice in conn.notices:
                print(f"⚠️ {notice.strip()}")
        print("--- Обработка списка завершена ---")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()

def call_pagination(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s::int, %s::int)", (limit, offset))
    rows = cur.fetchall()
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")
    cur.close()
    conn.close()

def call_delete(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_by_value(%s::text)", (value,))
    conn.commit()
    print(f"--- Контакт {value} удален ---")
    cur.close()
    conn.close()

if __name__ == "__main__":
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Search")
        print("2. Insert/Update Single")
        print("3. Insert Many (Manual Input)")
        print("4. Pagination")
        print("5. Delete")
        print("0. Exit")

        choice = input(">> ")

        if choice == "1":
            call_search(input("Pattern: "))
        elif choice == "2":
            call_insert_or_update(input("Name: "), input("Phone: "))
        elif choice == "3":
            call_insert_many()
        elif choice == "4":
            l = int(input("Limit: "))
            o = int(input("Offset: "))
            call_pagination(l, o)
        elif choice == "5":
            call_delete(input("Value: "))
        elif choice == "0":
            break