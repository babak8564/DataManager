# from FrontEnd.customwidget import *
import time
import ttkbootstrap as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from FrontEnd.customwidget import CustomTreeview, CustomEntry, PasswordEntry, ToolTip, CountDown
from FrontEnd.styles import MAIN, SUCCESS_TL, INFO_TL, WARNING_TL, DANGER_TL
from FrontEnd.popup import SettingsPopup, AddNewPopup, ShowRowPopUp, EditRowPopUp, ImportDataPopUp, ExportDataPopUp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BackEnd.core import App

tlp = ToolTip()
# The app has three view: ManagerFrame, SetAccountFrame and LoginFrame view that inherit from ViewFrame

class ViewFrame(tk.Frame):
    def __init__(self, app:'App', master = None, *args, **kwrgs):
        super().__init__(master, *args, **kwrgs)
        self.config(style=MAIN.CONTENT_TFRAME)
        self.notif_label = app.main_notif
        self.app = app
    
    def show(self):
        self.pack(fill='both', expand=1)
    
    def generate_notification(self, label:tk.Label, msg:str, style:str, delay:int=1000):
        """Display msg for label with given style after delay in milisecond then remove msg and restore style"""
        old_style = label.cget("style")
        label.config(text=msg, style=style)
        self.app.root.after(delay, lambda: label.config(text="", style=old_style))


