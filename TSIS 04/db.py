import psycopg2

# Edit these credentials to match your local PostgreSQL setup
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "postgres",
    "user":     "postgres",
    "password": "your_password_here",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def ensure_tables():
    sql = """
    CREATE TABLE IF NOT EXISTS players (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS game_sessions (
        id            SERIAL PRIMARY KEY,
        player_id     INTEGER REFERENCES players(id),
        score         INTEGER   NOT NULL,
        level_reached INTEGER   NOT NULL,
        played_at     TIMESTAMP DEFAULT NOW()
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


def get_or_create_player(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            row = cur.fetchone()
            if row:
                return row[0]
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id", (username,)
            )
            player_id = cur.fetchone()[0]
        conn.commit()
    return player_id


def save_result(username, score, level):
    player_id = get_or_create_player(username)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                (player_id, score, level),
            )
        conn.commit()


def get_leaderboard():
    # Returns list of (username, score, level_reached, played_at)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.username, s.score, s.level_reached,
                       TO_CHAR(s.played_at, 'YYYY-MM-DD') AS day
                FROM game_sessions s
                JOIN players p ON s.player_id = p.id
                ORDER BY s.score DESC
                LIMIT 10
            """)
            return cur.fetchall()


def get_personal_best(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(s.score)
                FROM game_sessions s
                JOIN players p ON s.player_id = p.id
                WHERE p.username = %s
            """, (username,))
            row = cur.fetchone()
    return row[0] if row and row[0] is not None else 0
