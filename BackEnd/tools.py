import time
import os
import json
import subprocess
import pyperclip as ppc


class TasksResumable:
    
    def __init__(self, name:str, **tasks):
        """
        @param name: name of the proccess that has task or tasks to be tracked.
        @param tasks: names and functions of tasks. The functions are executed in order.
        """
        self.name = name
        self.tasks = tasks
        if os.path.isfile(f"{name}.txt"):
            self.__from_completed_task()

    def __from_completed_task(self):
        """
        Load tasks from the last completed task.
        """
        with open(f"{self.name}.txt", 'r') as f:
            line = f.readline().removesuffix("\n").split(":")
            tasks = list(self.tasks.keys())
            try:
                idx = tasks.index(line[0])
                if line[1] == "completed":
                    idx += 1
                elif line[1] != "started":
                    raise Exception("The file is manipulated. Invalid Task Status.")
                self.tasks = {k:self.tasks[k] for k in tasks[idx:]}
            except IndexError as e:
                raise Exception(f"This file is not valid. {e}")
            except ValueError:
                raise Exception("Task is not valid.")
    
    def run_tasks(self):
        with open(f"{self.name}.txt", 'w') as f:
            for t_name, task in zip(self.tasks.keys(), self.tasks.values()):
                f.write(f"{t_name}:started")
                r = task()
                f.seek(0)
                f.write(f"{t_name}:completed")
                f.flush()
                yield t_name, r
                f.seek(0)
                f.truncate()
        os.remove(f"{self.name}.txt")


class ResumeableStepTask:
    
    def __init__(self, name, gtask):
        """
        @param name: name of the proccess that has task or tasks to be tracked.
        @param gtask: this is a generator that produce subtasks.
        """
        self.name = name
        self.task = gtask()
        obj = next(self.task)
        if os.path.isfile(f"{name}.json"):
            self.__from_completed_stage()
    
    def __from_completed_stage(self):
        """
        Continue from the last completed stage.
        """
        with open(f"{self.name}.json", 'r') as f:
            obj = json.load(f)
            self.task.send(obj)
    
    def run(self):
        with open(f"{self.name}.json", 'w') as f:
            while True:
                try:
                    obj = next(self.task)
                    json.dump(obj, f)
                    yield obj
                    f.seek(0,0)
                except StopIteration:
                    break
        os.remove(f"{self.name}.json")


class AppSettings:

    def __init__(self, dir:str):
        self.new_settings = {}
        self.app_dir = dir

    @property
    def data_directory(self):
        return os.path.join(self.app_dir, 'Data')

    def settings_path(self):
        return os.path.join(self.app_dir, 'Data', "settings.json")
    
    def load_settings(self):
        try:
            with open(self.settings_path(), "r") as f:
                return json.load(f)
        except:
            if self.new_settings:
                return self.new_settings
            return self.default_settings  # Return defaults if file doesn’t exist
    
    def save_settings(self, settings):
        try:
            with open(self.settings_path(), "w") as f:
                json.dump(settings, f, indent=4)  # indent for readability
            return True
        except:
            return False
    
    @property
    def default_settings(self):
        return {
                "timer": {"inactivity":300, "clipboard":30},
                "theme": {
                    "variant": 'small',
                    "type": 'regular',
                    "color": 'dark-blue'
                },
                "database": {
                    # Default to app directory, user can change it in settings section of UI
                    "name": "users_database.db",
                    "path": os.path.join(self.app_dir, 'Data')
                },
                "icons":{
                    "app_icon":os.path.join(self.app_dir, 'Icons', 'PassKeeper.png'),
                    "SetAccountFrame":{
                        "add_user_icon":os.path.join(self.app_dir, 'Icons', "add_user.png"),
                        "entry_username":os.path.join(self.app_dir, 'Icons', "user_name.png"),
                        "entry_open_eye":os.path.join(self.app_dir, 'Icons', "open_eye.png"),
                        "entry_close_eye":os.path.join(self.app_dir, 'Icons', "close_eye.png")
                    },
                    "LoginFrame":{
                        "background":os.path.join(self.app_dir, 'Icons', "background300x400.png"),
                        "user_icon":os.path.join(self.app_dir, 'Icons', "user.png"),
                        "entry_open_eye":os.path.join(self.app_dir, 'Icons', "open_eye.png"),
                        "entry_close_eye":os.path.join(self.app_dir, 'Icons', "close_eye.png")
                    },
                    "ManagerFrame":{
                        "add":os.path.join(self.app_dir, 'Icons', "Thin", "32x32", "add.png"),
                        "import":os.path.join(self.app_dir, 'Icons', "Thin", "32x32", "import_file.png"),
                        "export":os.path.join(self.app_dir, 'Icons', "Thin", "32x32", "export_file.png"),
                        "settings":os.path.join(self.app_dir, 'Icons', "Thin", "32x32", "settings.png"),
                        "logout":os.path.join(self.app_dir, 'Icons', "Thin", "32x32", "leave.png")
                    }
                }
            }


