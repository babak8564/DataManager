import sqlite3
from datetime import datetime

# QueryFactory
class QueryFactory:
    
    @staticmethod
    def create_users_table():
        return """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                salt BLOB,
                last_modified TEXT
            )
        """

    @staticmethod
    def create_users_data_table():
        return """
            CREATE TABLE IF NOT EXISTS users_data (
                data_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                site TEXT,
                username TEXT,
                password TEXT,
                extra_info TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        """

    @staticmethod
    def create_users_data_index():
        return "CREATE INDEX IF NOT EXISTS idx_user_id ON users_data (user_id)"

    @staticmethod
    def check_duplicate_data(user_id, c1, c2, c3, c4):
        # Check for existing duplicate
        query = "SELECT COUNT(*) FROM users_data WHERE user_id = ? AND site = ? AND username = ? AND password = ? AND extra_info = ?;"
        params = (user_id,c1,c2,c3,c4)
        return query,params
    
    @staticmethod
    def add_user(username, password, salt):
        query = "INSERT INTO users (username, password, salt, last_modified) VALUES (?, ?, ?, ?)"
        params = (username, password, salt, datetime.now().isoformat())
        return query, params

    @staticmethod
    def add_user_data(user_id, c1, c2, c3, c4):
        query = "INSERT INTO users_data (user_id, site, username, password, extra_info) VALUES (?, ?, ?, ?, ?)"
        params = (user_id, c1, c2, c3, c4)
        return query, params

    @staticmethod
    def update_last_modified(user_id):
        query = "UPDATE users SET last_modified = ? WHERE user_id = ?"
        params = (datetime.now().isoformat(), user_id)
        return query, params
    
    @staticmethod
    def update_user_data(user_id, data_id, c1=None, c2=None, c3=None, c4=None):
        query_parts = ["UPDATE users_data SET"]
        params = []
        
        if c1 is not None:
            query_parts.append("site = ?")
            params.append(c1)
        if c2 is not None:
            query_parts.append("username = ?")
            params.append(c2)
        if c3 is not None:
            query_parts.append("password = ?")
            params.append(c3)
        if c4 is not None:
            query_parts.append("extra_info = ?")
            params.append(c4)
        if not params:
            return None, None
        query = f"{query_parts[0]} {', '.join(query_parts[1:])} WHERE user_id = ? AND data_id = ?"
        params.extend([user_id, data_id])
        return query, tuple(params)

    @staticmethod
    def get_user_hash(user_id):
        query = "SELECT password FROM users WHERE user_id = ?"
        params = (user_id,)
        return query, params

    @staticmethod
    def get_user_salt(user_id):
        query = "SELECT salt FROM users WHERE user_id = ?"
        params = (user_id,)
        return query, params
    
    @staticmethod
    def remove_user_data(data_id):
        query = "DELETE FROM users_data WHERE data_id = ?"
        params = (data_id,)
        return query, params

    @staticmethod
    def get_columns_name(table_name:str):
        query = f"PRAGMA table_info({table_name})"
        params = tuple()
        return query, params

    @staticmethod
    def count_users():
        query = "SELECT COUNT(*) FROM users"
        params = ()
        return query, params
    
    @staticmethod
    def count_users_data():
        query = "SELECT COUNT(*) FROM users_data"
        params = ()
        return query, params

    @staticmethod
    def get_usernames():
        query = "SELECT username FROM users ORDER BY username"
        params = ()
        return query, params

    @staticmethod
    def get_user(user_id):
        query = "SELECT * FROM users WHERE user_id = ?"
        params = (user_id,)
        return query, params

    @staticmethod
    def get_column_values(table_name, column_name, user_id=None):
        if user_id is None:
            query = f"SELECT {column_name} FROM {table_name}"
            params = ()
        else:
            query = f"SELECT data_id, {column_name} FROM {table_name} WHERE user_id = ?"
            params = (user_id,)
        return query, params
    
    @staticmethod
    def get_specific_column(data_id, user_id, column_name):
        query = f"SELECT {column_name} FROM users_data WHERE data_id = ? AND user_id = ?"
        params = (data_id, user_id)
        return query, params
    
    @staticmethod
    def get_duplicate_column(user_id, column_name, column_value):
        query = f"SELECT * FROM users_data WHERE {column_name} = ? AND user_id = ?"
        params = (column_value, user_id)
        return query, params
    
    @staticmethod
    def get_specific_row(data_id, user_id):
        query = f"SELECT * FROM users_data WHERE data_id = ? AND user_id = ?"
        params = (data_id, user_id)
        return query, params
    
    @staticmethod
    def get_user_data(user_id):
        query = "SELECT * FROM users_data WHERE user_id = ?"
        params = (user_id,)
        return query, params

    @staticmethod
    def get_user_data_by_data_id(data_id):
        query = "SELECT * FROM users_data WHERE data_id = ?"
        params = (data_id,)
        return query, params
    
    @staticmethod
    def get_user_id(username):
        query = "SELECT user_id FROM users WHERE username = ?"
        params = (username,)
        return query, params



