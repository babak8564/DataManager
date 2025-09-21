import ttkbootstrap as tk
from PIL import Image, ImageTk
from tkinter import font as tkfont, Menu
from FrontEnd.styles import CryptoStyle, MAIN


class CustomTreeview(tk.Treeview):
    
    def __init__(self, master, columns, **kwargs):
        super().__init__(master, columns=columns, **kwargs)
        self.sort_order = {}  # Track sort order for each column
        self.options_indx = {} # Save index of any option menu str:int
        self.current_item:str = None
        self.current_column:str = None
        # Configure columns
        for col in columns:
            self.heading(col, text=col, anchor='center', command=lambda c=col: self.sort_column(c))
            self.sort_order[col] = 'asc'
    
    def enable_context_menu(self, show_context_menu, *arg):
        self.bind("<Button-3>", lambda e: show_context_menu(e, *arg))
        self.context_menu = Menu(self, tearoff=0)
        # if not hasattr(self, "options"):
        #     self.options = []
    
    def sort_column(self, col):
        # Get all items
        items = [(self.set(item, col), item) for item in self.get_children()]
        
        # Convert to appropriate type for sorting
        try:
            items = [(float(val), item) if val.replace('.', '', 1).isdigit() else (val, item) 
                    for val, item in items]
        except:
            pass
            
        # Sort
        items.sort(reverse=(self.sort_order[col] == 'desc'))
        
        # Rearrange items
        for index, (val, item) in enumerate(items):
            self.move(item, '', index)
            
        # Toggle sort order
        self.sort_order[col] = 'desc' if self.sort_order[col] == 'asc' else 'asc'
        
    def add_context_menu(self, name:str, func, *arg):
        self.context_menu.add_command(label=name, command=lambda:func(*arg))
        self.options_indx[name] = len(self.options_indx)
        # self.options.append(name)
    
    def config_menu_item(self, name, **kw):
        self.context_menu.entryconfig(self.options_indx[name], **kw)
    
  
class CustomEntry(tk.Frame):
    idx = 0
    _style_registry = {}

    def __init__(
        self,
        parent,
        style_object:CryptoStyle,
        image_path=None,
        image=None,
        image_side="right",
        hover_color=None,
        on_image_click=None,
        **kwargs
    ):
        super().__init__(parent)
        
        self.style = style_object.style
        self.hover_color = hover_color

        self.fcustom = f"Custom{CustomEntry.idx}.TFrame"
        style_object.add_style(self.fcustom, background="ENTRY_BG", borderwidth=1, relief='solid', bordercolor="REGULAR_BG")
        CustomEntry.idx += 1

        # Font setup
        font_size =  9 if style_object.variant == "small" else 11 if style_object.variant=='medium' else 13
        self.entry_font = ("Arial", font_size)

        # Set up the holding frame
        self.entry_frame = tk.Frame(self, style=self.fcustom, border=1)
        self.entry_frame.pack(fill="x")
        self.entry_frame.bind("<Enter>", lambda e: self.update_border("Hover",style_object))
        self.entry_frame.bind("<Leave>", lambda e: self.update_border("Leave", style_object))

        # Container for image and entry
        self.container = tk.Frame(self.entry_frame, style=self.fcustom, borderwidth=0, border=0)
        self.container.pack(fill="x")

        # Entry
        self.entry = tk.Entry(self.container, style=MAIN.CONTENT_TENTRY, **kwargs)
        
        # Calculate image size
        font_obj = tkfont.Font(font=self.entry_font)
        font_height = font_obj.metrics("linespace") or 16
        image_size = max(16, int(font_height * 1.5))

        # Load and resize image
        if image_path:
            self.original_img = Image.open(image_path).convert("RGBA")
        elif image:
            self.original_img = image.convert("RGBA")
        else:
            self.original_img = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
        img = self.original_img.resize((image_size, image_size), Image.LANCZOS)
        self.entry_img = ImageTk.PhotoImage(img)

        # Image label
        self.img_label = tk.Label(self.container, image=self.entry_img, style=MAIN.CUSTOMIMG_TLABEL)
        self.img_label.image = self.entry_img
        
        if image_side.lower() == "right":
            self.img_label.pack(side="right", padx=(0,2))
            self.entry.pack(side="right", fill="x", expand=True, padx=(2, 0))
        else:
            self.img_label.pack(side="left", padx=(2,0))
            self.entry.pack(side="left", fill="x", expand=True, padx=(0, 2))

        # Make image clickable
        self.on_image_click = on_image_click
        self.image_list = [self.original_img]
        self.current_image_index = 0
        self.img_label.bind("<Button-1>", self._handle_image_click)
        self.configure(font=self.entry_font)
        self.entry.bind("<Configure>", self._update_image_size)

    def update_font(self, font):
        print("Class: Detected variable update. new font: ", font)
        self.configure(font=font)
    
    def _handle_image_click(self, event):
        if self.on_image_click:
            self.on_image_click(self)
        else:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            self.set_image(image=self.image_list[self.current_image_index])

    def update_border(self, name, style_object:CryptoStyle):
        if name=="Leave":
            color = style_object.REGULAR_BG
        else:
            color = self.hover_color or style_object.OTHER_BUTTON
        style_object.style.configure(
            self.fcustom,
            bordercolor=color
        )

    def _update_image_size(self, event=None):
        font_obj = tkfont.Font(font=self.entry.cget("font"))
        font_height = font_obj.metrics("linespace") or 16
        image_size = max(16, int(font_height * 1.5))
        if hasattr(self, "original_img"):
            img = self.original_img.resize((image_size, image_size), Image.LANCZOS)
            self.entry_img = ImageTk.PhotoImage(img)
            self.img_label.configure(image=self.entry_img, style=MAIN.CUSTOMIMG_TLABEL)
            self.img_label.image = self.entry_img

    def configure(self, **kwargs):
        if "font" in kwargs:
            self.entry_font = kwargs["font"]
            self.entry.configure(font=self.entry_font)
            self._update_image_size()
            kwargs.__delitem__('font')
        super().configure(**kwargs)

    def get(self):
        return self.entry.get()

    def set_image(self, image_path=None, image=None):
        if image_path:
            self.original_img = Image.open(image_path).convert("RGBA")
        elif image:
            self.original_img = image.convert("RGBA")
        else:
            return
        self._update_image_size()

    def add_alternate_image(self, image_path=None, image=None):
        if image_path:
            img = Image.open(image_path).convert("RGBA")
        elif image:
            img = image.convert("RGBA")
        else:
            return
        self.image_list.append(img)
        if len(self.image_list) == 1:
            self.original_img = img
            self._update_image_size()


