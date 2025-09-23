import os
import time
from enum import Enum
from BackEnd.database import Database
from BackEnd.tools import AppSettings, AppVariable, Clipboard, gimport_text_data, \
gimport_csv_data, gexport_to_txt, gexport_to_csv, TasksResumable, ResumeableStepTask, step_copying
from BackEnd.encryption import Encryption

from typing import Any, List, TYPE_CHECKING, Callable
if TYPE_CHECKING:
    # we need these imports just for type hint. Its not affect runtime.
    from FrontEnd.styles import CryptoStyle
    from FrontEnd.view import ManagerFrame
    from ttkbootstrap import Window, Label, Frame

class AppState(Enum):
    SET_ACCOUNT = "set_account"
    LOGIN = "login"
    MAIN = "main"
    INACTIVE = "inactive"
    DATABASE_ERROR = 'database error'


class App:
    REPLACEMENT = " |🔻| "
    LINE_SEPARATOR = "-"*15
    
    def __init__(self, root, main_path):
        self.root:Window = root
        self.main_dir: str = os.path.dirname(os.path.abspath(main_path))
        if not os.path.isdir(os.path.join(self.main_dir, "Data")):
            os.mkdir(os.path.join(self.main_dir, "Data"))
        
        self.settings: AppSettings = AppSettings(self.main_dir)
        self.icons_path: str = os.path.join(self.main_dir, 'Icons')
        settings: dict = self.settings.load_settings()
        self.settings.new_settings = settings

        self.clipboard = Clipboard()

        self.style: 'CryptoStyle' | None = None
        self.main_notif: 'Label'  | None = None
        self.container: 'Frame'   | None = None
        self.view: 'ManagerFrame' | None = None

        self.state: AppState = AppState.SET_ACCOUNT  # Default state
        self._state_callback: Callable[[AppState], None] | None
        
        db_dir: str = settings['database']['path']
        db_fname:str = settings['database']['name']
        
        self.db_path: str = self.get_path(db_dir, db_fname)
        self.db = None
        self.db_error = None
        try:
            self.db = Database(self.db_path)  # Always create/connect
        except RuntimeError as e:
            self.state = AppState.DATABASE_ERROR
            self.db_error = str(e)
        self.user_id = None

        self.style_type = settings['theme']['type']
        self.style_variant = settings['theme']['variant']
        self.style_color = settings['theme']['color']
        
        self.encryption = Encryption()
        self.fernet_key = None
    
    def db_reconnect(self):
        db_dir: str = self.settings.new_settings['database']['path']
        db_fname:str = self.settings.new_settings['database']['name']
        
        self.db_path: str = self.get_path(db_dir, db_fname)
        self.db = None
        self.db_error = None
        try:
            self.db = Database(self.db_path)  # Always create/connect
            return "Connected to database."
        except RuntimeError as e:
            self.state = AppState.DATABASE_ERROR
            self.db_error = str(e)
            return "Connection to db failed."
    
    def is_database_valid(self):
        validation_msg = []
        is_valid = []
        try:
            r = self.db.are_tables_valid()
            is_valid.append(r)
            if r:
                validation_msg.append("Names and numbers of tables are valid")
            else:
                validation_msg.append("Names and numbers of tables are not valid")
            
            r = self.db.are_tables_schema_valid()
            is_valid.append(r)
            if r:
                validation_msg.append("Tables schema are valid")
            else:
                validation_msg.append("Tables schema are not valid")
                return False, validation_msg

            r = self.db.is_integrity_valid()
            is_valid.append(r)
            if r:
                validation_msg.append("Integrity of tables is valid")
            else:
                validation_msg.append("Integrity of tables is not valid")
            
            r = self.db.is_foreign_key_valid()
            is_valid.append(r)
            if r:
                validation_msg.append("Foriegn key is valid")
            else:
                validation_msg.append("Foriegn key is not valid")
            
            r = self.db.is_index_existance()
            is_valid.append(r)
            if r:
                validation_msg.append("Index is existance")
            else:
                validation_msg.append("Index is not existance")
            return all(is_valid), validation_msg

        except Exception as error:
            if "malformed" in str(error).lower():
                raise RuntimeError(str(error))
            return False, validation_msg
        
    def resumeable_db_copy(self, src, dst):
        rtask = ResumeableStepTask("Database copy", lambda :step_copying(src, dst))
        return rtask.run()
    
    def tasks_after_db_copy(self, src, dst):
        """
        define tasks for copying database from src to dst securely, even system or app crash in some point.
        """
        
        def apply_settings():
            self.settings.new_settings['database']['name'] = os.path.basename(dst)
            self.settings.new_settings['database']['path'] = os.path.dirname(dst)
            result = self.settings.save_settings(self.settings.new_settings)
            if result:
                return "New database setttings applied."
            return "Failed to save database settings."
        
        def remove_src_file():
            os.remove(src)
            return "Database source file deleted."
        
        tr = TasksResumable(
            "Tasks after database copy",
            change_settings = apply_settings,
            close_database = self.db.close,
            remove_src = remove_src_file,
            db_reconnect = self.db_reconnect
        )
        return tr.run_tasks()
    
    def manages_db_copy_procedure(self, src, dst):
        mode = '+w'
        if os.path.isfile("control_db_copy_procedure.txt"):
            mode = 'r+'
        copying_state = 'starting'
        after_copying_state = 'starting'
        
        with open("control_db_copy_procedure.txt", mode) as f:
            line = f.readline().removesuffix('\n')
            if line:
                copying_state, after_copying_state = line.split(',')
                line = f.readline().removesuffix('\n')
                if line:
                    if os.path.isdir(line):
                        src = line
                line = f.readline().removesuffix('\n')
                if line:
                    if os.path.isdir(line):
                        dst = line
            else:
                f.seek(0,0)
                f.write(f"{copying_state},{after_copying_state}\n{src}\n{dst}")
                f.flush()
            if copying_state=="starting":
                yield self.resumeable_db_copy(src, dst)
            f.seek(0,0)
            f.write("completed,starting")
            f.flush()
            if after_copying_state == 'starting':
                yield self.tasks_after_db_copy(src, dst)
            f.seek(0,0)
            f.write("completed,completed")
            f.flush()
        
        os.remove("control_db_copy_procedure.txt")
    
    def set_state_callback(self, callback:Callable[[AppState], None]):
        self._state_callback = callback
    
    def set_state(self, state:AppState):
        self.state = state
        if self._state_callback:
            self.view = self._state_callback(state)

    def initial_state(self):
        has_user, _ = self.db.has_users()
        if has_user:
            self.set_state(AppState.LOGIN)
        else:
            self.set_state(AppState.SET_ACCOUNT)

    def create_account(self, username:str, password:str):
        salt = os.urandom(16)
        user_id, message = self.db.add_user(username, self.encryption.hashing(password), salt)
        if user_id:
            self.user_id = user_id
            return salt, message
        return None, message
        
    def login(self, username, password:str):
        user_id, message = self.db.get_user_id(username)
        if user_id:
            verify = self.encryption.authorized(
                self.db.get_user_hash(user_id)[0], password
            )
            if verify:
                self.user_id = user_id
                salt, _ = self.db.get_salt(self.user_id)
                return salt, "Verify was successfull"
            return None, "Wrong password."
        return None, message

    def encrypt(self, item:str):
        if item not in ['', ' ', '\n', '\t', ' '*len(item), '\n'*len(item), '\t'*len(item)]:
            item = self.encryption.encrypt(self.fernet_key, item)
        return item
    
    def decrypt(self, item:str):
        if item not in ['', ' ', '\n', '\t', ' '*len(item), '\n'*len(item), '\t'*len(item)]:
            item = self.encryption.decrypt(self.fernet_key, item)
        return item

    def update_database_row(self, data_id, site:str, username:str, password:str, extra_info:str):
        return self.db.update_user_data(
                    self.user_id, data_id, 
                    site, username, password, extra_info
                )

    def insert_database_row(self, site:str, username:str, password:str, extra_info:str):
        data = [site]
        for item in [username, password, extra_info]:
            data.append(self.encrypt(item))
        return self.db.add_user_data(self.user_id, *data)

    def get_database_row(self, data_id):
        values = ["", "", "", ""]
        data, msg = self.db.get_specific_row(data_id, self.user_id)
        if data:
            i = 1
            values[0] = data[2]
            for item in data[3:]:
                values[i] = self.decrypt(item)
                i += 1
        return values, msg

    def has_database_duplicate(self, values):
        dup_list, _ = self.db.get_duplicate_column(self.user_id,'site', values[0])
        if dup_list:
            for items in dup_list:
                decrype_data = [items[2]]
                for item in items[3:]:
                    item = self.decrypt(item)
                    decrype_data.append(item)
                if values==decrype_data:
                    return True
        return False

    def get_path(self, *args):
        return os.path.normpath(os.path.join(*args))
    
    def raw_users_data(self, data_ids:list[int]=None):
        if data_ids:
            for data_id in data_ids:
                row, _ = self.db.get_specific_row(data_id, self.user_id)
                yield row[2], row[3], row[4], row[5]
        else:
            for row in self.db.fetch_rows_one_by_one("users_data"):
                yield row['site'], row['username'], row['password'], row['extra_info']
    
    def get_basename(self, file_path):
        return os.path.basename(file_path)
    
    def get_dirname(self, file_path):
        return os.path.dirname(file_path)
    
    def get_file_size(self, f_path):
        return os.path.getsize(f_path)

    def get_data_from_text(self, file_path:str, line_sep:str):
        return gimport_text_data(file_path, line_sep)
    
    def get_data_from_csv(self, file_path:str, n:int):
        return gimport_csv_data(file_path, n, self.REPLACEMENT)
    
    def export_data(self, data_vriable:AppVariable, raw_data, data_writer, encrypte, dt:int=500000):
        t0 = time.perf_counter_ns()
        data = []
        try:
            while True:
                while (time.perf_counter_ns() - t0) < dt:
                    values = list(next(raw_data))
                    if not encrypte:
                        for j in range(1,4):
                            values[j] = self.decrypt(values[j])
                    data.append(values)
                data_vriable.set(data)
                n_r, n_c = next(data_writer)
                yield n_r, n_c
                data = []
                t0 = time.perf_counter_ns()
        except StopIteration:
            print(f"Stop Iteration. {n_r} lines, {n_c} characters")
        except Exception as e:
            print(f"Unexpected Error. {n_r} lines, {n_c} characters\nError: {e}")
        if data:
            data_vriable.set(data)
            n_r, n_c = next(data_writer)
            yield n_r, n_c

    def export_to_txt(self, file_path:str, data_ids:list=None, encrypte:bool=True):
        data = AppVariable()
        raw_data = self.raw_users_data(data_ids)
        data_writer = gexport_to_txt(file_path, self.LINE_SEPARATOR, data)
        return self.export_data(data, raw_data, data_writer, encrypte)

    def export_to_csv(self, file_path, data_ids:iter=None, encrypte:bool = True):
        data = AppVariable()
        raw_data = self.raw_users_data(data_ids)
        data_writer = gexport_to_csv(file_path, self.REPLACEMENT, data)
        return self.export_data(data, raw_data, data_writer, encrypte)
    
    def key_maker(self, password:bytes, salt:bytes):
        self.fernet_key = self.encryption.key_maker(password, salt)
        self.root.event_generate("<<KeyGenerated>>", when='tail')

    def mark_to_manager(self):
        self.set_state(AppState.MAIN)
    
    def mark_inactive(self):
        self.fernet_key = None
        self.user_id = None
        self.set_state(AppState.INACTIVE)
    
    def on_closing(self):
        if self.db:
            self.db.close()
        self.root.destroy()


