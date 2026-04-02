from connect import get_connection

def call_search(pattern):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    cur.close()
    conn.close()


def call_insert_or_update(name, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()

    cur.close()
    conn.close()


def call_insert_many():
    names = ["Ali", "Bob", "Test"]
    phones = ["+7700", "abc", "+12345"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()

    cur.close()
    conn.close()


def call_pagination(limit, offset):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    cur.close()
    conn.close()


def call_delete(value):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_by_value(%s)", (value,))
    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    while True:
        print("\n1. Search")
        print("2. Insert/Update")
        print("3. Insert many")
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
            call_pagination(int(input("Limit: ")), int(input("Offset: ")))
        elif choice == "5":
            call_delete(input("Value: "))
        elif choice == "0":
            break