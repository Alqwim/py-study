-- 1. Вставить или обновить одного
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

-- 2. Вставить много с циклом и валидацией
CREATE OR REPLACE PROCEDURE insert_many_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        -- Проверка регулярным выражением (только цифры и +)
        IF phones[i] ~ '^\+?[0-9]+$' THEN
            IF EXISTS (SELECT 1 FROM contacts WHERE name = names[i]) THEN
                UPDATE contacts SET phone = phones[i] WHERE name = names[i];
            ELSE
                INSERT INTO contacts(name, phone) VALUES (names[i], phones[i]);
            END IF;
        ELSE
            -- Если телефон — фигня, просто кидаем текст в консоль Python
            RAISE NOTICE 'Invalid phone for user %: %', names[i], phones[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Удаление
CREATE OR REPLACE PROCEDURE delete_by_value(p_value TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_value OR phone = p_value;
END;
$$;