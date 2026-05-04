-- Сначала удаляем старое, чтобы избежать конфликтов имен и типов
DROP FUNCTION IF EXISTS get_contacts_paginated(integer, integer, text, text);
DROP FUNCTION IF EXISTS search_contacts(text);
DROP PROCEDURE IF EXISTS add_phone(varchar, varchar, varchar);
DROP PROCEDURE IF EXISTS move_to_group(varchar, varchar);
DROP PROCEDURE IF EXISTS delete_contact(varchar);
DROP PROCEDURE IF EXISTS update_contact(varchar, varchar, varchar);

-- 1. УМНАЯ ПАГИНАЦИЯ (Сортировка + Фильтр по группе)
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_lim INT, 
    p_offs INT, 
    p_sort_col TEXT, 
    p_filter_group TEXT
)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, birthday TEXT, group_name VARCHAR, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id, 
        c.name, 
        COALESCE(c.email, 'нет'), 
        COALESCE(c.birthday::text, 'нет'),
        COALESCE(g.name, 'Без группы'),
        COALESCE(string_agg(DISTINCT p.phone, ', '), 'нет номера')
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE (p_filter_group = '' OR g.name ILIKE p_filter_group)
    GROUP BY c.id, g.name
    ORDER BY 
        CASE WHEN p_sort_col = 'name' THEN c.name END ASC,
        CASE WHEN p_sort_col = 'birthday' THEN c.birthday::text END ASC,
        CASE WHEN p_sort_col = 'id' THEN c.id::text END ASC
    LIMIT p_lim OFFSET p_offs;
END;
$$ LANGUAGE plpgsql;

-- 2. УНИВЕРСАЛЬНЫЙ ПОИСК (Имя, Почта, Телефоны)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name VARCHAR, email VARCHAR, birthday TEXT, group_name VARCHAR, phones TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.name, 
        COALESCE(c.email, 'нет'), 
        COALESCE(c.birthday::text, 'нет'),
        COALESCE(g.name, 'Без группы'),
        COALESCE(string_agg(DISTINCT p.phone || ' (' || p.type || ')', ', '), 'нет номера')
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%' 
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;

-- 3. ДОБАВЛЕНИЕ НОМЕРА
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
AS $$
DECLARE v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name;
    IF v_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM phones WHERE contact_id = v_id AND phone = p_phone) THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 4. СМЕНА ГРУППЫ / СОЗДАНИЕ КОНТАКТА
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
AS $$
DECLARE v_g_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_g_id FROM groups WHERE name = p_group_name;
    INSERT INTO contacts (name, group_id) VALUES (p_contact_name, v_g_id)
    ON CONFLICT (name) DO UPDATE SET group_id = v_g_id;
END;
$$ LANGUAGE plpgsql;

-- 5. УДАЛЕНИЕ КОНТАКТА (Безопасное)
CREATE OR REPLACE PROCEDURE delete_contact(p_contact_name VARCHAR)
AS $$
DECLARE v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name;
    IF v_id IS NOT NULL THEN
        DELETE FROM phones WHERE contact_id = v_id;
        DELETE FROM contacts WHERE id = v_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 6. ОБНОВЛЕНИЕ ДАННЫХ
CREATE OR REPLACE PROCEDURE update_contact(p_name VARCHAR, p_email VARCHAR, p_birthday VARCHAR)
AS $$
BEGIN
    UPDATE contacts SET email = p_email, birthday = p_birthday::DATE WHERE name = p_name;
END;
$$ LANGUAGE plpgsql;