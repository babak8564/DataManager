from BackEnd.core import App, AppState
import ttkbootstrap as tk
from FrontEnd.view import ViewFrame, SetAccountFrame, LoginFrame, ManagerFrame, DatabaseErrorFrame
from FrontEnd.styles import CryptoStyle, MAIN

VIEWS = {
    AppState.MAIN:ManagerFrame,
    AppState.LOGIN:LoginFrame,
    AppState.SET_ACCOUNT:SetAccountFrame,
    AppState.INACTIVE:LoginFrame,
    AppState.DATABASE_ERROR:DatabaseErrorFrame
}

root = tk.Window()
app = App(root, __file__)

root.title("Password Manager")
root.geometry("900x500+50+50")
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.iconbitmap(app.settings.new_settings['icons']['app_ico'])

app.style = CryptoStyle(root, app.style_variant, app.style_type, app.style_color)

app.main_notif = tk.Label(root, text='', justify='center', anchor='center', style=MAIN.CONTENT_TLABEL)
app.main_notif.pack(padx=1, pady=(1,7), fill='x')

app.container = tk.Frame(root)
app.container.pack(fill='both', expand=1)

def clear_window():
    for widget in app.container.winfo_children():
        widget.destroy()

def show_view(view_class):
    clear_window()
    view:ViewFrame = view_class(app)
    view.show()
    return view

def handle_app_state(state:AppState):
    """Check app state and transition to MainView if needed."""
    
    return show_view(VIEWS[state])

app.set_state_callback(handle_app_state)

try:
    is_valid, msgs = app.is_database_valid()
    if is_valid:
        app.initial_state()
    else:
        app.db_error = msgs
        app.set_state(AppState.DATABASE_ERROR)
except RuntimeError as e:
    app.db_error = ["RuntimeError", str(e)]
    app.set_state(AppState.DATABASE_ERROR)

root.mainloop()