class ManagerFrame(ViewFrame):
    
    def __init__(self, app: 'App', **kw):
        super().__init__(app, app.container, **kw)
        self.settings = app.settings.new_settings

        self.timer = self.settings['timer']['inactivity']
        self.initial_time = time.time() # Check Time for inactivity
        
        self.toggle_to_right = '»»»'
        self.toggle_to_left  = '«««'

        # Load icons (adjust path in tools.py/AppSettings class)
        icons_path = self.settings["icons"]['ManagerFrame']
        self.icons = {
            "add": tk.PhotoImage(file=icons_path['add']),
            "import": tk.PhotoImage(file=icons_path['import']),
            "export": tk.PhotoImage(file=icons_path['export']),
            "settings": tk.PhotoImage(file=icons_path['settings']),
            "logout": tk.PhotoImage(file=icons_path['logout'])
        }
        self.sidebar_frame = tk.Frame(self, style=MAIN.SIDEBAR_TFRAME)# bg="lightgray")
        self.content_frame = tk.Frame(self, style=MAIN.CONTENT_TFRAME)
        self.counter_size = 30
        self.count_down = CountDown(
            self.app.root, self.counter_size, self.settings['timer']['clipboard']*1000
        )
        self.table_length = 0
        self.table_data = []
        self.load_ui()
        app.root.bind("<Button>", self.__reset_root_timer)
        app.root.bind("<Key>", self.__reset_root_timer)
        
    
    def __reset_root_timer(self, event):
        self.initial_time = time.time()
        self.timer = self.settings['timer']['inactivity']
        self.app.root.after(1000, self.__bind_toplevel)
    
    def __reset_toplevel_timer(self, event):
        self.initial_time = time.time()
        self.timer = self.settings['timer']['inactivity']
    
    def __bind_toplevel(self):
        for window in self.app.root.winfo_children(): 
            if isinstance(window, tk.Toplevel):
                window.bind("<Button>", self.__reset_toplevel_timer)
                window.bind("<Key>", self.__reset_toplevel_timer)

    def inactivity_ckeck(self):
        if time.time() - self.initial_time > self.timer:
            self.logout()
            return
        
        self.app.root.after(1000, self.inactivity_ckeck)

    def load_ui(self):
        
        self.sidebar_frame.pack(side='left',padx=1,pady=5,fill='y')
        self.content_frame.pack(side='left',padx=(1,5),pady=5, fill='both', expand=1)
        
        self.count_down.config_arc(fill='orange')
        self.count_down.config(background=self.app.style.CONTENT_BG)
        self.count_down.on_end = self.on_count_down_end
        self.app.root.bind("<<StyleUpdated>>", self.on_style_update)

        self.toggle_btn = tk.Label(self.sidebar_frame, text=self.toggle_to_right, style=MAIN.SIDEBAR_TLABEL)
        self.toggle_btn.pack()
        self.add_btn = tk.Button(self.sidebar_frame,text="", compound='left', image=self.icons["add"], command=self.add_new_row,style=MAIN.SIDEBAR_TBUTTON)
        self.import_btn = tk.Button(self.sidebar_frame,text="", compound='left', image=self.icons["import"], command=self.load_csv,style=MAIN.SIDEBAR_TBUTTON)
        self.export_btn = tk.Button(self.sidebar_frame,text="", compound='left', image=self.icons["export"], command=self.save_csv,style=MAIN.SIDEBAR_TBUTTON)
        self.settings_btn = tk.Button(self.sidebar_frame,text="", compound='left', image=self.icons["settings"],
                                     command=self.show_settings,style=MAIN.SIDEBAR_TBUTTON)
        self.logout_btn = tk.Button(self.sidebar_frame,text="", compound='left', image=self.icons["logout"], command=self.logout,style=MAIN.SIDEBAR_TBUTTON)
        self.toggle_btn.bind("<Button-1>", self.toggle_to_right_clicked)

        # Treeview setup
        columns = ("ID", "Site", "Username", "Password", "Extra_Info")
        columns_iconic = ("ID", "🌐 Site", "👤 Username", "🔑 Password", "🕮 Extra_Info")
        self.tree = CustomTreeview(
            self.content_frame, columns=columns,
            show="headings", style=MAIN.CUSTOM_TREEVIEW, height=5
        )
        
        for col, col_icon in zip(columns, columns_iconic):
            self.tree.heading(col, text=col_icon, anchor='center')
            self.tree.column(col, anchor='center',stretch=True)
        self.tree.column("ID", width=40)
        
        self.app.style.update_tree_color(self.app.root)
        # Enable Right click options for table(CustomTreeview)
        self.tree.enable_context_menu(self.show_tree_menu)
        self.tree.add_context_menu('Show', self.table_show_item)
        self.tree.add_context_menu('Copy', self.table_copy_cell)
        self.tree.add_context_menu('Edit', self.table_edit_item)
        self.tree.add_context_menu('Remove', self.table_remove_item)
        self.tree.add_context_menu('clear', self.table_selection_remove)
        self.tree.pack(fill='both', expand=True)

        # Create search box
        search_frame = tk.Frame(self.content_frame, style=MAIN.CONTENT_TFRAME)
        search_frame.pack(padx=5, fill='x')
        search_label_l = tk.Label(search_frame, text="Search:", style=MAIN.CONTENT_TLABEL)
        search_label_l.pack(side=tk.LEFT, pady=(0,5))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var, style=MAIN.CONTENT_TENTRY
        )
        self.search_entry.pack(side=tk.LEFT,pady=(0,5), fill='x')
        self.search_var.trace_add("write", self.on_search)  # Trigger search on text change

        # Load data and add them to table
        self.table_data, _ = self.app.db.get_column_values("users_data", "site", self.app.user_id)
        self.table_length = len(self.table_data)
        self.search_label_r = tk.Label(
            search_frame, text=f"Result: {self.table_length} row(s)",
            style=MAIN.CONTENT_TLABEL
        )
        self.search_label_r.pack(side=tk.LEFT, pady=(0,5), fill='x')
        self.load_data()
        self.animate_sidebar()

        # self.app.root.bind("<<KeyGenerated>>", lambda e: self.animate_sidebar())
    
    def animate_sidebar(self):
        """Pack the sidebar buttons with simple animation"""
        self.app.root.after(100, lambda:self.add_btn.pack(padx=5,pady=3,fill='x'))
        self.app.root.after(200, lambda:self.import_btn.pack(padx=5,pady=3,fill='x'))
        self.app.root.after(300, lambda:self.export_btn.pack(padx=5,pady=3,fill='x'))
        self.app.root.after(400, lambda:self.settings_btn.pack(padx=5,pady=3,fill='x'))
        self.app.root.after(500, lambda:self.logout_btn.pack(padx=5,pady=3,fill='x'))
        self.app.root.after(1000, self.inactivity_ckeck)

    def toggle_to_left_clicked(self, event):
        """Toggle sidebar to left"""
        self.toggle_btn.config(text=self.toggle_to_right)
        self.toggle_btn.bind("<Button-1>", self.toggle_to_right_clicked)
        for widget in self.sidebar_frame.winfo_children()[1:]:
            widget.configure(text='')
    
    def toggle_to_right_clicked(self, event):
        """Toggle sidebar to right"""
        self.toggle_btn.config(text=self.toggle_to_left) # » « 🡄 🡆
        self.toggle_btn.bind("<Button-1>", self.toggle_to_left_clicked)
        self.add_btn.config(text=' Add New')
        self.import_btn.config(text=' Import')
        self.export_btn.config(text=' Export')
        self.settings_btn.config(text=' Settings')
        self.logout_btn.config(text=' Logout')

    def get_table_rows(self):
        for child in self.tree.get_children():
            yield self.tree.item(child)['values']
    
    def on_search(self, *args):
        search_text = self.search_var.get().strip().lower()
        filtered_data = [
            row for row in self.table_data if search_text in row[1].lower()
        ]
        self.populate_treeview(filtered_data)
        self.search_label_r.config(text=f"Result: {len(filtered_data)} row(s)")
    
    def on_style_update(self, event):
        self.count_down.config(background=self.app.style.CONTENT_BG)

    def on_count_down_end(self):
        self.count_down.place_forget()
        self.app.clipboard.del_copy()
    
    def show_tree_menu(self, event):
        # Get item and column under mouse
        selected_items = list(self.tree.selection())
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)        
        if item:
            if item not in selected_items:
                selected_items = (item,)
            self.tree.selection_set(*selected_items)
            self.tree.current_item = item
            self.tree.current_column = column
            
            if len(selected_items)>1:
                for name in ['Show', 'Edit', 'Copy']:
                    self.tree.config_menu_item(name, state=tk.DISABLED)
            else:
                for name in ['Show', 'Edit', 'Copy']:
                    self.tree.config_menu_item(name, state=tk.NORMAL)
            self.tree.context_menu.post(event.x_root, event.y_root)

    def table_selection_remove(self):
        self.tree.selection_remove(self.tree.selection())
    
    def table_edit_item(self):
        self.notif_label.config(text='', style=MAIN.CUSTOM_TLABEL)
        EditRowPopUp(self.app, 500, 200, "Edit seleted row and update Database.")
    
    def table_remove_item(self):
        items = self.tree.selection()
        if items:
            ans = messagebox.askyesno(
                "Removing data",
                f"Are you sure about deleting {len(items)} {'row' if len(items)==1 else 'rows'}"
            )
            if ans:
                n_success = 0
                n_failed = 0
                for item in items:
                    row = self.tree.item(item)["values"]
                    result, msg = self.app.db.remove_user_data(row[0])
                    if result:
                        n_success += 1
                        self.tree.delete(item) 
                        self.table_data.remove((row[0], row[1]))
                    else:
                        print(msg)
                        n_failed += 1
                s_success = 'rows' if n_success>1 else 'row'
                s_failed = 'rows' if n_failed>1 else 'row'
                msg = f"The deletion of {n_success} {s_success} was successful and {n_failed} {s_failed} failed."
                self.generate_notification(self.app.main_notif, msg, INFO_TL, 5000)
                self.table_length -= n_success
                self.search_label_r.config(text=f"Result: {self.table_length} row(s)")
    
    def table_copy_cell(self):
        item = self.tree.current_item
        if item:
            row = self.tree.item(item)["values"]
            cols = list(self.tree['columns'])
            data_id = row[0]
            col_name = self.tree.column(self.tree.current_column)["id"]
            if col_name in ['ID','Site']:
                result = row[cols.index('Site')]
                self.app.clipboard.set_copy(result)
                return
            result, msg = self.app.db.get_specific_column(data_id, self.app.user_id, col_name)
            if result:
                result = self.app.encryption.decrypt(self.app.fernet_key, result)
                if not self.count_down.is_counting:
                    t = self.app.settings.new_settings['timer']['clipboard']
                    self.generate_notification(self.app.main_notif, f"You have {t} second to use clipboard.", MAIN.CONTENT_TLABEL, t*500)
                    self.count_down.place(relx=0.9, y=self.counter_size+1, anchor='se')
                    self.count_down.total_time = t*1000
                    
                self.count_down.start()
                self.app.clipboard.set_copy(result)
    
    def table_show_item(self):
        self.notif_label.config(text='', style=MAIN.CUSTOM_TLABEL)
        ShowRowPopUp(self.app, 500, 200, 'Show info for selected row.')
        
    def table_insert_data(self, data_id, site:str):
        if data_id:
            tag = ('even', ) if self.table_length%2==0 else ('odd',)
            item = self.tree.insert('', 'end', values=[data_id, site, "****", "****", "****"], tags=tag)
            self.tree.selection_set(item)
            self.table_data.append((data_id, site))
            self.table_length += 1
            self.search_label_r.config(text=f"Result: {self.table_length} row(s)")
            return True
        return False

    def populate_treeview(self, data):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert data into Treeview
        row_tag = ('odd',)
        for row in data:
            row_tag = ('even',) if row_tag==('odd',) else ('odd',)
            self.tree.insert("", "end", values=[row[0],row[1],"****","****","****"], tags=row_tag)
    
    def load_data(self):
        if self.table_data:
            row_tag = ('odd',)
            for row in self.table_data:
                row_tag = ('even',) if row_tag==('odd',) else ('odd',)
                self.tree.insert("", "end", values=[row[0],row[1],"****","****","****"], tags=row_tag)  # row is (data_id, user_id, c1, c2, c3, c4)

    def load_csv(self):
        self.notif_label.config(text='', style=MAIN.CUSTOM_TLABEL)
        ImportDataPopUp(self.app, 550, 250, 'select which type of file you want to extract data from.')

    def save_csv(self):
        self.notif_label.config(text='', style=MAIN.CUSTOM_TLABEL)
        ExportDataPopUp(self.app, 350, 200, "Export Data to CSV or TXT format")

    def show_settings(self):
        self.notif_label.config(text='', style=MAIN.CUSTOM_TLABEL)
        popup_width = 600
        popup_height = 300
        SettingsPopup(self.app, popup_width, popup_height, "Settings")
    
    def add_new_row(self):
        self.notif_label.config(text='', style=MAIN.CUSTOM_TLABEL)
        AddNewPopup(self.app, 500, 200, " Add New Info to database ")
    
    def logout(self):
        for window in self.app.root.winfo_children(): 
            if isinstance(window, tk.Toplevel):
                window.destroy()
        self.app.mark_inactive()
        self.app.root.unbind_all("<Button>")
        self.app.root.unbind_all("<Key>")


