CREATE OR REPLACE PROCEDURE sp_upsert_user(
    IN p_first_name TEXT,
    IN p_surname TEXT,
    IN p_phone TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
    v_first_name TEXT := TRIM(COALESCE(p_first_name, ''));
    v_surname TEXT := TRIM(COALESCE(p_surname, ''));
    v_phone TEXT := TRIM(COALESCE(p_phone, ''));
BEGIN
    IF v_first_name = '' THEN
        RAISE EXCEPTION 'first_name cannot be empty';
    END IF;

    IF v_phone !~ E'^\\+?[0-9][0-9\\-\\s]{3,31}$' THEN
        RAISE EXCEPTION 'invalid phone format: %', v_phone;
    END IF;

    SELECT c.id
    INTO v_contact_id
    FROM contacts AS c
    WHERE c.first_name = v_first_name
      AND c.surname = v_surname
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        INSERT INTO contacts (first_name, surname, phone)
        VALUES (v_first_name, v_surname, v_phone);
    ELSE
        UPDATE contacts
        SET phone = v_phone
        WHERE id = v_contact_id;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE sp_insert_many_users(
    IN p_first_names TEXT[],
    IN p_surnames TEXT[],
    IN p_phones TEXT[],
    INOUT p_invalid_data TEXT[] DEFAULT ARRAY[]::TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_i INT;
    v_first_name TEXT;
    v_surname TEXT;
    v_phone TEXT;
BEGIN
    IF p_first_names IS NULL OR p_surnames IS NULL OR p_phones IS NULL THEN
        RAISE EXCEPTION 'All arrays are required (first_names, surnames, phones)';
    END IF;

    IF array_length(p_first_names, 1) IS DISTINCT FROM array_length(p_surnames, 1)
        OR array_length(p_first_names, 1) IS DISTINCT FROM array_length(p_phones, 1)
    THEN
        RAISE EXCEPTION 'Array sizes must match';
    END IF;

    IF p_invalid_data IS NULL THEN
        p_invalid_data := ARRAY[]::TEXT[];
    END IF;

    FOR v_i IN 1..COALESCE(array_length(p_first_names, 1), 0) LOOP
        v_first_name := TRIM(COALESCE(p_first_names[v_i], ''));
        v_surname := TRIM(COALESCE(p_surnames[v_i], ''));
        v_phone := TRIM(COALESCE(p_phones[v_i], ''));

        IF v_first_name = '' THEN
            p_invalid_data := array_append(
                p_invalid_data,
                FORMAT('row %s: empty first_name', v_i)
            );
        ELSIF v_phone !~ E'^\\+?[0-9][0-9\\-\\s]{3,31}$' THEN
            p_invalid_data := array_append(
                p_invalid_data,
                FORMAT(
                    'row %s: %s %s -> invalid phone [%s]',
                    v_i,
                    v_first_name,
                    v_surname,
                    v_phone
                )
            );
        ELSE
            CALL sp_upsert_user(v_first_name, v_surname, v_phone);
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE sp_delete_user(
    IN p_username TEXT DEFAULT NULL,
    IN p_phone TEXT DEFAULT NULL,
    INOUT p_deleted_count INT DEFAULT 0
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_username TEXT := NULLIF(TRIM(COALESCE(p_username, '')), '');
    v_phone TEXT := NULLIF(TRIM(COALESCE(p_phone, '')), '');
BEGIN
    IF v_username IS NULL AND v_phone IS NULL THEN
        RAISE EXCEPTION 'Provide username or phone';
    END IF;

    DELETE FROM contacts AS c
    WHERE
        (v_username IS NOT NULL AND LOWER(c.first_name) = LOWER(v_username))
        OR (v_phone IS NOT NULL AND c.phone = v_phone);

    GET DIAGNOSTICS p_deleted_count = ROW_COUNT;
END;
$$;
