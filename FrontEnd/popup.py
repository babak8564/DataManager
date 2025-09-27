from tkinter import filedialog
from FrontEnd.customwidget import *
from FrontEnd.styles import POPUP,SUCCESS_TL, DANGER_TL, INFO_TL, WARNING_TL
from BackEnd.core import App

class Popup(tk.Toplevel):

    def __init__(self, app:App, width:int, height:int, title:str='', iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, transient=None, overrideredirect=True, windowtype=None, topmost=False, toolwindow=False, alpha=1, **kwargs):
        super().__init__(title, iconphoto, size, position, minsize, maxsize, resizable, transient, overrideredirect, windowtype, topmost, toolwindow, alpha, **kwargs)
        self.grab_set()

        self.app = app

        main_x = app.root.winfo_x()
        main_y = app.root.winfo_y()
        main_width = app.root.winfo_width()
        main_height = app.root.winfo_height()

        x = main_x + (main_width - width) // 2
        y = main_y + (main_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title_info = tk.StringVar(self, title)
        self.main_fram = tk.Frame(self, style=POPUP.CUSTOM_TFRAME)
        self.main_fram.pack(fill='both', expand=1)
        self.info_label = tk.Label(self.main_fram, textvariable=self.title_info, justify='center', anchor='center', style=INFO_TL)
        self.info_label.pack(fill='x')

        close_label = tk.Label(self.main_fram, text="❌", style=DANGER_TL)
        close_label.place(relx=1, y=0, anchor='ne')
        close_label.bind("<ButtonRelease-1>", self.on_close)
        
        # Dragging functionality
        self.info_label.bind("<Button-1>", self.start_drag)
        self.info_label.bind("<B1-Motion>", self.drag)
        self.setup_ui()
    
    def setup_ui(self):
        pass

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.winfo_x() + deltax
        new_y = self.winfo_y() + deltay
        self.geometry(f"+{new_x}+{new_y}")
    
    def main_notification(self, msg:str, style:str, delay:int=2000):
        """Display msg for label with given style after delay in milisecond then remove msg and restore style"""
        old_title = self.title_info.get()
        old_style = self.info_label.cget('style')
        self.title_info.set(msg)
        self.info_label.config(style=style)
        self.after(delay, self.title_info.set, old_title)
        self.after(delay, lambda:self.info_label.config(style=old_style))
    
    def open_dialog(self, dialog, *args, **kwrgs):
        self.grab_release()
        self.withdraw
        result = dialog(*args, **kwrgs)
        self.deiconify()
        self.lift()
        self.grab_set()
        self.focus_set()
        return result
    
    def on_close(self, ev=None):
        if ev:
            y_max, x_max = ev.widget.winfo_reqheight(), ev.widget.winfo_reqwidth()
            if (0<ev.x<x_max) and (0<ev.y<y_max):
                self.destroy()
        else:
            self.destroy()

class SettingsPopup(Popup):
    
    def __init__(self, app, width, height, title = '', iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, transient=None, overrideredirect=True, windowtype=None, topmost=False, toolwindow=False, alpha=1, **kwargs):
        self.settings = app.settings.new_settings
        self.content_frame = None
        self.save_btn = None
        self.setting_label = None
        self.secure_procedure = None
        super().__init__(app, width, height, title, iconphoto, size, position, minsize, maxsize, resizable, transient, overrideredirect, windowtype, topmost, toolwindow, alpha, **kwargs)
        
    def setup_ui(self):
        top_frame = tk.Frame(self.main_fram, style=POPUP.CONTENT_TFRAME)
        top_frame.pack(fill='both', expand=1,padx=1, pady=1)
        bottom_frame = tk.Frame(self.main_fram, style=POPUP.SIDEBAR_TFRAME)
        bottom_frame.pack(side='bottom',fill='x',padx=1, pady=1)

        side_frame = tk.Frame(top_frame, style=POPUP.SIDEBAR_TFRAME)
        side_frame.pack(side='left',fill="y", padx=(0,1))

        self.content_frame = tk.Frame(top_frame, style=POPUP.CONTENT_TFRAME)
        self.content_frame.config()
        self.content_frame.pack(side='left',fill="both", expand=True, padx=(1,0))  # Padding to show border

        self.setting_label = tk.Label(self.content_frame,
                                      text="Settings for App", 
                                      justify="center",
                                      style=POPUP.CUSTOM_TLABEL, font=('Arial', 12, 'bold'))
        self.setting_label.pack()
        # Sidebar "Buttons" (Labels)
        set_timer_btn = tk.Button(side_frame, text='⏳Timer', style=POPUP.SIDEBAR_TBUTTON, command=self.show_timer_settings)
        set_timer_btn.pack(padx=5, pady=(3,1), anchor='w', fill='x')
        set_theme_btn = tk.Button(side_frame, text='🎨Appearance', style=POPUP.SIDEBAR_TBUTTON, command=self.show_theme_settings)
        set_theme_btn.pack(padx=5, pady=1, anchor='w', fill='x')
        set_db_btn = tk.Button(side_frame, text='🗄DataBase', style=POPUP.SIDEBAR_TBUTTON, command=self.show_database_settings)
        set_db_btn.pack(padx=5, pady=1, anchor='w', fill='x')
        self.save_btn = tk.Button(bottom_frame, text='Save Settings', command=self.save_settings,style=POPUP.CONTENT_TBUTTON, state='disabled')
        self.save_btn.pack(side='bottom', fill='x', anchor='s',padx=3, pady=5)

        self.show_timer_settings()

    def clear_settings_frame(self):
        for widget in self.content_frame.winfo_children()[1:]:
            widget.destroy()
    
    def update_theme(self):
        self.app.style.update_style(self.variant_combo.get(), self.style_combo.get(), self.color_combo.get())
        self.settings['theme']['variant'] = self.variant_combo.get()
        self.settings['theme']['type']    = self.style_combo.get()
        self.settings['theme']['color']   = self.color_combo.get()
        self.save_btn.config(state='normal')
    
    def update_timers(self):
        self.settings['timer']['inactivity'] = int(self.inactivity_timer.get())
        self.settings['timer']['clipboard'] = int(self.clipboard_timer.get())
        self.save_btn.config(state='normal')
    
    def choose_db_path(self, entry_path:tk.Entry):
        dir = self.open_dialog(filedialog.askdirectory)
        # dir = filedialog.askdirectory()
        if dir:
            entry_path.delete(0, 'end')
            entry_path.insert(0, dir)

    def changing_db_path(self, db_name, db_path):
        src_path = self.settings['database']['path']
        src_name = self.settings['database']['name']
        dst_name:str = db_name.get()
        dst_path:str = db_path.get()
        if not dst_name.endswith('.db'):
            dst_name += '.db'
        src = self.app.get_path(src_path, src_name)
        dst = self.app.get_path(dst_path, dst_name)
        if src==dst:
            self.main_notification("There is no change to apply!", WARNING_TL)
            return
        self.secure_procedure = self.app.manages_db_copy_procedure(src, dst)
        try:
            task = next(self.secure_procedure)
            self.database_copy_steps(task)
        except StopIteration:
            self.main_notification("There is no task for database copying.", WARNING_TL)
    
    def database_copying(self, task):
        try:
            next(task)
            self.app.root.after(1000, self.database_copying, task)
        except StopIteration:
            try:
                task = next(self.secure_procedure)
                self.after_database_copy(task)
            except StopIteration:
                self.main_notification(f"Something went wrong. Maybe controller file has been manipulated", DANGER_TL, 5000)     
    
    def after_database_copy(self, task):
        try:
            next(task)
            self.app.root.after(1000, self.after_database_copy, task)
        except StopIteration:
            try:
                task = next(self.secure_procedure)
            except StopIteration:
                self.main_notification("Procedure of database copy completely done.", SUCCESS_TL)
            self.app.root.after(2500, self.destroy)
        
    def show_database_settings(self):
        self.clear_settings_frame()
        msg = 'Change DataBase Settings.'
        self.setting_label.config(text=msg, anchor='center')
        
        l_name = tk.Label(self.content_frame, text='Change database file name:', style=POPUP.CUSTOM_TLABEL)
        l_name.pack(padx=5, pady=(15,0))

        e_db_name = tk.Entry(self.content_frame, style=POPUP.CUSTOM_TENTRY)
        e_db_name.pack(padx=5, pady=(0,5))

        l_path = tk.Label(self.content_frame, text='Change database directory:', style=POPUP.CUSTOM_TLABEL)
        l_path.pack(padx=5, pady=(15,0))
        
        e_db_path = tk.Entry(self.content_frame, style=POPUP.CUSTOM_TENTRY)
        e_db_path.pack(padx=15, fill='x', pady=2)
        
        tk.Button(self.content_frame, text='choose a directory', command=lambda: self.choose_db_path(e_db_path), style=POPUP.CONTENT_TBUTTON).pack(padx=15, fill='x')

        e_db_path.insert(0, self.settings['database']['path'])
        e_db_name.insert(0, self.settings['database']['name'])

        tk.Button(self.content_frame, text="Apply Changes", command=lambda: self.changing_db_path(e_db_name, e_db_path), style=POPUP.CUSTOM_TBUTTON).pack(padx=15, pady=15)
        self.app.style.update_Entry_Combo(self.content_frame)

    def show_timer_settings(self):
        self.clear_settings_frame()
        msg = "Set your desire 'Inactivity Timer' and 'Clipboard Timer'"
        self.setting_label.config(text=msg)
        

        inactivity_label = tk.Label(self.content_frame, text="Inactivity Timer:", style=POPUP.CUSTOM_TLABEL)
        inactivity_label.pack(padx=5, pady=(15,0))
        self.inactivity_timer = tk.Combobox(self.content_frame, values=[180,300,600,900, 1800], style=POPUP.CUSTOM_TCOMBOBOX, state='readonly')
        self.inactivity_timer.pack(padx=5,pady=(0,5))

        clipboard_label = tk.Label(self.content_frame, text="Clipboard Timer:", style=POPUP.CUSTOM_TLABEL)
        clipboard_label.pack(padx=5, pady=(5,0))
        self.clipboard_timer = tk.Combobox(self.content_frame, values=[15, 30, 60], style=POPUP.CUSTOM_TCOMBOBOX, state='readonly')
        self.clipboard_timer.pack(padx=5,pady=(0,5))

        self.inactivity_timer.set(self.settings['timer']['inactivity'])
        self.inactivity_timer.bind("<<ComboboxSelected>>", lambda e: self.update_timers())

        self.clipboard_timer.set(self.settings['timer']['clipboard'])
        self.clipboard_timer.bind("<<ComboboxSelected>>", lambda e: self.update_timers())

        self.app.style.update_Entry_Combo(self.content_frame)

    def show_theme_settings(self):
        self.clear_settings_frame()
        
        self.color_combo = tk.Combobox(self.content_frame, values=self.app.style.color_options, state="readonly",style=POPUP.CUSTOM_TCOMBOBOX)
        self.color_combo.set(self.app.style.color)
        self.color_combo.pack(pady=5)
        self.color_combo.bind("<<ComboboxSelected>>", lambda e: self.update_theme())

        self.style_combo = tk.Combobox(self.content_frame, values=self.app.style.type_options, state="readonly",style=POPUP.CUSTOM_TCOMBOBOX)
        self.style_combo.set(self.app.style.type)
        self.style_combo.pack(pady=5)
        self.style_combo.bind("<<ComboboxSelected>>", lambda e: self.update_theme())

        self.variant_combo = tk.Combobox(self.content_frame, values=self.app.style.variant_options, state="readonly",style=POPUP.CUSTOM_TCOMBOBOX)
        self.variant_combo.set(self.app.style.variant)
        self.variant_combo.pack(pady=5)
        self.variant_combo.bind("<<ComboboxSelected>>", lambda e: self.update_theme())

        self.setting_label.config(text='Change Theme Settings\nvariant, style and color could be modified.')
        self.app.style.update_Entry_Combo(self.content_frame)
        
    def save_settings(self):
        result = self.app.settings.save_settings(self.settings)
        if result:
            msg = 'Your changes were saved successfully.'
            style = SUCCESS_TL
        else:
            msg = 'Saving your changes failed.'
            style = DANGER_TL
        self.main_notification(msg, style)
        self.save_btn.config(state='disabled')

class AddNewPopup(Popup):
     
    def setup_ui(self):
        entry_frame = tk.Frame(self.main_fram, style=POPUP.CONTENT_TFRAME)
        entry_frame.pack(padx=5, pady=5, fill='both', expand=1)

        eFrame1 = tk.Frame(entry_frame, style=POPUP.CONTENT_TFRAME)
        eFrame1.pack(padx=5,pady=(0,1))
        eFrame2 = tk.Frame(entry_frame, style=POPUP.CONTENT_TFRAME)
        eFrame2.pack(padx=5,pady=(0,1))
        bFrame1 = tk.Frame(entry_frame, style=POPUP.CONTENT_TFRAME)
        bFrame1.pack(pady=1, anchor='center')

        # ---------------upframe elements---------------
        e1 = Entry(eFrame1,'Site', style=POPUP.CUSTOM_TENTRY)
        e1.pack(side='left',padx=2, pady=(5,2), fill='x')
        e2 = Entry(eFrame1,'Username', style=POPUP.CUSTOM_TENTRY)
        e2.pack(side='left',padx=2, pady=(5,2), fill='x')
        e3 = Entry(eFrame1,'Password', style=POPUP.CUSTOM_TENTRY)
        e3.pack(side='left',padx=2, pady=(5,2), fill='x')

        td = Text(
            eFrame2,'Extra Info', height=5, autostyle=False,
            font=self.app.style.font,
            background=self.app.style.ENTRY_BG, foreground= self.app.style.Entry_FG,
            insertbackground=self.app.style.Entry_FG
        )
        td.pack(side=tk.LEFT, padx=5, pady=2)
        
        add_btn = tk.Button(bFrame1, text='Add New Info', command=lambda:self.add_new_data(e1,e2,e3,td), style=POPUP.CONTENT_TBUTTON)
        add_btn.pack(side='left', padx=5, pady=2)
        cancle_btn = tk.Button(bFrame1, text='Cancle', style='outline.TButton', command=self.on_close)
        cancle_btn.pack(side='left', padx=5, pady=2)
    
    def add_new_data(self,e1,e2,e3,td):
        data_id, msg = self.app.insert_database_row(e1.result(), e2.result(), e3.result(), td.result())
        result = self.app.view.table_insert_data(data_id, e1.result())
        if result:
            self.main_notification(msg, SUCCESS_TL, 3000)
            self.destroy()
        else:
            self.info_label.config(style=DANGER_TL)
            self.title_info.set(msg)
            self.after(5000, lambda: self.info_label.config(style=INFO_TL))
            self.after(5000, lambda: self.title_info.set(self.title()))


class ShowRowPopup(Popup):
    
    def __init__(self, app:App, width, height, title = '', iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, transient=None, overrideredirect=True, windowtype=None, topmost=False, toolwindow=False, alpha=1, **kwargs):
        self.data_id = None
        self.selected_item = None
        self.values = ["", "", "", ""]
        super().__init__(app, width, height, title, iconphoto, size, position, minsize, maxsize, resizable, transient, overrideredirect, windowtype, topmost, toolwindow, alpha, **kwargs)
        
    def setup_ui(self):
        self.selected_item = self.app.view.tree.current_item
        info_style = INFO_TL
        if self.selected_item:
            row = self.app.view.tree.item(self.selected_item)["values"]
            self.data_id = row[0]
            self.values, msg = self.app.get_database_row(self.data_id)
            if self.values == ["", "", "", ""]:
                info_style = DANGER_TL
                self.title_info.set(msg)
        else:
            self.title_info.set("No Item selected from table. Close popup and selecte one row.")
        
        self.info_label.config(style=info_style)
        entry_frame = tk.Frame(self.main_fram, style=POPUP.CONTENT_TFRAME)
        entry_frame.pack(padx=5, pady=5, fill='both', expand=1)

        eFrame1 = tk.Frame(entry_frame, style=POPUP.CONTENT_TFRAME)
        eFrame1.pack(padx=5,pady=(0,5))
        eFrame2 = tk.Frame(entry_frame, style=POPUP.CONTENT_TFRAME)
        eFrame2.pack(padx=5,pady=(0,5))
        self.bFrame1 = tk.Frame(entry_frame, style=POPUP.CONTENT_TFRAME)
        self.bFrame1.pack(pady=2, anchor='center')

        # ---------------upframe elements---------------
        self.e1 = tk.Entry(eFrame1, style=POPUP.CUSTOM_TENTRY)
        self.e1.pack(side='left',padx=2, pady=(5,1), fill='x')
        self.e2 = tk.Entry(eFrame1, style=POPUP.CUSTOM_TENTRY)
        self.e2.pack(side='left',padx=2, pady=(5,1), fill='x')
        self.e3 = tk.Entry(eFrame1, style=POPUP.CUSTOM_TENTRY)
        self.e3.pack(side='left',padx=2, pady=(5,1), fill='x')

        self.td = tk.Text(
            eFrame2, height=5, autostyle=False,
            font=self.app.style.font,
            background=self.app.style.ENTRY_BG, foreground= self.app.style.Entry_FG,
            insertbackground=self.app.style.Entry_FG
        )
        self.td.pack(side=tk.LEFT, padx=5, pady=1)
        
        self.e1.delete(0, 'end')
        self.e1.insert(0, self.values[0])
        self.e2.delete(0, 'end')
        self.e2.insert(0, self.values[1])
        self.e3.delete(0, 'end')
        self.e3.insert(0, self.values[2])
        self.td.delete('1.0', '1.end')
        self.td.insert('1.0', self.values[3])
        
        cancle_btn = tk.Button(self.bFrame1, text='Close', style='outline.TButton', command=self.on_close)
        cancle_btn.pack(side='left', padx=5)


class EditRowPopup(ShowRowPopup):
    
    def setup_ui(self):
        super().setup_ui()
        edit_btn = tk.Button(
            self.bFrame1, text='Edit Info', 
            command=self.edit_clicked,
            style=POPUP.CONTENT_TBUTTON
        )
        edit_btn.pack(side='left', padx=5)
    
    def edit_clicked(self):
        values = [self.e1.get(),self.e2.get(),self.e3.get(),self.td.get('1.0', 'end-1c')]
        if self.values != values:
            if self.data_id:
                i = 1
                for item in values[1:]:
                    values[i] = self.app.encrypt(item)
                    i += 1
                result, msg = self.app.update_database_row(self.data_id, values[0], values[1], values[2], values[3])
                if result:
                    info_style = SUCCESS_TL
                    self.app.view.tree.item(self.selected_item, values=[self.data_id, values[0], "****", "****", "****"])
                    self.after(3000, self.on_close)
                else:
                    info_style = DANGER_TL
                self.title_info.set(msg)
                self.info_label.config(style=info_style)
        else:
            self.title_info.set("No change has been made.")
            self.after(2000, lambda:self.title_info.set(self.title()))


class ImportDataPopup(Popup):
    
    def __init__(self, app, width, height, title = '', iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, transient=None, overrideredirect=True, windowtype=None, topmost=False, toolwindow=False, alpha=1, **kwargs):
        self.txt_file = None
        self.csv_file = None
        self.delta = None
        self.values = None
        self.progress_lenght = 0
        self.n_success = 0
        self.n_failed = 0
        self.n_duplicate = 0
        super().__init__(app, width, height, title, iconphoto, size, position, minsize, maxsize, resizable, transient, overrideredirect, windowtype, topmost, toolwindow, alpha, **kwargs)
        
    def setup_ui(self):

        container = tk.Frame(self.main_fram, style=POPUP.CONTENT_TFRAME)
        container.pack(fill='both', expand=1, padx=2, pady=5)
        
        csv_frame = tk.Frame(container, style=POPUP.CONTENT_TFRAME)
        csv_frame.pack(side='left', padx=5, fill='both', expand=1)
        text_frame = tk.Frame(container, style=POPUP.CONTENT_TFRAME)
        text_frame.pack(side='left', padx=5, fill='both', expand=1)

        csv_info = "🔷 Choose number of columns (2, 3, 4)\n\n🔷 click on 📜 CSV button"
        csv_info_label = tk.Label(csv_frame, text=csv_info, font=("Arial", 10), style=POPUP.SIDEBAR_TLABEL)
        csv_info_label.pack(fill='x', pady=(15,3))
        self.n_cols = tk.Combobox(csv_frame, values=[2,3,4], state='readonly', style=POPUP.CUSTOM_TCOMBOBOX)
        self.n_cols.pack(fill='x', pady=(10,3))
        self.csv_btn = tk.Button(csv_frame, text="📜 CSV", command=self.read_csv, style=POPUP.CUSTOM_TBUTTON)
        self.csv_btn.pack(pady=15, fill='x')
        self.n_cols.set(4)

        txt_info = "🔷 Enter line separator (e.g, ---------)\n\n🔷 click on 📜 TXT button."
        
        txt_info_label = tk.Label(text_frame, text=txt_info, font=("Arial", 10), style=POPUP.SIDEBAR_TLABEL)
        txt_info_label.pack(fill='x',pady=(15,3))
        # tk.Button(text_frame, text="Choose txt file", command=lambda:self.choose_file([("TEXT file","*.txt")])).pack(fill='x')
        self.line_sep = Entry(text_frame, "Enter Line separator", style=POPUP.CUSTOM_TENTRY)
        self.line_sep.pack(fill='x', pady=(10,3))
        self.txt_btn = tk.Button(text_frame, text="📜 TXT", command=self.read_txt, style=POPUP.CUSTOM_TBUTTON)
        self.txt_btn.pack(pady=15, fill='x')

        self.percentage = tk.StringVar(self, "")
        plabel = tk.Label(self.main_fram, textvariable=self.percentage, style=POPUP.CONTENT_TLABEL)
        plabel.pack(fill='x',padx=5)
        self.progress = tk.Progressbar(self.main_fram, length=100, bootstyle=tk.INFO)
        self.progress.pack(fill='x', pady=(0,5), padx=5)
        self.progress['value'] = 100

    def disable(self):
        self.csv_btn.config(state=tk.DISABLED)
        self.txt_btn.config(state=tk.DISABLED)

    def active(self):
        self.csv_btn.config(state=tk.NORMAL)
        self.txt_btn.config(state=tk.NORMAL)
    
    def choose_file(self, file_type:list):
        file_path = self.open_dialog(filedialog.askopenfilename, filetypes=file_type)
        # file_path = filedialog.askopenfilename(
        #     filetypes=file_type
        # )
        if file_path:
            if file_type[0][1] == "*.txt":
                self.txt_file = file_path
            else:
                self.csv_file = file_path
    
    def read_csv(self):
        self.percentage.set("")
        n_column = int(self.n_cols.get())
        self.progress['value'] = 0
        self.percentage.set("Reading file...")
        self.choose_file([("CSV file", "*.csv")])
        if self.csv_file:
            self.progress_lenght =  self.app.get_file_size(self.csv_file)
            if self.progress_lenght:
                self.progress.config(length=self.progress_lenght)
                self.delta = 100/self.progress_lenght # used for showing progress
                self.values = self.app.get_data_from_csv(self.csv_file, n_column) # create a generator to fetch data in other methode.
                self.start_importing()
                self.disable()
            else:
                self.percentage.set("File is empty.")
                self.progress['value'] = 100
            self.csv_file = None
        else:
            self.progress['value'] = 100
            self.percentage.set("")
        
    def read_txt(self):
        self.percentage.set("")
        if not self.line_sep.result():
            self.line_sep.focus()
            return
        self.progress['value'] = 0
        self.percentage.set("Reading file...")
        self.choose_file([("TEXT file","*.txt")])
        if self.txt_file:
            self.progress_lenght = self.app.get_file_size(self.txt_file)
            if self.progress_lenght>0:
                self.progress.config(length=self.progress_lenght)
                self.delta = 100/self.progress_lenght # used for showing progress
                self.values = self.app.get_data_from_text(self.txt_file, self.line_sep.result()) # create a generator to fetch data in other methode.
                self.start_importing()
                self.disable()
            else:
                self.percentage.set("File is empty.")
                self.progress['value'] = 100
            self.txt_file = None
        else:
            self.progress['value'] = 100
            self.percentage.set("")
    
    def start_importing(self):
        try:
            progress_size, data, lin_indx = next(self.values)
            for values in data:
                duplicate = self.app.has_database_duplicate(values)
                if duplicate:
                    self.n_duplicate += 1
                else:
                    data_id, _ = self.app.insert_database_row(values[0], values[1], values[2], values[3])
                    if data_id:
                        self.app.view.table_insert_data(data_id, values[0])
                        self.n_success += 1
                    else:
                        self.n_failed += 1
            self.progress['value'] = self.delta*progress_size
            self.percentage.set(f"{int((progress_size/self.progress_lenght)*100)}% Complete | {lin_indx} lines read successfully")
            self.after(1,self.start_importing)
            return
        except StopIteration as e:
            self.percentage.set(f"100% Complete | Adding {self.n_success} rows was successful, {self.n_failed} failed, and {self.n_duplicate} duplicates were found.")
        except TypeError as e:
            self.percentage.set(f"No Data. Error: {e}")
        except Exception as e:
            print(e)
            self.percentage.set(f"Error: {e}")
        self.active()
        self.progress['value'] = 100
        self.n_duplicate = 0
        self.n_failed = 0
        self.n_success = 0
        

class ExportDataPopup(Popup):

    def __init__(self, app, width, height, title = '', iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, transient=None, overrideredirect=True, windowtype=None, topmost=False, toolwindow=False, alpha=1, **kwargs):
        self.delta = None
        self.value = None
        self.directory = None
        self.for_all = tk.BooleanVar()
        self.encryption_state = tk.BooleanVar()
        self.item_selected = ()
        self.length = 0
        super().__init__(app, width, height, title, iconphoto, size, position, minsize, maxsize, resizable, transient, overrideredirect, windowtype, topmost, toolwindow, alpha, **kwargs)
    
    def setup_ui(self):
        self.item_selected = self.app.view.tree.selection()

        radio_frame = tk.Frame(self.main_fram, style=POPUP.CONTENT_TFRAME)
        radio_frame.pack(padx=5, pady=(5,0))
        export_frame =tk.Frame(self.main_fram, style=POPUP.CONTENT_TFRAME)
        export_frame.pack(padx=5, pady=5)
        
        exleft_frame = tk.Frame(export_frame, style=POPUP.CONTENT_TFRAME)
        exleft_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)
        exright_frame = tk.Frame(export_frame, style=POPUP.CONTENT_TFRAME)
        exright_frame.pack(side=tk.LEFT, padx=5, fill=tk.BOTH)

        # radioframe
        numbers_frame = tk.Frame(radio_frame, style=POPUP.CONTENT_TFRAME)
        method_frame = tk.Frame(radio_frame, style=POPUP.CONTENT_TFRAME)
        numbers_frame.pack(side=tk.LEFT, padx=5, pady=5)
        method_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        all_btn = tk.Radiobutton(
            numbers_frame, text="Export All Data", variable=self.for_all,
            value=True, style=POPUP.CONTENT_TRADIOBTN
        )
        all_btn.pack(anchor='w', fill='x', pady=5)
        selected_btn = tk.Radiobutton(
            numbers_frame, text="Export Selected Rows", variable=self.for_all,
            value=False, style=POPUP.CONTENT_TRADIOBTN
        )
        selected_btn.pack(anchor='w', fill='x', pady=5)

        
        with_encrypt = tk.Radiobutton(
            method_frame, text="With Enryption", variable=self.encryption_state, 
            value=True, style=POPUP.CONTENT_TRADIOBTN
        )
        with_encrypt.pack(anchor='w', fill='x', pady=5)
        no_encrypt = tk.Radiobutton(
            method_frame, text="No  Encryption", variable=self.encryption_state, 
            value=False, style=POPUP.CONTENT_TRADIOBTN
        )
        no_encrypt.pack(anchor='w', fill='x', pady=5)

        # eframe
        e = Entry(exleft_frame, "Enter file name")
        e.pack(padx=2, fill=tk.X)
        self.csv_btn = tk.Button(exleft_frame, text="Export to CSV", command=lambda:self.export_to_csv(e.result()))
        self.csv_btn.pack(padx=1, pady=5, fill=tk.X)

        b = tk.Button(exright_frame, text="choose directory", command=self.choose_dir)
        b.pack(padx=2, fill=tk.X)
        self.txt_btn = tk.Button(exright_frame, text="Export to TXT", command=lambda:self.export_to_txt(e.result()))
        self.txt_btn.pack(padx=1, pady=5, fill=tk.X)

        self.percentage = tk.StringVar(self, "")
        plabel = tk.Label(self.main_fram, textvariable=self.percentage, style=POPUP.CONTENT_TLABEL)
        plabel.pack(fill='x',padx=5)
        self.progress = tk.Progressbar(self.main_fram, length=100, bootstyle=tk.INFO)
        self.progress.pack(fill='x', pady=(0,5), padx=5)
        self.progress['value'] = 100
    
    @property
    def get_data_ids(self):
        if self.for_all.get():
            return None
        return (int(self.app.view.tree.item(iid)["values"][0]) for iid in self.item_selected)
    
    @property
    def data_length(self):
        if self.for_all.get():
            return self.app.db.count_users_data()[0]
        return len(self.item_selected)
    
    def choose_dir(self):
        self.directory = self.open_dialog(filedialog.askdirectory,mustexist=True, title="Select Directory")
        # self.directory = filedialog.askdirectory(
        #     mustexist=True, title="Select Directory"
        # )

    def disable(self):
        self.csv_btn.config(state=tk.DISABLED)
        self.txt_btn.config(state=tk.DISABLED)

    def active(self):
        self.csv_btn.config(state=tk.NORMAL)
        self.txt_btn.config(state=tk.NORMAL)
    
    def export_to_txt(self, file_name:str):
        if file_name:
            if not self.directory:
                self.directory = self.app.settings.data_directory
            file_path = self.app.get_path(self.directory, file_name+'.txt')
            self.length = self.data_length
            if self.length:
                self.percentage.set("")
                self.progress.config(length=self.length)
                self.delta = 100/self.length
                self.progress['value'] = 0
                self.value = self.app.export_to_txt(
                    file_path, self.get_data_ids, self.encryption_state.get()
                )
                self.start_exporting()
                self.disable()
            else:
                self.percentage.set("No data.")
                self.progress['value'] = 100

    def export_to_csv(self, file_name):
        if file_name:
            if not self.directory:
                self.directory = self.app.settings.data_directory
            file_path = self.app.get_path(self.directory, file_name+'.csv')
            self.length = self.data_length
            if self.length:
                self.percentage.set("")
                self.progress.config(length=self.length)
                self.delta = 100/self.length
                self.progress['value'] = 0
                self.value = self.app.export_to_csv(
                    file_path, self.get_data_ids, self.encryption_state.get()
                )
                self.start_exporting()
                self.disable()
            else:
                self.percentage.set("No data.")
                self.progress['value'] = 100
    
    def start_exporting(self, n_c:int=0):
        
        try:
            line_indx, number_chars = next(self.value)
            if line_indx:
                self.progress['value'] += self.delta
                n_c += number_chars
                self.percentage.set(f"{line_indx} lines| {int((line_indx/self.length)*100)}% completed | {n_c} characters write successfully.")
            self.after(1,self.start_exporting, n_c)
            return
        except StopIteration as e:
            if n_c>0:
                self.percentage.set(f"{self.length} lines| 100% completed | {n_c} characters write successfully.")
            else:
                self.percentage.set("No Data To Write.")
            self.value = None
            # self.active()
        except TypeError as e:
            print(e)
            self.percentage.set(f"typeError: {e}")
            # self.active()
        except Exception as e:
            self.percentage.set(f"Error: {e}")
            # self.active()
        self.active()
        self.progress['value'] = 100

