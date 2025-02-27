import tkinter as tk
from tkinter import ttk

def create_title_bar(app):
    """Erstellt die Titelleiste"""
    app.title_bar = ttk.Frame(app.root, style='Dark.TFrame')
    app.title_bar.pack(fill=tk.X, pady=2)
    
    # Menü-Button (≡)
    menu_btn = ttk.Label(app.title_bar,
                        text="≡",
                        style='Menu.TLabel',
                        cursor="hand2")
    menu_btn.pack(side=tk.LEFT, padx=10)
    menu_btn.bind('<Button-1>', app.show_main_menu)
    
    # Titel
    title = ttk.Label(app.title_bar, 
                     text="MY TODO",
                     style='Title.TLabel')  # Cursor für Drag & Drop
    title.pack(side=tk.LEFT, padx=10)
    
    # Schließen-Button
    close_btn = ttk.Label(app.title_bar,
                         text="×",
                         style='Close.TLabel',
                         cursor="hand2")
    close_btn.pack(side=tk.RIGHT, padx=5)
    close_btn.bind('<Button-1>', lambda e: app.close_app()) 