class ToolTip:
    def __init__(self, bg='red', fg='silver', font=('Arial', 9)):
        self.__tooltip = None
        self.bg = bg
        self.fg = fg
        self.font = font
    
    def show(self, widget, msg):
        if self.__tooltip:
            return
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() - 20
        y += widget.winfo_rooty() - 20
        self.__tooltip = tk.Toplevel(widget)
        
        self.__tooltip.wm_overrideredirect(True)
        
        self.__tooltip.config(background=self.bg)
        l = tk.Label(self.__tooltip, text=msg, background=self.bg, foreground=self.fg, font=self.font)
        l.pack(side='left')
        b = tk.Button(self.__tooltip, text="X", command=self.__destroy_tip)
        b.pack(side='left')

        lwidth = l.winfo_reqwidth()
        bwidth = b.winfo_reqwidth()

        width = lwidth+bwidth
        height = max(b.winfo_reqheight(),l.winfo_reqheight())
        self.__tooltip.wm_geometry(f"{width}x{height}+{x}+{y}")
        widget.after(5000, self.__destroy_tip)
    
    def __destroy_tip(self):
        if self.__tooltip:
            self.__tooltip.destroy()
            self.__tooltip = None


class PasswordEntry(CustomEntry):
    
    def __init__(
        self,
        parent,
        style_object:CryptoStyle,
        open_eye_path,
        close_eye_path,
        placeholder="Enter your Password",
        placeholder_color="#808080",
        image_side="right",
        hover_color=None,
        tooltip:ToolTip=None,
        **kwargs
    ):
        super().__init__(
            parent,
            style_object=style_object,
            image_path=close_eye_path,
            image_side=image_side,
            hover_color=hover_color,
            show="",
            **kwargs
        )

        self.tooltip = tooltip
        okeycommand = None
        if tooltip:
            okeycommand = self.register(self.isOkay_tooltip)
        else:
            okeycommand = self.register(self.isOkay)

        self.open_eye_img = Image.open(open_eye_path).convert("RGBA")
        self.close_eye_img = Image.open(close_eye_path).convert("RGBA")
        self.image_list = [self.close_eye_img, self.open_eye_img]
        self.is_password_hidden = True

        self.on_image_click = self._toggle_password
        self.img_label.bind("<Button-1>", self._handle_image_click)

        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.typed_color = style_object.Entry_FG
        self.style.configure( # need to modified
            MAIN.CONTENT_TENTRY,
            foreground=self.placeholder_color
        )

        self.entry.config(validate="key", validatecommand=(okeycommand, "%S"))
        self.entry.insert(0, self.placeholder)
        self.is_placeholder = True

        self.entry.bind("<FocusIn>", self.focusIn)
        self.entry.bind("<FocusOut>", self.focusOut)

    def isOkay(self, what):
        # print(why, where, what)
        if what in ['',' ', ',', '.', '\\']:
            return False
        elif (" " in what) and (what!=self.placeholder):
            return False
        return True
    
    def isOkay_tooltip(self, what):
        if what in ['',' ', ',', '.', '\\']:
            self.tooltip.show(self, f"Password can't contain -{what}-. Invalid charachters -> [\\   ,   .   white space] ")
            return False
        elif (" " in what) and (what!=self.placeholder):
            self.tooltip.show(self, f"Password can't contain white space.")
            return False
        return True

    def _toggle_password(self, widget):
        if self.is_password_hidden:
            show=""
            self.set_image(image=self.open_eye_img)
            self.is_password_hidden = False
        else:
            show="*"
            self.set_image(image=self.close_eye_img)
            self.is_password_hidden = True
        if self.is_placeholder:
            show = ''
        self.entry.configure(show=show)

    def focusIn(self, event):
        if self.is_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(style=MAIN.CONTENT_TENTRY, foreground=self.typed_color)
            if self.is_password_hidden:
                self.entry.configure(show="*")
            self.is_placeholder = False

    def focusOut(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.configure(style=MAIN.CONTENT_TENTRY, foreground=self.placeholder_color,show="")
            self.is_placeholder = True

    def get(self):
        if self.is_placeholder:
            return ""
        return self.entry.get()


class CountDown(tk.Canvas):
    def __init__(self, master, size, total_time=60000, **kwg):
        """total_time and dt(interval) are in milisecond"""
        super().__init__(master, width=size+1, height=size+1, **kwg)
        self.arc_options = {'start': 90, 'extent':0, 'fill':'yellow'}
        self.arc_id = self.create_arc(
            0, 0, size, size, **self.arc_options
        )
        self.counter_size = size
        self.delta_t = int(total_time/100)
        self.delta_deg = 3.6
        self.degree = 0
        self.is_counting = False
        self.on_end = None

    @property
    def total_time(self):
        return self.delta_t*100
    
    @total_time.setter
    def total_time(self, total_time):
        self.delta_t = int(total_time/100)
    
    def config_arc(self, **kwg):
        for key in kwg:
            self.arc_options[key] = kwg[key]
        if self.arc_id:
            self.itemconfig(self.arc_id, **self.arc_options)
    
    def start(self):
        if self.arc_id is None:
            self.arc_id = self.create_arc(
                0, 0, self.counter_size, self.counter_size,
                **self.arc_options
            )
        self.degree = 0
        if not self.is_counting:
            self.__counting()
            self.is_counting = True
    
    def __counting(self):
        if (self.degree - self.delta_deg) > -360:
            self.degree -= self.delta_deg
            self.itemconfig(self.arc_id, extent=self.degree)
            self.master.after(self.delta_t, self.__counting)
        else:
            self.delete(self.arc_id)
            self.arc_id = None
            self.is_counting = False
            if self.on_end:
                self.on_end()


class Entry(tk.Entry):
    
    def __init__(self,master, inittext='click here ...', **kwg) -> None:
        super().__init__(master=master,**kwg)
        self.fg = self['foreground']
        self.config(foreground='gray')
        self.initText = inittext
        self.insert(0, self.initText)
        self.bind("<FocusIn>", self.focusIn)
        self.bind("<FocusOut>", self.focusOut)

    def result(self):
        text = self.get()
        if text == self.initText:
            return ''
        return text
        
    
    def focusIn(self, event=None):
        text = self.get()
        if text == self.initText:
            self.delete(0, 'end')
            self.config(foreground=self.fg)
    
    def focusOut(self, event=None):
        text = self.get()
        if not text:
            self.delete(0, 'end')
            self.config(foreground='gray')
            self.insert(0, self.initText)
    
    def themeChanged(self, fg):
            self.fg = fg
            text = self.get()
            if text and text!=self.initText:
                self.delete(0, 'end')
                self.config(foreground=self.fg)
                self.insert(0, text)
    def setstr(self, index: str | int, string: str) -> None:
        self.config(foreground=self.fg)
        self.insert(index, string)
    
    def reset(self):
        self.delete(0, 'end')
        self.config(foreground='gray')
        self.insert(0, self.initText)


class Text(tk.Text):
    
    def __init__(self,master, inittext='click here ...', **kwg) -> None:
        super().__init__(master=master,**kwg)
        self.fg = self['foreground']
        self.config(foreground='gray')
        self.initText = inittext
        self.insert('1.0', self.initText)
        self.bind("<FocusIn>", self.focusIn)
        self.bind("<FocusOut>", self.focusOut)
    
    def result(self):
        text = self.get('1.0','end-1c')
        if text == self.initText:
            return ''
        return text
    
    def focusIn(self, event=None):
        text = self.get('1.0', '1.end')
        if text == self.initText:
            self.delete('1.0', '1.end')
            self.config(foreground=self.fg)
    
    def focusOut(self, event=None):
        text = self.get('1.0', '1.end')
        if not text:
            self.delete('1.0', '1.end')
            self.config(foreground='gray')
            self.insert('1.0', self.initText)
    
    def themeChanged(self, fg):
            self.fg = fg
            text = self.get('1.0', '1.end')
            if text and text!=self.initText:
                self.delete('1.0', '1.end')
                self.config(foreground=self.fg)
                self.insert('1.0', text)
    
    def setstr(self, index: str | float, chars: str, *args: str | list[str] | tuple[str, ...]) -> None:
        self.config(foreground=self.fg)
        self.insert(index, chars, *args)
    
    def reset(self):
        self.delete('1.0', 'end')
        self.config(foreground='gray')
        self.insert('1.0', self.initText)

