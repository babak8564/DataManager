# import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

SUCCESS_TL = 'Success.TLabel'
WARNING_TL = 'Warning.TLabel'
INFO_TL    = 'Info.TLabel'
DANGER_TL  = 'Danger.TLabel'


class MAIN:
    # TFrame Style Names
    CUSTOM_TFRAME  = 'Main.Custom.TFrame'
    CONTENT_TFRAME = 'Main.Content.TFrame'
    SIDEBAR_TFRAME = 'Main.Sidebar.TFrame'
    CUSTOMEIMG_TFRAME  = 'Main.CustomEimg.TFrame'
    # HOVEREIMG_TFRAME  = 'Main.CustomEimg.TFrame'
    
    # TButton Style Names
    CUSTOM_TBUTTON  = 'Main.Custom.TButton'
    OUTLINE_TBUTTON = 'Main.Outline.TButton'
    CONTENT_TBUTTON = 'Main.Content.TButton'
    SIDEBAR_TBUTTON = 'Main.Sidebar.TButton'
    TEXT_TBUTTON    = 'Main.Link.TButton'
    
    # TEntry Style Names
    CUSTOM_TENTRY = 'Main.Custom.TEntry'
    CONTENT_TENTRY = 'Main.Content.TEntry'
    # SIDEBAR_TENTRY = 'Main.Sidebar.TEntry'
    
    # TLabel Style Names
    CUSTOM_TLABEL = 'Main.Custom.TLabel'
    CUSTOMIMG_TLABEL = 'Main.CustomImg.TLabel'
    CONTENT_TLABEL = 'Main.Content.TLabel'
    SIDEBAR_TLABEL = 'Main.Sidebar.TLabel'
    
    # TCombobox Style Names Treeview
    CUSTOM_TCOMBOBOX = 'Main.Custom.TCombobox'
    # CONTENT_TCOMBOBOX = 'Main.Content.TCombobox'
    # SIDEBAR_TCOMBOBOX = 'Main.Sidebar.TCombobox'
    
    # Treeview Style Names
    CUSTOM_TREEVIEW = 'Main.Custom.Treeview'
    # CONTENT_TREEVIEW = 'Main.Content.Treeview'
    # SIDEBAR_TREEVIEW = 'Main.Sidebar.Treeview'


class POPUP:
    # TFrame Style Names
    CUSTOM_TFRAME = 'Popup.Custom.TFrame'
    CONTENT_TFRAME = 'Popup.Content.TFrame'
    SIDEBAR_TFRAME = 'Popup.Sidebar.TFrame'
    
    # TButton Style Names
    CUSTOM_TBUTTON = 'Popup.Custom.TButton'
    CONTENT_TBUTTON = 'Popup.Content.TButton'
    SIDEBAR_TBUTTON = 'Popup.Sidebar.TButton'

    # TRadioButton
    CUSTOM_TRADIOBTN = "Custom.TRadiobutton"
    CONTENT_TRADIOBTN = "Content.TRadiobutton"
    
    # TEntry Style Names
    CUSTOM_TENTRY = 'Popup.Custom.TEntry'
    # CONTENT_TENTRY = 'Popup.Content.TEntry'
    # SIDEBAR_TENTRY = 'Popup.Sidebar.TEntry'
    # Text Style Names
    # CUSTOM_TTEXT = 'Popup.Custom.Text'
    
    # TLabel Style Names
    CUSTOM_TLABEL = 'Popup.Custom.TLabel'
    CONTENT_TLABEL = 'Popup.Content.TLabel'
    SIDEBAR_TLABEL = 'Popup.Sidebar.TLabel'
    
    # TCombobox Style Names Treeview
    CUSTOM_TCOMBOBOX = 'Popup.Custom.TCombobox'
    # CONTENT_TCOMBOBOX = 'Popup.Content.TCombobox'
    # SIDEBAR_TCOMBOBOX = 'Popup.Sidebar.TCombobox'
    
    # Treeview Style Names
    CUSTOM_TREEVIEW = 'Popup.Custom.Treeview'
    # CONTENT_TREEVIEW = 'Popup.Content.Treeview'
    # SIDEBAR_TREEVIEW = 'Popup.Sidebar.Treeview'