class SetAccountFrame(ViewFrame):
    
    def __init__(self, app: 'App', **kw):
        super().__init__(app, app.container, **kw)
        # self.config(style=MAIN.CUSTOM_TFRAME)
        self.account = None
        
        icons_path = app.settings.new_settings["icons"]['SetAccountFrame']
        
        # Lables widgets for giving info to users about app
        line0 = "Set Up Your Account Name And Password."
        line1 = "Make Sure Your Sensitive Data Remain Safe."
        self.lable0 = tk.Label(self, text=line0, font = ('Times', 28, 'normal'), style=MAIN.CUSTOM_TLABEL)
        self.label1 = tk.Label(
            self, text=line1, justify='left', style=MAIN.CUSTOM_TLABEL, font=('Times', 20, 'normal'),
            foreground=app.style.SUCCESS
        )
        # Lables widgets pack
        self.lable0.pack(padx=10,pady=(50,10))
        self.label1.pack(padx=10, pady=(0,5))
        
        # Authentication Entries widgets, create and pack
        img = tk.PhotoImage(file=icons_path['add_user_icon'])
        img_label = tk.Label(self, image=img, style=MAIN.CUSTOM_TLABEL)
        img_label.pack(padx=5, pady=5)
        img_label.image = img # Keep a reference to the image to prevent garbage collection

        fields_frame = tk.Frame(self, style=MAIN.CUSTOM_TFRAME)
        fields_frame.pack(padx=10)

        self.account_entry = CustomEntry(
            fields_frame,
            app.style,
            icons_path['entry_username'],
            hover_color='green'
        )
        self.account_entry.pack(padx=5,pady=5)
        self.p1 = PasswordEntry(
            fields_frame,
            app.style,
            icons_path['entry_open_eye'],
            icons_path['entry_close_eye'],
            "Enter Password",
            hover_color='green',
            tooltip=tlp
        )
        self.p2 = PasswordEntry(
            fields_frame,
            app.style,
            icons_path['entry_open_eye'],
            icons_path['entry_close_eye'],
            "Confirm Password",
            hover_color='green',
            tooltip=tlp
        )
        self.p1.pack(padx=5,pady=5)
        self.p2.pack(padx=5,pady=5)
        
        # Button widget create and pack
        self.confirmButton = tk.Button(
            fields_frame, text="Create Account", 
            command=self.confirmation
        )
        self.confirmButton.pack(pady=2, padx=5, fill='x')
        self.confirm_label = tk.Label(fields_frame, text="", style=MAIN.CONTENT_TLABEL)
        self.confirm_label.pack(padx=5)
        self.app.root.bind(
            "<Return>",
            lambda e: self.confirmation()
        )
        self.account_entry.entry.focus()
    
    def confirmation(self):
        username = self.account_entry.get()
        password = self.p1.get()
        confirm_password = self.p2.get()
        msg = "Consider the following:"
        msg += "\nusername is empty" if not username else ''
        msg += '\npassword is empty' if not password else ''
        msg += '\nconfirm password is empty' if not confirm_password else ''
        if "empty" in msg:
            messagebox.showerror("Error", msg)
            # self.app.main_notif.config(text=msg, style=WARNING_TL)
            return
        if password != confirm_password:
            messagebox.showerror("Error", "password dose not match!")
            return
        salt , msg = self.app.create_account(username, password)
        if salt:
            
            # self.p2.entry.unbind("<KeyPress-Return>")
            self.app.root.unbind("<Return>")
            self.confirmButton.configure(state=tk.DISABLED)
            self.confirm_label.config(text="Please wait to generate your key...", style=SUCCESS_TL)
            self.app.root.after(10, self.app.key_maker, password.encode(), salt)
            self.app.root.bind("<<KeyGenerated>>", lambda e: self.app.mark_to_manager())
            return
        self.generate_notification(self.app.main_notif, msg, DANGER_TL)