class AppVariable:
    
    def __init__(self, value=None):
        self.__v = value
    
    def set(self, value):
        self.__v = value
    
    def get(self):
        return self.__v


class Clipboard:
    
    def __init__(self):
        self.has_copy = False
        self.init_time = None
    
    def del_copy(self):
        if self.has_copy:
            ppc.copy("")
            self.has_copy = False
    
    def set_copy(self, value:str):
        ppc.copy(value)
        self.has_copy = True

def step_copying(src, dst, chunk_size=20480):
    x = 0
    start = (yield x)
    if start is None:
        start = 0
    mode = 'wb' if start==0 else '+rb'
    with open(src, "rb") as src_file:
        src_file.read(start)
        with open(dst, mode) as dst_file:
            if start>0:
                dst_file.seek(0,2)
            chunk = src_file.read(chunk_size)
            w_idx = start
            while chunk:
                w_idx += dst_file.write(chunk)
                dst_file.flush()
                yield w_idx
                chunk = src_file.read(chunk_size)

def gimport_text_data(file_path:str, line_sep:str, n_cols:int=4, encoding:str='utf-8', dt:int=500000):
    """
    @param file_path: Path to the text file
    @param line_sep: Separator to identify new data to be extracted
    @param n_cols: Each new data extracted from the lines is divided into n columns
    @param encoding: To read the file with the open function and get the byte size of each line
    @param dt: Nanoseconds time To read lines during which the code will block, 
    it is better to choose a time greater than 0.1 milliseconds, i.e. 100000 nanoseconds, 
    the default is 500000 nanoseconds(0.5 milliseconds).
    You can use this generator to prevent the code from blocking.
    """
    f_size = os.path.getsize(file_path)
    sum_size = 0
    indx = 1
    new_line = 0
    # Step 1: Check for CRLF (\r\n) in a small portion of the file
    with open(file_path, 'rb') as file:
        sample = file.readline()  # Read first line to check for \r\n
        if b'\r\n' in sample:
            new_line = 1
            
    with open(file_path, "r", encoding=encoding) as file:
        t0 = time.perf_counter_ns()
        data = []
        line_data = [" "]*n_cols
        i = 0
        for line in file:
            sum_size += len(line.encode(encoding)) + new_line
            line = line.removesuffix('\n')
            if line_sep in line:
                data.append([*line_data[:n_cols-1], "\n".join(line_data[n_cols-1:])])
                line_data = [" "]*n_cols
                i = 0
            else:
                line_data.insert(i, line)
                if i<n_cols:
                    line_data.pop()
                i += 1
            if (time.perf_counter_ns() - t0) >= dt:
                yield sum_size, data, indx
                t0 = time.perf_counter_ns()
                data = []
            elif f_size == sum_size:
                if i>0:
                    data.append([*line_data[:n_cols-1], "\n".join(line_data[n_cols-1:])])
                    i=0
                yield sum_size, data, indx
            indx += 1
        if i>0:
            data.append([*line_data[:n_cols-1], "\n".join(line_data[n_cols-1:])])
            yield sum_size, data, indx

