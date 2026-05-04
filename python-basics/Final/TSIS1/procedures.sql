-- ==========================================================
-- ХРАНИМЫЕ ПРОЦЕДУРЫ И ФУНКЦИИ ДЛЯ ТЕЛЕФОННОЙ КНИГИ
-- ==========================================================

-- Удаляем старые версии объектов, чтобы избежать конфликтов при обновлении
DROP FUNCTION IF EXISTS get_contacts_paginated(integer, integer, text, text);
DROP FUNCTION IF EXISTS search_contacts(text);
DROP PROCEDURE IF EXISTS add_phone(varchar, varchar, varchar);
DROP PROCEDURE IF EXISTS move_to_group(varchar, varchar);
DROP PROCEDURE IF EXISTS delete_contact(varchar);
DROP PROCEDURE IF EXISTS update_contact(varchar, varchar, varchar);

-- 1. ФУНКЦИЯ ПАГИНАЦИИ (Постраничный вывод)
-- Позволяет выводить список частями, сортировать их и фильтровать по группе
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_lim INT,            -- Сколько записей показать
    p_offs INT,           -- Сколько записей пропустить
    p_sort_col TEXT,      -- По какому столбцу сортировать (name/birthday/id)
    p_filter_group TEXT   -- Название группы для фильтрации
)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, birthday TEXT, group_name VARCHAR, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id, 
        c.name, 
        COALESCE(c.email, 'нет'),                     -- Если email NULL, пишем 'нет'
        COALESCE(c.birthday::text, 'нет'),            -- Если даты нет, пишем 'нет'
        COALESCE(g.name, 'Без группы'),               -- Если группы нет, пишем 'Без группы'
        COALESCE(string_agg(DISTINCT p.phone, ', '), 'нет номера') -- Собираем все номера в одну строку через запятую
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id           -- Присоединяем таблицу групп
    LEFT JOIN phones p ON c.id = p.contact_id         -- Присоединяем таблицу номеров
    WHERE (p_filter_group = '' OR g.name ILIKE p_filter_group) -- Фильтрация (регистр не важен)
    GROUP BY c.id, g.name                             -- Группируем, чтобы номера не дублировали строки с именами
    ORDER BY 
        CASE WHEN p_sort_col = 'name' THEN c.name END ASC,
        CASE WHEN p_sort_col = 'birthday' THEN c.birthday::text END ASC,
        CASE WHEN p_sort_col = 'id' THEN c.id::text END ASC
    LIMIT p_lim OFFSET p_offs;                         -- Сама пагинация
END;
$$ LANGUAGE plpgsql;

-- 2. УНИВЕРСАЛЬНЫЙ ПОИСК
-- Ищет совпадения по имени, почте или любому из номеров телефона
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
    WHERE c.name ILIKE '%' || p_query || '%'          -- Поиск по части имени
       OR c.email ILIKE '%' || p_query || '%'         -- Поиск по части почты (например, 'gmail')
       OR p.phone ILIKE '%' || p_query || '%'         -- Поиск по цифрам номера
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;

-- 3. ДОБАВЛЕНИЕ НОМЕРА ТЕЛЕФОНА
-- Находит контакт по имени и добавляет ему новый телефон, если такого еще нет
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

-- 4. ПЕРЕНОС В ГРУППУ / СОЗДАНИЕ ГРУППЫ
-- Создает группу, если её нет, и привязывает её к контакту
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
AS $$
DECLARE v_g_id INT;
BEGIN
    -- Создаем группу, если её не существует
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    -- Берем её ID
    SELECT id INTO v_g_id FROM groups WHERE name = p_group_name;
    -- Привязываем контакт к этой группе (или создаем контакт, если это новый человек)
    INSERT INTO contacts (name, group_id) VALUES (p_contact_name, v_g_id)
    ON CONFLICT (name) DO UPDATE SET group_id = v_g_id;
END;
$$ LANGUAGE plpgsql;

-- 5. УДАЛЕНИЕ КОНТАКТА
-- Сначала удаляет все номера человека, а потом его самого (каскадное удаление вручную)
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

-- 6. ОБНОВЛЕНИЕ ДАННЫХ КОНТАКТА
CREATE OR REPLACE PROCEDURE update_contact(p_name VARCHAR, p_email VARCHAR, p_birthday VARCHAR)
AS $$
BEGIN
    UPDATE contacts SET email = p_name, birthday = p_birthday::DATE WHERE name = p_name;
END;
$$ LANGUAGE plpgsql;