class LoginFrame(ViewFrame):
    
    def __init__(self, app: 'App', **kw):
        super().__init__(app, app.container, **kw)
        
        usernames, message = app.db.get_usernames()
        icons_path = app.settings.new_settings["icons"]['LoginFrame']

        bg_image = Image.open(icons_path['background'])
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self, image=self.bg_photo, style=MAIN.CUSTOM_TLABEL)
        bg_label.place(x=0, y=0)#, relwidth=1, relheight=1)
        bg_label.image = self.bg_photo  # Prevent garbage collection
        
        main_frame = tk.Frame(self, style=MAIN.CUSTOM_TFRAME)
        main_frame.pack(padx=20, anchor='e')

        label = tk.Label(
            main_frame, text='Welcome Back\nSecurity is the first priority',
            justify='center',
            style=MAIN.CUSTOM_TLABEL,
            font=('Arial', 18, "bold")
        )
        label.pack(pady=(10,20))
        
        # Image label
        img = tk.PhotoImage(file=icons_path['user_icon'])
        img_label = tk.Label(main_frame, image=img, style=MAIN.CUSTOM_TLABEL)
        img_label.pack(pady=5)
        img_label.image = img # Keep a reference to the image to prevent garbage collection

        fildes_frame = tk.Frame(main_frame, style=MAIN.CUSTOM_TFRAME)
        fildes_frame.pack(pady=5)

        # Authentication Fields
        self.password = PasswordEntry(
            fildes_frame,
            app.style,
            icons_path['entry_open_eye'],
            icons_path['entry_close_eye'],
            "Enter Password",
            hover_color='green',
            tooltip=tlp
        )
        self.username_combo = tk.Combobox(fildes_frame, values=usernames, style=MAIN.CUSTOM_TCOMBOBOX, state='readonly')
        self.login_btn = tk.Button(fildes_frame,text='Login', style=MAIN.OUTLINE_TBUTTON, width=30)
        self.login_label = tk.Label(fildes_frame, text="", style=MAIN.CONTENT_TLABEL)
        if usernames:
            self.username_combo.set(usernames[0])

        # Pack Authentication Fields
        self.username_combo.pack(pady=2, fill='x')
        self.password.pack(pady=2, fill='x')
        self.login_btn.pack(pady=2)
        self.login_label.pack(pady=2)
        self.password.entry.focus()
        
        self.login_btn.config(command=lambda: self.login(self.username_combo.get(), self.password.get()))
        self.fid = self.app.root.bind("<Return>", lambda e: self.login(self.username_combo.get(), self.password.get()))
    
    def login(self, username, password):
        if not password:
            self.generate_notification(self.app.main_notif, "Password cannot be empty.", WARNING_TL)
            return
        salt, msg = self.app.login(username, password)
        if salt:
            self.app.root.unbind("<Return>", self.fid)
            # self.app.root.after(100, self.app.key_maker, password.encode(), salt)
            self.login_btn.config(state=tk.DISABLED)
            self.login_label.config(text="Please wait to generate your key...", style=SUCCESS_TL)
            self.app.root.after(10, self.app.key_maker, password.encode(), salt)
            self.app.root.bind("<<KeyGenerated>>", lambda e: self.app.mark_to_manager())
            return
        self.generate_notification(self.app.main_notif, msg, DANGER_TL)


