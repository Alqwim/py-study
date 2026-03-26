# phonebook.py
import csv
from Practice_7.connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        phone VARCHAR(20)
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # если есть заголовок
        rows = [tuple(row) for row in reader]
        cur.executemany("INSERT INTO contacts (name, phone) VALUES (%s, %s)", rows)
    conn.commit()
    cur.close()
    conn.close()

def insert_manual(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def update_contact(old_name=None, old_phone=None, new_name=None, new_phone=None):
    conn = get_connection()
    cur = conn.cursor()
    if old_name:
        cur.execute("UPDATE contacts SET name=%s WHERE name=%s", (new_name, old_name))
    if old_phone:
        cur.execute("UPDATE contacts SET phone=%s WHERE phone=%s", (new_phone, old_phone))
    conn.commit()
    cur.close()
    conn.close()

def search_contacts(name=None, phone_prefix=None):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM contacts WHERE TRUE"
    params = []
    if name:
        query += " AND name LIKE %s"
        params.append(f"{name}%")
    if phone_prefix:
        query += " AND phone LIKE %s"
        params.append(f"{phone_prefix}%")
    cur.execute(query, tuple(params))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def delete_contact(name=None, phone=None):
    conn = get_connection()
    cur = conn.cursor()
    if name and phone:
        cur.execute("DELETE FROM contacts WHERE name=%s OR phone=%s", (name, phone))
    elif name:
        cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
    elif phone:
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
    conn.commit()
    cur.close()
    conn.close()

# ---------------- Пример использования ----------------
if __name__ == "__main__":
    create_table()
    
    # вставка из CSV
    insert_from_csv("contacts.csv")
    
    # ручная вставка
    insert_manual("NewUser", "+77001234567")
    
    # обновление контакта
    update_contact(old_name="NewUser", new_name="UpdatedUser")
    
    # поиск контактов
    print("По имени 'Aya':", search_contacts(name="Aya"))
    print("По телефону +7:", search_contacts(phone_prefix="+7"))
    
    # удаление контакта
    delete_contact(name="UpdatedUser")