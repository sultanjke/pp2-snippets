CREATE OR REPLACE FUNCTION fn_search_contacts(p_pattern TEXT)
RETURNS TABLE (
    contact_id INT,
    first_name TEXT,
    surname TEXT,
    phone TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_pattern TEXT := COALESCE(TRIM(p_pattern), '');
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name::TEXT,
        c.surname::TEXT,
        c.phone::TEXT
    FROM contacts AS c
    WHERE
        c.first_name ILIKE '%' || v_pattern || '%'
        OR c.surname ILIKE '%' || v_pattern || '%'
        OR c.phone LIKE '%' || v_pattern || '%'
    ORDER BY c.id;
END;
$$;


CREATE OR REPLACE FUNCTION fn_get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (
    contact_id INT,
    first_name TEXT,
    surname TEXT,
    phone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_limit IS NULL OR p_limit <= 0 THEN
        RAISE EXCEPTION 'LIMIT must be greater than 0';
    END IF;

    IF p_offset IS NULL OR p_offset < 0 THEN
        RAISE EXCEPTION 'OFFSET must be >= 0';
    END IF;

    RETURN QUERY
    SELECT
        c.id,
        c.first_name::TEXT,
        c.surname::TEXT,
        c.phone::TEXT
    FROM contacts AS c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;