class DatabaseErrorFrame(ViewFrame):
    
    def __init__(self, app:'App', *args, **kwrgs):
        super().__init__(app, app.container, *args, **kwrgs)
        # Lables widgets for giving info to users about app
        lable0 = tk.Label(
            self, text="Database Error", font = ('Times', 28, 'normal'), style=MAIN.CUSTOM_TLABEL,
             foreground=app.style.WARNING
        )
        lable0.pack(padx=10, pady=10)

        info_frame = tk.Frame(self, style=MAIN.CUSTOM_TFRAME)
        info_frame.pack()
        if "RuntimeError" in self.app.db_error:
            info = f"{'\n'.join(self.app.db_error)}\nReplace with a backup or delete the file"
            fg = app.style.DANGER
            justify='center'
            l = tk.Label(
                info_frame, text=info, justify=justify, style=MAIN.CUSTOM_TLABEL, font=('Times', 18, 'normal'),
                foreground=fg)
            l.pack(anchor='w')
        else:
            justify='left'
            for msg in self.app.db_error:
                info = ""
                if "not" in msg:
                    info = msg+ "❌" 
                    fg = app.style.DANGER
                else:
                    info = msg+ "✔️"
                    fg = app.style.SUCCESS
                
                l = tk.Label(
                    info_frame, text=info, justify=justify, style=MAIN.CUSTOM_TLABEL, font=('Times', 18, 'normal'),
                    foreground=fg)
                l.pack(anchor='w')
        
        label2 = tk.Label(
            self, text=f"The path to your database file:\n{self.app.db_path}", justify='center', 
            style=MAIN.CUSTOM_TLABEL, font=('Times', 14, 'normal'), foreground=app.style.INFO
        )
        label2.pack(padx=10, pady=10)
        
