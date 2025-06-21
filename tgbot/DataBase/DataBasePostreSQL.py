import psycopg2
from tgbot.DataBase.DataBaseInterface import DataBaseInterface

class DataBasePostgreSQL(DataBaseInterface):
    def __init__(self, database_url):
        super().__init__()
        self.database_url = database_url
        self.__create_table()

    def get_persons(self, chat_id):
        conn = self.__get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT name FROM users WHERE chat_id = %s ORDER BY position", (chat_id,))
        persons = [row[0] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return persons

    def add_person(self, chat_id, name):
        conn = self.__get_db_connection()
        cur = conn.cursor()

        # Get the maximum position for this chat
        cur.execute("SELECT COALESCE(MAX(position), -1) FROM users WHERE chat_id = %s", (chat_id,))
        max_position = cur.fetchone()[0]
        next_position = max_position + 1

        cur.execute("SELECT name FROM users WHERE chat_id = %s AND name = %s", (chat_id, name))
        if not cur.fetchone():
            cur.execute("INSERT INTO users (chat_id, name, position) VALUES (%s, %s, %s)", 
                       (chat_id, name, next_position))
            conn.commit()

        cur.close()
        conn.close()

    def remove_person(self, chat_id, name):
        conn = self.__get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT name FROM users WHERE chat_id = %s AND name = %s", (chat_id, name))
        if not cur.fetchone():
            raise ValueError(f"{name} нет в списке!")
        else:
            cur.execute("DELETE FROM users WHERE chat_id = %s AND name = %s", (chat_id, name))
            conn.commit()

        cur.close()
        conn.close()

    def clear_chat(self, chat_id):
        conn = self.__get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE chat_id = %s", (chat_id,))
        conn.commit()

        cur.close()
        conn.close()

    def set_people_list(self, chat_id, names):
        conn = self.__get_db_connection()
        cur = conn.cursor()
        
        try:
            # Get the maximum position for this chat
            cur.execute("SELECT COALESCE(MAX(position), -1) FROM users WHERE chat_id = %s", (chat_id,))
            max_position = cur.fetchone()[0]
            
            # Insert all names with incrementing positions
            for i, name in enumerate(names):
                cur.execute("SELECT name FROM users WHERE chat_id = %s AND name = %s", (chat_id, name))
                if not cur.fetchone():
                    cur.execute(
                        "INSERT INTO users (chat_id, name, position) VALUES (%s, %s, %s)",
                        (chat_id, name, max_position + 1 + i)
                    )
            
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def reorder_people(self, chat_id, new_order):
        """Update positions of people according to the new order"""
        conn = self.__get_db_connection()
        cur = conn.cursor()
        
        try:
            # Update positions based on the new order
            for position, name in enumerate(new_order):
                cur.execute(
                    "UPDATE users SET position = %s WHERE chat_id = %s AND name = %s",
                    (position, chat_id, name)
                )
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def __get_db_connection(self):
        return psycopg2.connect(self.database_url, sslmode="require")
    
    # Создание таблицы (выполняется один раз)
    def __create_table(self):
        conn = self.__get_db_connection()
        cur = conn.cursor()
        
        try:
            # First, check if the table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    chat_id BIGINT NOT NULL,
                    name TEXT NOT NULL,
                    position INTEGER NOT NULL DEFAULT 0
                );
            """)
            
            # Check if position column exists, if not add it
            cur.execute("""
                DO $$ 
                BEGIN 
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM information_schema.columns 
                        WHERE table_name='users' AND column_name='position'
                    ) THEN 
                        ALTER TABLE users ADD COLUMN position INTEGER NOT NULL DEFAULT 0;
                        
                        -- Initialize positions for existing records
                        WITH ranked AS (
                            SELECT id, chat_id, ROW_NUMBER() OVER (PARTITION BY chat_id ORDER BY id) - 1 as new_position
                            FROM users
                        )
                        UPDATE users 
                        SET position = ranked.new_position
                        FROM ranked 
                        WHERE users.id = ranked.id;
                    END IF;
                END $$;
            """)
            
            conn.commit()
        finally:
            cur.close()
            conn.close()