# Database
class Database:
    
    def __init__(self, db_name, query_factory=QueryFactory):
        self.conn = None
        self.qf = query_factory
        try:
            self.conn = sqlite3.connect(db_name)
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.create_tables()
        except sqlite3.Error as e:
            # For init, we might still raise an exception since GUI can't start without a DB
            raise RuntimeError(f"Failed to connect to database: {e}")

    def execute_query(self, query, params=()):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(query, params)
                return cursor.lastrowid, "Operation completed successfully"
        except sqlite3.IntegrityError as e:
            return None, f"Duplicate entry: {e}"
        except sqlite3.Error as e:
            return None, f"Database error: {e}"

    def fetch_one(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            if result:
                return result, "Record found"
            return None, "No record found"
        except sqlite3.Error as e:
            return None, f"Fetch error: {e}"

    def fetch_all(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            if results:
                return results, f"Found {len(results)} records"
            return [], "No records found"
        except sqlite3.Error as e:
            return [], f"Fetch error: {e}"

    def are_tables_valid(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'users_data')")
        tables = cursor.fetchall()
        if len(tables) != 2:
            return False
        else:
            for table in [('users',), ('users_data',)]:
                if table not in tables:
                    return False
            return True
    
    def are_tables_schema_valid(self):
        cursor = self.conn.cursor()
        expected_users_columns = {
            'user_id': 'INTEGER',
            'username': 'TEXT',
            'password': 'TEXT',
            'salt': 'BLOB',
            'last_modified': 'TEXT'
        }
        expected_users_data_columns = {
            'data_id': 'INTEGER',
            'user_id': 'INTEGER',
            'site': 'TEXT',
            'username': 'TEXT',
            'password': 'TEXT',
            'extra_info': 'TEXT'
        }
        # Check 'users' table schema
        cursor.execute("PRAGMA table_info(users)")
        users_columns = {row[1]: row[2] for row in cursor.fetchall()}
        b1 = all(col in users_columns and users_columns[col] == dtype for col, dtype in expected_users_columns.items())
        cursor.execute("PRAGMA table_info(users_data)")
        users_data_columns = {row[1]: row[2] for row in cursor.fetchall()}
        b2 = all(col in users_data_columns and users_data_columns[col] == dtype for col, dtype in expected_users_data_columns.items())
        if b1 and b2:
            return True
        else:
            return False
    
    def is_integrity_valid(self):
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        if result[0] != 'ok':
            return False
        else:
            return True

    def is_foreign_key_valid(self):
        cursor = self.conn.cursor()    
        cursor.execute("PRAGMA foreign_key_list(users_data)")
        fk_info = cursor.fetchall()
        expected_fk = [(0, 0, 'users', 'user_id', 'user_id', 'NO ACTION', 'NO ACTION', 'CASCADE')]
        if not any(fk[2:6] == expected_fk[0][2:6] for fk in fk_info):
            return False
        return True

    def is_index_existance(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_user_id'")
        r = cursor.fetchone()
        if not r:
            return False
        return True

    def create_tables(self):
        # For simplicity, assume table creation always works or fails silently
        # In a real app, you might want a setup method with feedback
        self.execute_query(self.qf.create_users_table())
        self.execute_query(self.qf.create_users_data_table())
        self.execute_query(self.qf.create_users_data_index())

    
    def is_duplicate(self,user_id, c1, c2, c3, c4):
        try: # check for duplicate data
            query, params = self.qf.check_duplicate_data(user_id, c1, c2, c3, c4)
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            if count > 0:
                return True  # Indicate no insert was performed
            return False
        except sqlite3.Error as e:
            return False

    def has_users(self):
        query, params = self.qf.count_users()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count > 0, "User check successful"
        except sqlite3.Error as e:
            return False, f"Error checking users: {e}"
    
    def count_users_data(self):
        query, params = self.qf.count_users_data()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()[0], "Count users data  successful"
        except sqlite3.Error as e:
            return 0, f"Error counting users data: {e}"

    def update_user_data(self, user_id, data_id, c1=None, c2=None, c3=None, c4=None):
        # Verify row exists and belongs to user_id
        query, params = self.qf.get_user_data_by_data_id(data_id)
        result, message = self.fetch_one(query, params)
        if not result:
            return False, "Data not found"
        if result[1] != user_id:  # user_id is second column
            return False, "Data does not belong to this user"

        # Check if any changes were provided
        if all(x is None for x in [c1, c2, c3, c4]):
            return False, "No changes specified"

        # Execute update
        query, params = self.qf.update_user_data(user_id, data_id, c1, c2, c3, c4)
        _, message = self.execute_query(query, params)
        if "successfully" in message.lower():
            # Update last_modified
            query, params = self.qf.update_last_modified(user_id)
            _, update_message = self.execute_query(query, params)
            if "successfully" in update_message.lower():
                return True, "Data updated and user updated successfully"
            return True, f"Data updated, but failed to update user: {update_message}"
        return False, message
    
    def add_user(self, username, password, salt):
        if not username or not password:
            return None, "Username and password cannot be empty"
        # hashed = hashlib.sha256(password.encode()).hexdigest()
        query, params = self.qf.add_user(username, password, salt)
        return self.execute_query(query, params)

    def add_user_data(self, user_id, c1, c2, c3, c4):
        if c1 and any([c2, c3, c4]):  # Basic validation
            query, params = self.qf.add_user_data(user_id, c1, c2, c3, c4)
            data_id, message = self.execute_query(query, params)
            if data_id:  # Success case: update last_modified
                query, params = self.qf.update_last_modified(user_id)
                _, update_message = self.execute_query(query, params)
                if "successfully" in update_message.lower():  # Check if update worked
                    return data_id, "Data added and user updated successfully"
                return data_id, f"Data added, but failed to update user: {update_message}"
            return None, message  # Return error message if insert failed
        return None, "Please enter one more item along with the site name."

    def remove_user_data(self, data_id):
        query, params = self.qf.get_user_data_by_data_id(data_id)
        result, message = self.fetch_one(query, params)
        if not result:
            return False, "Data not found"
        user_id = result[1]  # user_id is second column
        query, params = self.qf.remove_user_data(data_id)
        _, delete_message = self.execute_query(query, params)
        if "successfully" in delete_message.lower():
            query, params = self.qf.update_last_modified(user_id)
            self.execute_query(query, params)  # No need to check this one
            return True, "Data removed successfully"
        return False, delete_message

    def get_user_hash(self, user_id):
        query, params = self.qf.get_user_hash(user_id)
        try:
            result, _ =  self.fetch_one(query, params)
            if result:
                return result[0], "hash found"
            return None, 'No hash found'
        except sqlite3.Error as e:
            return None, f"Error fetching hash: {e}"

    def get_salt(self, user_id):
        query, params = self.qf.get_user_salt(user_id)
        try:
            result, _ =  self.fetch_one(query, params)
            if result:
                return result[0], "salt found"
            return None, 'No salt found'
        except sqlite3.Error as e:
            return None, f"Error fetching salt: {e}"
    
    def get_usernames(self):
        query, params = self.qf.get_usernames()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            usernames = [row[0] for row in cursor.fetchall()]
            return usernames, f"Found {len(usernames)} usernames"
        except sqlite3.Error as e:
            return [], f"Error fetching usernames: {e}"
    
    def get_columns_name(self, table:str):
        query, params = self.qf.get_columns_name(table)
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            columns = [row[1] for row in cursor.fetchall()]  # Extract 'name' from each row
            if columns:
                return columns, f"Found {len(columns)} columns in {table}"
            return [], f"No columns found in {table}"
        except sqlite3.Error as e:
            return [], f"Error retrieving columns: {e}"
    
    def get_user_id(self, username):
        if not username:
            return None, "Username cannot be empty"
        query, params = self.qf.get_user_id(username)
        result, message = self.fetch_one(query, params)
        if result:
            return result[0], "User found"  # result[0] is user_id
        return None, message  # "No record found" or error message
    
    def get_user(self, user_id):
        query, params = self.qf.get_user(user_id)
        return self.fetch_one(query, params)

    def get_user_data(self, user_id):
        query, params = self.qf.get_user_data(user_id)
        return self.fetch_all(query, params)

    def get_column_values(self, table_name, column_name, user_id):
        query, params = self.qf.get_column_values(table_name, column_name, user_id)
        return self.fetch_all(query, params)
    
    def get_specific_column(self, data_id, user_id, column_name):
        query, params = self.qf.get_specific_column(data_id, user_id, column_name)
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            if result:
                value = result[0]
                return value, "Value fetched successfully"
            return None, "Row not found"
        except sqlite3.Error as e:
            return None, f"Error fetching column: {e}"
    
    def get_duplicate_column(self, user_id, column_name, column_value):
        query, params = self.qf.get_duplicate_column(user_id, column_name, column_value)
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            if result:
                return result, "Value fetched successfully"
            return None, "Row not found"
        except sqlite3.Error as e:
            return None, f"Error fetching column: {e}"

    def get_specific_row(self, data_id, user_id):
        query, params = self.qf.get_specific_row(data_id, user_id)
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            if result:
                # value = result[0]
                return result, "Value fetched successfully"
            return None, "Row not found"
        except sqlite3.Error as e:
            return None, f"Error fetching column: {e}"
    
    def fetch_rows_one_by_one(self, table_name):
        try:
            self.conn.row_factory = sqlite3.Row # Allows accessing columns by name
            cursor = self.conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            for row in cursor:
                yield row
        except sqlite3.Error as e:
            yield None
    
    def close(self):
        if self.conn:
            self.conn.close()
        return "Database closed"