def gimport_csv_data(file_path:str, n_columns:int, replacement:str, encoding:str='utf-8', dt:int=500000):
    """
    @param file_path: Path to the text file
    @param n_columns: Each new data extracted from the lines is divided into n columns
    @param replacement: Replacement will be replace with \n to obtain correct form of text
    @param encoding: To read the file with the open function and get the byte size of each line
    @param dt: Nanoseconds time To read lines during which the code will block, 
    it is better to choose a time greater than 0.1 milliseconds, i.e. 100000 nanoseconds, 
    the default is 500000 nanoseconds(0.5 milliseconds).
    You can use this generator to prevent the code from blocking.
    """
    f_size = os.path.getsize(file_path)
    sum_size = 0
    indx = 1
    new_line = 0
    # Step 1: Check for CRLF (\r\n) in a small portion of the file
    with open(file_path, 'rb') as file:
        sample = file.readline()  # Read first line to check for \r\n
        if b'\r\n' in sample:
            new_line = 1
    
    data = []
    if n_columns<=0:
        n_columns = 1
    with open(file_path, 'r', encoding='utf_8') as file:
        t0 = time.perf_counter_ns()
        for line in file:
            row = [" "] * 4
            sum_size += len(line.encode(encoding)) + new_line
            line = line.removesuffix("\n")
            items = line.split(",", n_columns-1)
            i = 0
            for item in items:
                row[i] = item.replace(replacement, '\n')
                i += 1
            data.append(row)
            if (time.perf_counter_ns() - t0) >= dt:
                yield sum_size, data, indx
                t0 = time.perf_counter_ns()
                data = []
            indx += 1
        if data:
            yield sum_size, data, indx

def gexport_to_txt(file_path:str, line_sep:str, data_var:AppVariable):
    """
    @param file_path: Path to the text file
    @param line_sep: Separator to identify new data
    @param data_var: Any Object that has set and get method,
    set data like list[list[str]] and this function use get method
    """
    with open(file_path, 'w', encoding="utf-8") as f:
        i = 0
        nc = 0
        while True:
            data = data_var.get()
            for items in data:
                nc += f.write('\n'.join(items) + f'\n{line_sep}\n')
                i += 1
            yield i, nc
            nc = 0

def gexport_to_csv(file_path:str, replacement:str, data_var:AppVariable):
    """
    @param file_path: Path to the text file
    @param replacement: Replace \\n character  with the replacement to put all data in one line
    @param data_var: Any Object that has set and get method,
    set data like list[list[str]] and this function use get method
    """
    with open(file_path, 'w', encoding="utf-8") as f:
        nc, i = 0, 0
        while True:
            data = data_var.get()
            for items in data:
                items[0] = items[0].replace("\n", '')
                items[1] = items[1].replace("\n", '')
                items[2] = items[2].replace("\n", '')
                items[3] = items[3].replace("\n", replacement)
                nc += f.write(','.join(items)+'\n')
                i += 1
            yield i, nc
            nc = 0

def import_text_data00(file_path:str, line_sep:str, n_cols:int=4):
    """line_sep is needed to extract data. It seperate data in 2 fields: site, extra info"""
    lines = []
    if os.path.isfile(file_path):

        with open(file_path, 'r') as f:
            lines = f.readlines()

    data = []
    line_data = [""]*n_cols
    i = 0
    for line in lines:
        line = line.removesuffix('\n')
        if line_sep in line:
            data.append([*line_data[:n_cols-1], "\n".join(line_data[n_cols-1:])])
            # data.append([line_data[0], line_data[1], line_data[2], "\n".join(line_data[3:])])
            line_data = [""]*n_cols
            i = 0
        else:
            line_data.insert(i, line)
            if i<n_cols:
                line_data.pop()
            i += 1
    return data

def import_csv_data00(file_path:str, n_columns:int, replacement:str):
    """The number of columns in the csv file(file_path) should be given by n_columns."""
    data = []
    lines = []
    if n_columns<=0:
        n_columns = 1
    with open(file_path, 'r', encoding='utf_8') as f:
        lines = f.readlines()
    try:
        for line in lines:
            row = [" "]*4
            line = line.removesuffix("\n")
            items = line.split(",", n_columns-1)
            i = 0
            for item in items:
                row[i] = item.replace(replacement, '\n')
                i += 1
            data.append(row)
        return data
    except IndexError as e:
        print("Maximum number of columns is 4, you enter ", n_columns)
        return data

def timing(func):
    def wrap(*a, **k):
        t0 = time.perf_counter_ns()
        r = func(*a, **k)
        t = time.perf_counter_ns() - t0
        print(f"nano: {t}, micro: {t/1000}, milli: {t/1e6}, second: {t/1e9}")
        return r
    return wrap