class CryptoStyle:
    
    def __init__(self, root, variant="small", style_type="regular", color_style="yellow", theme='flatly'):
        self.variant_options = ['small', 'medium', 'large']
        self.type_options = ['regular', 'outline']
        self.color_options = [
            "obsidian-depths", "charcoal-dreams", "deep-sea-abyss", 
            "forest-dusk", "sable-night", "dark-forest",
            "yellow", "teal", "dark", "dark-blue", "dark-purple"
        ]
        self.root = root
        if variant in self.variant_options:
            self.variant = variant
        else:
            self.variant = 'medium'
        if style_type in self.type_options:
            self.type = style_type
        else:
            self.type = 'regular'
        if color_style in self.color_options:
            self.color = color_style
        else:
            self.color = 'yellow'
        self.style = ttk.Style()
        self.style.theme_use(theme)
        self.odd_color, self.even_color = '', ''
        self.ext_styles = {} # Hold extrnal style defenition used for future style update
        
        self.apply_style()
        # print("style apply to app")
        # root.event_generate("<<StyleUpdated>>", when="tail")
        # print("generat event.")
    
    def add_style(self, name, **options):
        self.ext_styles[name] = options
        self._update_ext_style(name, **options)
    
    def _update_ext_style(self, name, **options):
        d = {}
        for key in options:
            try:
                value = getattr(self, options[key])
                d[key] = value
            except:
                value = options[key]
                d[key] = value
        self.style.configure(name, **d)
    
    def _update_ext_styles(self):
        for name in self.ext_styles:
            options = self.ext_styles[name]
            self._update_ext_style(name, **options)

    def apply_style(self):
        
        self.font = ("Arial", 9 if self.variant == "small" else 11 if self.variant=='medium' else 13)
        self.root.option_add("*TCombobox*Listbox.font", self.font)

        # Common colors
        self.TEXT_FG = "#3E2723" if self.color == "yellow" else "#333333" if self.color == "teal" else "#FFFFFF"
        self.ENTRY_BG_FOCUS = "A1D6E2"
        self.SUCCESS = "#28A745"
        self.INFO = "#17A2B8"
        self.WARNING = "#FFC107"
        self.DANGER = "#DC3545"

        # Dark style colors
        if self.color == "dark":
            self.PRIMARY_BG = "#121212"
            self.SIDEBAR_BG = "#121212"
            self.CONTENT_BG = "#121212"
            self.BUTTON_BG = "#03DAC6"     # Teal
            self.BUTTON_ACTIVE = "#BB86FC" # Purple
            self.REGULAR_BG = "#BB86FC"    # Purple
            self.REGULAR_ACTIVE = "#03DAC6"# Teal
            self.ACCENT = "#BB86FC"        # Purple
            self.OTHER_BUTTON = "#03DAC6"  # Teal
            self.OTHER_ACTIVE = "#BB86FC"  # Purple
            self.TREE_HEADING = "#BB86FC"
            self.TREE_HOVER = "#03DAC6"
            self.EVEN_ROW = "#1E1E1E"
            self.ODD_ROW = "#161616"
            self.TREE_SELECTED = "#03DAC6"
            self.COMBO_BG = "#1A1A1A"
            self.ENTRY_BG = "#1F1F1F"
            self.Entry_FG = self.TEXT_FG
            self.ENTRY_BG_FOCUS = "#BB86FC"
        elif self.color == "dark-purple":  # New purple-focused dark
            self.PRIMARY_BG = "#1A1423"    # Darker purple-gray
            self.SIDEBAR_BG = "#2E1A47"    # Deep purple
            self.CONTENT_BG = "#1A1423"
            self.BUTTON_BG = "#BB86FC"     # Light purple
            self.BUTTON_ACTIVE = "#8E24AA" # Dark purple
            self.REGULAR_BG = "#8E24AA"
            self.REGULAR_ACTIVE = "#BB86FC"
            self.ACCENT = "#BB86FC"
            self.OTHER_BUTTON = "#D81B60"  # Magenta self.ACCENT
            self.OTHER_ACTIVE = "#AD1457"  # Darker magenta
            self.TREE_HEADING = "#BB86FC"
            self.TREE_HOVER = "#D81B60"
            self.EVEN_ROW = "#2E1A47"
            self.ODD_ROW = "#1A1423"
            self.TREE_SELECTED = "#D81B60"
            self.COMBO_BG = "#2E1A47"
            self.ENTRY_BG = "#372554"
            self.Entry_FG = self.TEXT_FG
            self.ENTRY_BG_FOCUS = "#8E24AA"
        elif self.color == "dark-blue":  # New blue-focused dark
            self.PRIMARY_BG = "#0D1B2A"    # Dark navy
            self.SIDEBAR_BG = "#1B263B"    # Deeper navy
            self.CONTENT_BG = "#0D1B2A"
            self.BUTTON_BG = "#40C4FF"     # Light blue
            self.BUTTON_ACTIVE = "#0288D1" # Dark blue
            self.REGULAR_BG = "#0288D1"
            self.REGULAR_ACTIVE = "#40C4FF"
            self.ACCENT = "#40C4FF"
            self.OTHER_BUTTON = "#FFB300"  # Yellow self.ACCENT
            self.OTHER_ACTIVE = "#E69500"  # Darker yellow
            self.TREE_HEADING = "#40C4FF"
            self.TREE_HOVER = "#FFB300"
            self.EVEN_ROW = "#1B263B"
            self.ODD_ROW = "#0D1B2A"
            self.TREE_SELECTED = "#FFB300"
            self.COMBO_BG = "#1B263B"
            self.ENTRY_BG = "#263858"
            self.Entry_FG = self.TEXT_FG
            self.ENTRY_BG_FOCUS = "#FFB300"
        elif self.color == "dark-forest":
            self.PRIMARY_BG = "#1B3A57"
            self.SIDEBAR_BG = "#2C3E50"
            self.CONTENT_BG = "#1B3A57"
            self.BUTTON_BG = "#A4C8E1"     # Soft blue
            self.BUTTON_ACTIVE = "#4A6E8D" # Mid blue
            self.REGULAR_BG = "#4A6E8D"
            self.REGULAR_ACTIVE = "#A4C8E1"
            self.ACCENT = "#A4C8E1"
            self.OTHER_BUTTON = "#FFC107"  # Neutral self.ACCENT
            self.OTHER_ACTIVE = "#4A6E8D"
            self.TREE_HEADING = "#A4C8E1"
            self.TREE_HOVER = "#F0F0F0"
            self.EVEN_ROW = "#2C3E50"
            self.ODD_ROW = "#1B3A57"
            self.TREE_SELECTED = "#4A6E8D"
            self.COMBO_BG = "#2C3E50"
            self.ENTRY_BG = "#A4C8E1"    #"#4A6E8D"
            self.Entry_FG = "#212121"
        elif self.color == "sable-night":
            self.PRIMARY_BG = "#1C1C1C"
            self.SIDEBAR_BG = "#3D3D3D"
            self.CONTENT_BG = "#1C1C1C"
            self.BUTTON_BG = "#A0A0A0"     # Light gray
            self.BUTTON_ACTIVE = "#5E5E5E" # Mid gray
            self.REGULAR_BG = "#5E5E5E"
            self.REGULAR_ACTIVE = "#A0A0A0"
            self.ACCENT = "#A0A0A0"
            self.OTHER_BUTTON = "#7F7F7F"  # Mid-tone gray
            self.OTHER_ACTIVE = "#3D3D3D"
            self.TREE_HEADING = "#A0A0A0"
            self.TREE_HOVER = "#7F7F7F"
            self.EVEN_ROW = "#3D3D3D"
            self.ODD_ROW = "#1C1C1C"
            self.TREE_SELECTED = "#7F7F7F"
            self.COMBO_BG = "#3D3D3D"
            self.ENTRY_BG = "#C9C9C9"
            self.Entry_FG = "#212121"
        elif self.color == "forest-dusk":
            self.PRIMARY_BG = "#2E3A24"
            self.SIDEBAR_BG = "#4A5E3D"
            self.CONTENT_BG = "#2E3A24"
            self.BUTTON_BG = "#A9DFBF"     # Soft green
            self.BUTTON_ACTIVE = "#6B8E23" # Olive green
            self.REGULAR_BG = "#6B8E23"
            self.REGULAR_ACTIVE = "#A9DFBF"
            self.ACCENT = "#A9DFBF"
            self.OTHER_BUTTON = "#D81B60"  # Neutral self.ACCENT
            self.OTHER_ACTIVE = "#6B8E23"
            self.TREE_HEADING = "#A9DFBF"
            self.TREE_HOVER = "#6B8E23"
            self.EVEN_ROW = "#4A5E3D"
            self.ODD_ROW = "#2E3A24"
            self.TREE_SELECTED = "#6B8E23"
            self.COMBO_BG = "#4A5E3D"
            self.ENTRY_BG = "#A9DFBF"
            self.Entry_FG = "#212121"
        elif self.color == "deep-sea-abyss":
            self.PRIMARY_BG = "#001F3F"
            self.SIDEBAR_BG = "#003366"
            self.CONTENT_BG = "#001F3F"
            self.BUTTON_BG = "#AEEEEE"     # Light aqua
            self.BUTTON_ACTIVE = "#007BFF" # Bright blue
            self.REGULAR_BG = "#007BFF"
            self.REGULAR_ACTIVE = "#AEEEEE"
            self.ACCENT = "#AEEEEE"
            self.OTHER_BUTTON = "#005B96"  # Mid blue
            self.OTHER_ACTIVE = "#003366"
            self.TREE_HEADING = "#AEEEEE"
            self.TREE_HOVER = "#007BFF"
            self.EVEN_ROW = "#003366"
            self.ODD_ROW = "#001F3F"
            self.TREE_SELECTED = "#005B96"
            self.COMBO_BG = "#003366"
            self.ENTRY_BG = "#003366"
            self.Entry_FG = self.TEXT_FG
            self.ENTRY_BG_FOCUS = "#007BFF"
        elif self.color == "charcoal-dreams":
            self.PRIMARY_BG = "#3B3B3B"
            self.SIDEBAR_BG = "#4A4A4A"
            self.CONTENT_BG = "#3B3B3B"
            self.BUTTON_BG = "#B2B2B2"     # Light silver
            self.BUTTON_ACTIVE = "#757575" # Mid gray
            self.REGULAR_BG = "#757575"
            self.REGULAR_ACTIVE = "#B2B2B2"
            self.ACCENT = "#B2B2B2"
            self.OTHER_BUTTON = "#616161"  # Darker gray
            self.OTHER_ACTIVE = "#4A4A4A"
            self.TREE_HEADING = "#B2B2B2"
            self.TREE_HOVER = "#616161"
            self.EVEN_ROW = "#4A4A4A"
            self.ODD_ROW = "#3B3B3B"
            self.TREE_SELECTED = "#D81B60"
            self.COMBO_BG = "#4A4A4A"
            self.ENTRY_BG = "#B2B2B2"
            self.Entry_FG = "#212121"
        elif self.color == "obsidian-depths":
            self.PRIMARY_BG = "#2C3E50"
            self.SIDEBAR_BG = "#34495E"
            self.CONTENT_BG = "#2C3E50"
            self.BUTTON_BG = "#1ABC9C"     # Teal
            self.BUTTON_ACTIVE = "#16A085" # Darker teal
            self.REGULAR_BG = "#16A085"
            self.REGULAR_ACTIVE = "#1ABC9C"
            self.ACCENT = "#1ABC9C"
            self.OTHER_BUTTON = "#8E24AA"  # Light neutral
            self.OTHER_ACTIVE = "#1ABC9C"
            self.TREE_HEADING = "#1ABC9C"
            self.TREE_HOVER = "#ECF0F1"
            self.EVEN_ROW = "#34495E"
            self.ODD_ROW = "#2C3E50"
            self.TREE_SELECTED = "#8E24AA"
            self.COMBO_BG = "#34495E"
            self.ENTRY_BG = "#34495E"
            self.Entry_FG = self.TEXT_FG
            self.ENTRY_BG_FOCUS = "#1ABC9C"
        elif self.color == "yellow":
            self.PRIMARY_BG = "#FFF8E1"
            self.SIDEBAR_BG = "#FFECB3"
            self.CONTENT_BG = "#FFF8E1" #FFE082
            self.BUTTON_BG = "#FFE082"
            self.BUTTON_ACTIVE = "#FFB300"
            self.REGULAR_BG = "#FFB300"
            self.REGULAR_ACTIVE = "#E69500"
            self.ACCENT = "#FFC107"
            self.OTHER_BUTTON = "#1995AD"
            self.OTHER_ACTIVE = "#15788C"
            self.TREE_HEADING = "#FFC107"
            self.TREE_HOVER = "#FFFF00"
            self.EVEN_ROW = "#FFFFCC"
            self.ODD_ROW = "#F8F1E9"
            self.TREE_SELECTED = "#FFCA28"
            self.COMBO_BG = "#FFFFE0"
            self.ENTRY_BG = "#FFFFF0"
            self.Entry_FG = self.TEXT_FG
        else:  # color_style == "teal"
            self.PRIMARY_BG = "#F1F1F2"
            self.SIDEBAR_BG = "#D3D3D4"
            self.CONTENT_BG = "#F1F1F2"
            self.BUTTON_BG = "#A1D6E2"
            self.BUTTON_ACTIVE = "#1995AD"
            self.REGULAR_BG = "#1995AD"
            self.REGULAR_ACTIVE = "#A1D6E2"
            self.ACCENT = "#1995AD"
            self.OTHER_BUTTON = "#FFC107"
            self.OTHER_ACTIVE = "#21B5D3"
            self.TREE_HEADING = "#1995AD"
            self.TREE_HOVER = "#21B5D3"
            self.EVEN_ROW = "#BCE2EB"
            self.ODD_ROW = "#E8E8E9"
            self.TREE_SELECTED = "#1B263B"
            self.COMBO_BG = "#E8F4F8"
            self.ENTRY_BG = "#F5FAFC"
            self.Entry_FG = self.TEXT_FG
            self.ENTRY_BG_FOCUS = "#21B5D3"

        self.root.configure(bg=self.CONTENT_BG)
        MAIN.CONTENT_BG = self.CONTENT_BG

        # Style button for main window
        self.style.configure(MAIN.TEXT_TBUTTON, 
                        background=self.CONTENT_BG, 
                        foreground=self.TEXT_FG, 
                        padding=(8, 6) if self.variant == "small" else (12, 10),
                        font=self.font,
                        borderwidth=0)
        self.style.map(MAIN.TEXT_TBUTTON,
                background=[("active", self.CONTENT_BG)])
        self.style.configure(MAIN.OUTLINE_TBUTTON, 
                        background=self.BUTTON_BG, 
                        foreground=self.TEXT_FG, 
                        padding=(8, 6) if self.variant == "small" else (12, 10),
                        font=self.font,
                        borderwidth=0)
        self.style.map(MAIN.OUTLINE_TBUTTON,
                background=[("active", self.BUTTON_ACTIVE)])
        # Main window styles (no borders)
        if self.type == "outline":
            # Style frames for main and popup windows:
            
            self.style.configure(MAIN.CUSTOM_TFRAME, background=self.PRIMARY_BG, borderwidth=0)
            self.style.configure(MAIN.SIDEBAR_TFRAME, background=self.SIDEBAR_BG, borderwidth=0)
            self.style.configure(MAIN.CONTENT_TFRAME, background=self.CONTENT_BG, borderwidth=0)
            self.style.configure(MAIN.CUSTOMEIMG_TFRAME, background=self.ENTRY_BG, borderwidth=1, relief=SOLID, bordercolor=self.REGULAR_BG)
            # Popup (Settings) styles (with borders)
            self.style.configure(POPUP.CUSTOM_TFRAME, 
                            background=self.PRIMARY_BG, 
                            borderwidth=2, 
                            relief=SOLID, 
                            bordercolor=self.ACCENT)
            self.style.configure(POPUP.SIDEBAR_TFRAME, 
                            background=self.SIDEBAR_BG, 
                            borderwidth=0, 
                            relief=SOLID, 
                            bordercolor=self.ACCENT)
            self.style.configure(POPUP.CONTENT_TFRAME, 
                            background=self.CONTENT_BG, 
                            borderwidth=0, 
                            relief=SOLID, 
                            bordercolor=self.ACCENT)
            # Style button for main window
            self.style.configure(MAIN.CUSTOM_TBUTTON, 
                            background=self.BUTTON_BG, 
                            foreground=self.TEXT_FG, 
                            padding=(8, 6) if self.variant == "small" else (12, 10),
                            font=self.font,
                            borderwidth=0)
            self.style.map(MAIN.CUSTOM_TBUTTON,
                    background=[("active", self.BUTTON_ACTIVE)])
            # Style button for main window sidebar
            self.style.configure(MAIN.SIDEBAR_TBUTTON, 
                            background=self.BUTTON_BG, 
                            foreground=self.TEXT_FG, 
                            padding=(8, 6) if self.variant == "small" else (12, 10),
                            anchor='w',
                            font=self.font,
                            borderwidth=0)
            self.style.map(MAIN.SIDEBAR_TBUTTON,
                    background=[("active", self.BUTTON_ACTIVE)])
            
        else:  # regular
            self.style.configure(MAIN.CUSTOM_TFRAME, background=self.PRIMARY_BG, borderwidth=0)
            self.style.configure(MAIN.SIDEBAR_TFRAME, background=self.SIDEBAR_BG, borderwidth=0)
            self.style.configure(MAIN.CONTENT_TFRAME, background=self.CONTENT_BG, borderwidth=0)
            self.style.configure(MAIN.CUSTOMEIMG_TFRAME, background=self.ENTRY_BG, borderwidth=1, relief=SOLID, bordercolor=self.REGULAR_BG)
            # Popup (Settings) styles (with borders)
            self.style.configure(POPUP.CUSTOM_TFRAME, 
                            background=self.PRIMARY_BG, 
                            borderwidth=2, 
                            relief=SOLID, 
                            bordercolor=self.REGULAR_BG)
            self.style.configure(POPUP.SIDEBAR_TFRAME, 
                            background=self.SIDEBAR_BG, 
                            borderwidth=0, 
                            relief='' if self.variant=="small" else SOLID, 
                            bordercolor=self.REGULAR_BG)
            self.style.configure(POPUP.CONTENT_TFRAME, 
                            background=self.CONTENT_BG, 
                            borderwidth=0, 
                            relief='' if self.variant=="small" else SOLID, 
                            bordercolor=self.REGULAR_BG)
            # Style button for main window
            self.style.configure(MAIN.CUSTOM_TBUTTON, 
                            background=self.REGULAR_BG, 
                            foreground=self.TEXT_FG, 
                            padding=(8, 6) if self.variant == "small" else (12, 10),
                            font=self.font,
                            borderwidth=0)
            self.style.map(MAIN.CUSTOM_TBUTTON, 
                    background=[("active", self.REGULAR_ACTIVE)])
            # Style button for main window sidebar
            self.style.configure(MAIN.SIDEBAR_TBUTTON, 
                            background=self.REGULAR_BG, 
                            foreground=self.TEXT_FG, 
                            padding=(8, 6) if self.variant == "small" else (12, 10),
                            anchor='w',
                            font=self.font,
                            borderwidth=0)
            self.style.map(MAIN.SIDEBAR_TBUTTON, 
                    background=[("active", self.REGULAR_ACTIVE)])
        
        # Settings Sidebar Buttons
        self.style.configure(POPUP.SIDEBAR_TBUTTON,
                        background=self.SIDEBAR_BG,  # Matches frame for "no background" effect
                        foreground=self.ACCENT,
                        font=("Arial", 10 if self.variant == "small" else 12 if self.variant=='medium' else 14),
                        anchor='w',
                        # padding=(8, 6) if self.variant == "small" else (12, 10),
                        borderwidth=0,          # No border
                        relief=FLAT)
        self.style.map(POPUP.SIDEBAR_TBUTTON,
                background=[("active", self.CONTENT_BG),      # Hover: bright color
                            ("selected", self.ACCENT)])    # Selected: bright color
        
        self.style.configure(POPUP.CUSTOM_TBUTTON,
                        background=self.SIDEBAR_BG,  # Matches frame for "no background" effect
                        foreground=self.ACCENT,
                        font=("Arial", 14 if self.variant == "small" else 16 if self.variant=='medium' else 18),
                        anchor='center',
                        # padding=(8, 6) if self.variant == "small" else (12, 10),
                        borderwidth=0,          # No border
                        relief=FLAT)
        self.style.map(POPUP.CUSTOM_TBUTTON,
                background=[("active", self.CONTENT_BG),      # Hover: bright color
                            ("selected", self.ACCENT)])    # Selected: bright color

        # Other Button styles
        self.style.configure(MAIN.CONTENT_TBUTTON, 
                        background=self.OTHER_BUTTON, 
                        foreground="#FFFFFF", 
                        padding=(8, 6) if self.variant == "small" else (12, 10), 
                        font=("Arial", 9 if self.variant == "small" else 11 if self.variant=="medium" else 14),
                        borderwidth=0)
        self.style.map(MAIN.CONTENT_TBUTTON, 
                background=[("active", self.OTHER_ACTIVE)])

        self.style.configure(POPUP.CUSTOM_TRADIOBTN,
            background=self.REGULAR_BG,
            foreground=self.TEXT_FG
        )
        self.style.configure(POPUP.CONTENT_TRADIOBTN,
            background=self.CONTENT_BG,
            foreground=self.TEXT_FG
        )

        # Label styles
        self.style.configure(MAIN.CUSTOM_TLABEL, 
                        background=self.PRIMARY_BG, 
                        foreground=self.TEXT_FG, 
                        font=self.font)
        self.style.configure(MAIN.CONTENT_TLABEL, 
                        background=self.CONTENT_BG, 
                        foreground=self.TEXT_FG, 
                        font=self.font)
        self.style.configure(MAIN.SIDEBAR_TLABEL, 
                        background=self.SIDEBAR_BG, 
                        foreground=self.TREE_SELECTED,
                        font=("Segoe UI Emoji", 12 if self.variant == "small" else 14 if self.variant=="medium" else 16, "bold")
                        )
        self.style.configure(POPUP.CUSTOM_TLABEL, 
                        background=self.PRIMARY_BG, 
                        foreground=self.TEXT_FG,
                        # padding=(4, 2) if self.variant == "small" else (6, 3),
                        anchor='center',
                        justify="center", # Align text lines in center
                        wraplength=0,     # Allow wrapping without forced left-align
                        font=("Arial", 8 if self.variant == "small" else 9 if self.variant=="medium" else 10),
                        borderwidth=0,
                        relief="flat")
        self.style.configure(POPUP.CONTENT_TLABEL, 
                        background=self.CONTENT_BG, 
                        foreground=self.TEXT_FG, 
                        font=("Arial", 8 if self.variant == "small" else 9 if self.variant=="medium" else 10))
        self.style.configure(POPUP.SIDEBAR_TLABEL, 
                        background=self.SIDEBAR_BG, 
                        foreground=self.TEXT_FG, 
                        font=("Arial", 8 if self.variant == "small" else 9 if self.variant=="medium" else 10))


        # Treeview styles
        self.style.configure(MAIN.CUSTOM_TREEVIEW, 
                        background=self.CONTENT_BG, 
                        foreground=self.TEXT_FG, 
                        fieldbackground=self.ODD_ROW,
                        font=self.font,
                        borderwidth=0)
        self.style.configure("Main.Custom.Treeview.Heading", 
                        background=self.TREE_HEADING, 
                        foreground=self.TEXT_FG, 
                        font=("Segoe UI Emoji", 12 if self.variant == "small" else 14 if self.variant=="medium" else 16), 
                        borderwidth=0, 
                        relief=FLAT, 
                        anchor="w")
        self.style.map("Main.Custom.Treeview.Heading", 
                background=[("active", self.TREE_HOVER)])
        self.style.configure(POPUP.CUSTOM_TREEVIEW,
                        background=self.CONTENT_BG, 
                        foreground=self.TEXT_FG, 
                        fieldbackground=self.ODD_ROW,
                        font=self.font,
                        borderwidth=1 if self.variant == "small" else 2, 
                        relief=SOLID, 
                        bordercolor=self.ACCENT)
        self.style.configure("Settings.Custom.Treeview.Heading", 
                        background=self.TREE_HEADING, 
                        foreground=self.TEXT_FG, 
                        font=("Segoe UI Emoji", 11 if self.variant == "small" else 12 if self.variant=="medium" else 14),
                        borderwidth=0, 
                        relief=FLAT, 
                        anchor="w")
        self.style.map("Settings.Custom.Treeview.Heading", 
                background=[("active", self.TREE_HOVER)])
        self.style.map(MAIN.CUSTOM_TREEVIEW, background=[("selected", self.TREE_SELECTED)])
        self.style.map(POPUP.CUSTOM_TREEVIEW, background=[("selected", self.TREE_SELECTED)])
        self.style.configure("Treeview", rowheight=20 if self.variant == "small" else 25 if self.variant=="medium" else 30)
        self.style.layout(MAIN.CUSTOM_TREEVIEW, [("Custom.Treeview.treearea", {"sticky": "nswe"})])
        self.style.layout(POPUP.CUSTOM_TREEVIEW, [("Custom.Treeview.treearea", {"sticky": "nswe"})])

        # Combobox styles
        self.style.configure(MAIN.CUSTOM_TCOMBOBOX, 
                        fieldbackground=self.COMBO_BG, 
                        foreground=self.TEXT_FG, 
                        background=self.COMBO_BG, 
                        font=self.font,
                        borderwidth=1,
                        relief=SOLID,
                        bordercolor=self.ACCENT)
        self.style.map(MAIN.CUSTOM_TCOMBOBOX, 
                fieldbackground=[("focus", self.ACCENT if self.color == "yellow" else "#A1D6E2")],
                background=[("focus", self.ACCENT if self.color == "yellow" else "#A1D6E2")])
        self.style.configure(POPUP.CUSTOM_TCOMBOBOX, 
                        fieldbackground=self.COMBO_BG, 
                        foreground=self.TEXT_FG, 
                        background=self.COMBO_BG, 
                        font=self.font,
                        borderwidth=1,
                        relief=SOLID,
                        bordercolor=self.ACCENT)
        self.style.map(POPUP.CUSTOM_TCOMBOBOX, 
                fieldbackground=[("focus", self.ACCENT if self.color == "yellow" else "#A1D6E2")],
                background=[("focus", self.ACCENT if self.color == "yellow" else "A1D6E2")])
        
        # Combobox dropdown styles
        self.style.configure("Main.Custom.TCombobox.Popdown",
                        font=self.font,
                        background=self.COMBO_BG,
                        foreground=self.TEXT_FG)
        self.style.configure("Settings.Custom.TCombobox.Popdown",
                        font=self.font,
                        background=self.COMBO_BG,
                        foreground=self.TEXT_FG)

        # Entry styles
        self.style.configure(
            MAIN.CONTENT_TENTRY,
            fieldbackground=self.ENTRY_BG,
            background=self.ENTRY_BG,
            foreground=self.Entry_FG,
            font=self.font,
            borderwidth=0,  # Borderless to blend with frame
            relief="flat",
            padding=(2, 2), #if variant == "small" else (6, 3),
            bordercolor=self.ENTRY_BG,
            lightcolor=self.ENTRY_BG,
            darkcolor=self.ENTRY_BG,
            highlightthickness=0
        )
        self.style.map(
            MAIN.CONTENT_TENTRY,
            fieldbackground=[("active", self.ENTRY_BG),("focus", self.ENTRY_BG)],
            background=[("active", self.ENTRY_BG),("focus",  self.ENTRY_BG)],
            bordercolor=[("active", self.ENTRY_BG),("focus", self.ENTRY_BG)],
            lightcolor=[("active", self.ENTRY_BG), ("focus", self.ENTRY_BG)],
            darkcolor=[("active", self.ENTRY_BG), ("focus", self.ENTRY_BG)]
        )
        self.style.configure(MAIN.CUSTOM_TENTRY, 
                        fieldbackground=self.ENTRY_BG, 
                        foreground=self.Entry_FG, 
                        font= self.font,
                        borderwidth=1,
                        relief=SOLID,
                        bordercolor=self.ACCENT)
        self.style.map(MAIN.CUSTOM_TENTRY, 
                fieldbackground=[("focus", self.ACCENT if self.color == "yellow" else self.ENTRY_BG_FOCUS)],
                bordercolor=[("focus", self.BUTTON_ACTIVE if self.color == "yellow" else "#15788C")])
        self.style.configure(POPUP.CUSTOM_TENTRY, 
                        fieldbackground=self.ENTRY_BG, 
                        foreground=self.Entry_FG, 
                        font=self.font,
                        borderwidth=1,
                        relief=SOLID,
                        bordercolor=self.ACCENT)
        self.style.map(POPUP.CUSTOM_TENTRY, 
                fieldbackground=[("focus", self.ACCENT if self.color == "yellow" else self.ENTRY_BG_FOCUS)],
                bordercolor=[("focus", self.BUTTON_ACTIVE if self.color == "yellow" else "#15788C")])
        
        self.style.configure(MAIN.CUSTOMIMG_TLABEL, 
                        background=self.ENTRY_BG)

        # Notification label styles
        self.style.configure(SUCCESS_TL, 
                        background=self.SUCCESS, 
                        foreground="#FFFFFF", 
                        font=self.font)
        self.style.configure(INFO_TL, 
                        background=self.INFO, 
                        foreground="#FFFFFF", 
                        font=self.font)
        self.style.configure(WARNING_TL, 
                        background=self.WARNING, 
                        foreground="#FFFFFF", 
                        font=self.font)
        self.style.configure(DANGER_TL, 
                        background=self.DANGER, 
                        foreground="#FFFFFF", 
                        font=self.font)

        # Return style config and row colors
        self.odd_color = self.ODD_ROW
        self.even_color = self.EVEN_ROW
    
    
    def update_style(self, variant=None, style_type=None, color_style=None):
        """Update style attributes and reapply"""
        if variant is not None:
            self.variant = variant
        if style_type is not None:
            self.type = style_type
        if color_style is not None:
            self.color = color_style
        
        self.apply_style()
        self._update_ext_styles()
        # update Treeview odd/even row color and update font for Entry and Combobox
        if variant:
            self.update_Entry_Combo(self.root)
        if color_style:
            self.update_tree_color(self.root)
        self.root.event_generate("<<StyleUpdated>>", when="tail")
        self.root.update_idletasks()
    
    def update_tree_color(self, root):
        for w in root.winfo_children():
            if isinstance(w, ttk.Treeview):
                w.tag_configure("even", background=self.even_color)
                w.tag_configure("odd", background=self.odd_color)
            else:
                self.update_tree_color(w)
        
    def update_Entry_Combo(self, root):
        for w in root.winfo_children():
            if isinstance(w, (ttk.Combobox, ttk.Entry)):
                w.configure(font=self.font)
            else:
                self.update_Entry_Combo(w)
       



