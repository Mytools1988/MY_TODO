import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import threading
import time
import json
from datetime import datetime, timedelta
import os
import tkinter.filedialog
import shutil
import csv
import ctypes
from ctypes import wintypes

# Globale Konstanten
COLORS = {
    'dark': {
        'bg': '#202020',
        'bg_secondary': '#2d2d2d',
        'bg_tertiary': '#383838',
        'bg_input': '#303030',
        'bg_hover': '#383838',
        'bg_active': '#404040',
        'fg': '#ffffff',
        'fg_secondary': '#b0b0b0',
        'fg_tertiary': '#808080',
        'fg_input': '#ffffff',
        'accent': '#007acc',
        'error': '#ff4444',
        'error_hover': '#ff6666'
    },
    'light': {
        'bg': '#ffffff',
        'bg_secondary': '#f5f5f5',
        'bg_tertiary': '#eeeeee',
        'bg_input': '#ffffff',
        'bg_hover': '#f0f0f0',
        'bg_active': '#e8e8e8',
        'fg': '#000000',
        'fg_secondary': '#666666',
        'fg_tertiary': '#999999',
        'fg_input': '#000000',
        'accent': '#007acc',
        'error': '#cc0000',
        'error_hover': '#ff0000'
    }
}

class AlwaysOnTopTodo:
    def __init__(self, root):
        self.root = root
        self.root.title("Always On Top To-Do List")
        self.root.geometry("300x400+10+10")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', 1)
        self.root.attributes('-alpha', 0.85)
        
        # Theme-Einstellungen
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'text_bg': '#ffffff',
                'text_fg': '#000000',
                'title_bg': '#f0f0f0',
                'title_fg': '#000000'
            },
            'dark': {
                'bg': '#2d2d2d',
                'text_bg': '#2d2d2d',
                'text_fg': '#ffffff',
                'title_bg': '#1e1e1e',
                'title_fg': '#ffffff'
            }
        }
        self.current_theme = 'light'
        
        # Titelleiste
        self.title_bar = tk.Frame(self.root, height=30)
        self.title_bar.pack(fill='x')
        
        # Theme Toggle Button
        self.theme_button = tk.Button(self.title_bar, text="🌓", command=self.toggle_theme,
                                    bd=0, padx=5)
        self.theme_button.pack(side='left')
        
        # Minimize und Close Buttons
        self.minimize_button = tk.Button(self.title_bar, text="-", command=self.minimize_window,
                                       bd=0, padx=5)
        self.minimize_button.pack(side='right')
        
        self.close_button = tk.Button(self.title_bar, text="×", command=self.close_app,
                                    bd=0, padx=5)
        self.close_button.pack(side='right')
        
        # Haupttextbereich
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, 
                                                 font=("Arial", 12))
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Fenster verschieben
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.on_move)
        
        # Automatisches Speichern
        self.text_area.bind('<KeyRelease>', self.delayed_save)
        self.save_timer = None
        
        # Todo-Manager initialisieren
        self.todo_manager = TodoManager()
        
        self.load_todo()
        self.start_auto_reload()
        self.apply_theme()
    
    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()
    
    def apply_theme(self):
        theme = self.themes[self.current_theme]
        
        # Titelleiste
        self.title_bar.configure(bg=theme['title_bg'])
        self.theme_button.configure(bg=theme['title_bg'], fg=theme['title_fg'])
        self.minimize_button.configure(bg=theme['title_bg'], fg=theme['title_fg'])
        self.close_button.configure(bg=theme['title_bg'], fg=theme['title_fg'])
        
        # Hauptbereich
        self.root.configure(bg=theme['bg'])
        self.text_area.configure(
            bg=theme['text_bg'],
            fg=theme['text_fg'],
            insertbackground=theme['text_fg'],  # Cursor-Farbe
            selectbackground='#404040' if self.current_theme == 'dark' else '#a6c9e2',  # Auswahlfarbe
            selectforeground=theme['text_fg']
        )
    
    def start_move(self, event):
        """Startet die Fensterbewegung"""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """Bewegt das Fenster"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def minimize_window(self):
        """Minimiert das Fenster"""
        self.root.iconify()
    
    def load_todo(self):
        # Implement the logic to load todos from a file or database
        pass
    
    def start_auto_reload(self):
        # Implement the logic to periodically reload todos
        pass
    
    def delayed_save(self, event):
        # Implement the logic to save todos after a delay
        pass

    def on_close_hover(self, label, enter):
        """Ändert das Aussehen des Schließen-Buttons beim Hover"""
        if enter:
            label.configure(foreground=self.colors['error'])
        else:
            label.configure(foreground=self.colors['fg'])

    def close_app(self):
        """Beendet die Anwendung"""
        if messagebox.askyesno("Beenden", "Möchten Sie die Anwendung wirklich beenden?"):
            self.save_settings()
            self.root.destroy()

class TodoApp:
    """Hauptanwendungsklasse für die Todo-Anwendung"""
    
    def __init__(self):
        # Hauptfenster
        self.root = tk.Tk()
        self.root.title("Actiontext")
        self.root.configure(bg=COLORS['dark']['bg'])
        
        # Fenster-Eigenschaften
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.attributes('-alpha', 0.95)
        
        # Pfade
        self.storage_path = os.path.abspath('todos.txt')
        self.categories_path = os.path.abspath('categories.txt')
        self.settings_path = os.path.abspath('settings.txt')
        
        # Standardwerte
        self.colors = COLORS['dark']
        self.categories = ["Allgemein"]  # Standardkategorie
        
        # Initialisierung
        self.setup_styles()         # 1. Styles
        self.load_categories()      # 2. Kategorien laden
        self.create_gui()           # 3. GUI
        self.todo_manager = TodoManager()  # 4. Daten
        self.load_todos()           # 5. Todos laden
        
        # Fensterposition
        self.center_window()
        
    def start_move(self, event):
        """Startet die Fensterbewegung"""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """Bewegt das Fenster"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def center_window(self):
        """Zentriert das Fenster auf dem Bildschirm"""
        self.root.update_idletasks()
        width = 300
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_title_bar(self):
        """Erstellt die Titelleiste"""
        self.title_bar = ttk.Frame(self.root, style='Dark.TFrame')
        self.title_bar.pack(fill=tk.X, pady=2)
        
        # Menü-Button (≡)
        menu_btn = ttk.Label(self.title_bar,
                            text="≡",
                            style='Menu.TLabel',
                            cursor="hand2")
        menu_btn.pack(side=tk.LEFT, padx=10)
        menu_btn.bind('<Button-1>', self.show_main_menu)
        
        # Titel
        title = ttk.Label(self.title_bar, 
                         text="Meine Aufgaben",
                         style='Title.TLabel')
        title.pack(side=tk.LEFT, padx=10)
        
        # Schließen-Button
        close_btn = ttk.Label(self.title_bar,
                             text="×",
                             style='Close.TLabel',
                             cursor="hand2")
        close_btn.pack(side=tk.RIGHT, padx=10)
        close_btn.bind('<Button-1>', lambda e: self.close_app())

    def create_main_area(self):
        """Erstellt den Hauptbereich mit den Aufgabengruppen"""
        # Hauptcontainer
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbarer Bereich
        self.canvas = tk.Canvas(self.main_frame, 
                              bg=self.colors['bg'],
                              highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, 
                                     orient=tk.VERTICAL,
                                     command=self.canvas.yview)
        
        # Frame für Todos
        self.todo_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), 
                                window=self.todo_frame,
                                anchor="nw",
                                tags="todo_frame")
        
        # Scrollbar Konfiguration
        self.canvas.configure(yscrollcommand=self.update_scrollbar)
        
        # Event Bindings
        self.todo_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Mausrad-Scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_bottom_bar(self):
        """Erstellt die untere Leiste"""
        self.bottom_bar = ttk.Frame(self.root)
        self.bottom_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        # Neue Aufgabe Button (+)
        self.add_button = ttk.Label(self.bottom_bar,
                                  text="+",
                                  style='Add.TLabel',
                                  cursor="hand2")
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.add_button.bind('<Button-1>', lambda e: self.add_todo())
        
        # Kategorie Button (⊞)
        self.category_button = ttk.Label(self.bottom_bar,
                                       text="⊞",
                                       style='Category.TLabel',
                                       cursor="hand2")
        self.category_button.pack(side=tk.LEFT, padx=5)
        self.category_button.bind('<Button-1>', self.show_category_menu)
        
        # Suchfeld
        self.search_frame = ttk.Frame(self.bottom_bar)
        self.search_frame.pack(side=tk.RIGHT, padx=10)
        
        search_icon = ttk.Label(self.search_frame,
                               text="⌕",
                               style='Search.TLabel')
        search_icon.pack(side=tk.RIGHT, padx=(0, 5))
        
        self.search_entry = ttk.Entry(self.search_frame,
                                    width=15,
                                    style='Search.TEntry')
        self.search_entry.pack(side=tk.RIGHT)
        self.search_entry.bind('<KeyRelease>', self.on_search)

    def load_todos(self):
        """Lädt die Todos"""
        self.todo_manager.load()
        self.show_all_todos()

    def setup_styles(self):
        """Konfiguriert die Styles für die Anwendung"""
        style = ttk.Style()
        
        # Frame Styles
        style.configure('Dark.TFrame', background=self.colors['bg'])
        style.configure('Category.TFrame', background=self.colors['bg_secondary'])
        style.configure('Todo.TFrame', 
                       background=self.colors['bg_secondary'],
                       padding=5)
        
        # Label Styles
        style.configure('Title.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=('Arial', 12, 'bold'))
        
        style.configure('TodoText.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['fg'],
                       padding=5)
        
        style.configure('Close.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=('Arial', 14))
        
        style.configure('Add.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=('Arial', 16))
        
        style.configure('Category.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=('Arial', 14))
        
        style.configure('Search.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['fg_secondary'],
                       font=('Arial', 12))
        
        # Entry Style
        style.configure('Search.TEntry',
                       fieldbackground=self.colors['bg_input'],
                       foreground=self.colors['fg_input'],
                       insertcolor=self.colors['fg'])
        
        style.configure('Menu.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=('Arial', 16))  # Größerer Font für das Menü-Symbol

    def create_gui(self):
        """Erstellt die komplette GUI"""
        self.create_title_bar()
        self.create_main_area()
        self.create_bottom_bar()
        self._setup_bindings()

    def _setup_bindings(self):
        """Richtet die Event-Bindings ein"""
        # Fenster verschieben
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.on_move)
        
        # Suche
        self.search_entry.bind('<KeyRelease>', self.on_search)

    def show_all_todos(self):
        """Zeigt alle Todos an"""
        # Bestehende Todos aus der Liste entfernen
        for widget in self.todo_frame.winfo_children():
            widget.destroy()
        
        # Todos nach Kategorien gruppieren
        todos_by_category = {}
        for todo in self.todo_manager.get_all():
            category = todo.get('category', 'Allgemein')
            if category not in todos_by_category:
                todos_by_category[category] = []
            todos_by_category[category].append(todo)
        
        # Alle Kategorien anzeigen
        for category in sorted(todos_by_category.keys()):
            # Kategorie-Header
            category_frame = ttk.Frame(self.todo_frame, style='Category.TFrame')
            category_frame.pack(fill=tk.X, pady=(10,5))
            
            # Kategorie-Label mit Anzahl
            count = len(todos_by_category[category])
            category_label = ttk.Label(category_frame, 
                                    text=f"⊞ {category} ({count})",
                                    style='TodoText.TLabel')
            category_label.pack(anchor="w", padx=5)
            
            # Container für Todos dieser Kategorie
            todos_frame = ttk.Frame(self.todo_frame)
            todos_frame.pack(fill=tk.X)
            todos_frame.category = category
            
            # Todos in dieser Kategorie anzeigen
            for todo in self._sort_by(todos_by_category[category]):
                self._create_todo_item(todos_frame, todo)

    def _sort_by(self, todos, key='priority', reverse=False):
        """Sortiert Todos nach verschiedenen Kriterien"""
        priority_order = {'▲': 0, '►': 1, '▼': 2}
        
        if key == 'priority':
            return sorted(todos, 
                         key=lambda x: priority_order.get(x.get('priority', '►')),
                         reverse=reverse)
        elif key == 'deadline':
            return sorted(todos,
                         key=lambda x: x.get('deadline', ''),
                         reverse=reverse)
        else:
            return sorted(todos,
                         key=lambda x: x.get(key, ''),
                         reverse=reverse)

    def on_search(self, event=None):
        """Sucht in den Todos"""
        query = self.search_entry.get().strip()
        if query:
            results = self.todo_manager.search(query)
            # Ergebnisse anzeigen
            for widget in self.todo_frame.winfo_children():
                widget.destroy()
            for todo in self._sort_by(results):
                self._create_todo_item(self.todo_frame, todo)
        else:
            self.show_all_todos()

    def close_app(self):
        """Beendet die Anwendung"""
        if messagebox.askyesno("Beenden", "Möchten Sie die Anwendung wirklich beenden?"):
            self.save_settings()
            self.root.destroy()

    def add_todo(self):
        """Erstellt ein neues Todo mit Dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Neue Aufgabe")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        
        # Container
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Aufgabentext
        ttk.Label(main_frame, text="Aufgabe:").pack(anchor="w")
        text_entry = ttk.Entry(main_frame, width=40)
        text_entry.pack(fill=tk.X, pady=(0, 10))
        text_entry.focus()
        
        # Kategorie
        ttk.Label(main_frame, text="Kategorie:").pack(anchor="w")
        category_var = tk.StringVar(value="Allgemein")
        category_combo = ttk.Combobox(main_frame, 
                                    textvariable=category_var,
                                    values=self.categories,
                                    state="readonly")
        category_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Priorität
        ttk.Label(main_frame, text="Priorität:").pack(anchor="w")
        priority_var = tk.StringVar(value="►")
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(priority_frame, text="Hoch", value="▲", variable=priority_var).pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Normal", value="►", variable=priority_var).pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Niedrig", value="▼", variable=priority_var).pack(side=tk.LEFT)
        
        # Deadline
        ttk.Label(main_frame, text="Deadline (optional):").pack(anchor="w")
        deadline_entry = ttk.Entry(main_frame)
        deadline_entry.pack(fill=tk.X, pady=(0, 20))
        
        def save_todo():
            text = text_entry.get().strip()
            if text:
                todo = {
                    'text': text,
                    'category': category_var.get(),
                    'priority': priority_var.get(),
                    'deadline': deadline_entry.get().strip()
                }
                self.todo_manager.add(todo)
                self.show_all_todos()
                dialog.destroy()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        save_btn = ttk.Button(button_frame, 
                            text="Speichern",
                            command=save_todo,
                            style='Primary.TButton')
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame,
                              text="Abbrechen",
                              command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Enter-Taste zum Speichern
        text_entry.bind('<Return>', lambda e: save_todo())

    def _create_todo_item(self, parent_frame, todo):
        """Erstellt ein einzelnes Todo-Item"""
        # Container für das Todo
        todo_frame = ttk.Frame(parent_frame, style='Todo.TFrame')
        todo_frame.pack(fill=tk.X, pady=2)
        
        # Prioritäts-Label
        priority_label = ttk.Label(todo_frame,
                                text=todo.get('priority', '►'),
                                style='TodoText.TLabel',
                                width=2)
        priority_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Checkbox für Completed-Status
        completed_var = tk.BooleanVar(value=todo.get('completed', False))
        checkbox = ttk.Checkbutton(todo_frame,
                                 variable=completed_var,
                                 command=lambda: self._toggle_todo_completed(todo_frame.todo_index))
        checkbox.pack(side=tk.LEFT, padx=5)
        
        # Text-Label
        text_label = ttk.Label(todo_frame,
                             text=todo['text'],
                             style='TodoText.TLabel',
                             wraplength=200)
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Deadline (falls vorhanden)
        if todo.get('deadline'):
            deadline_label = ttk.Label(todo_frame,
                                    text=todo['deadline'],
                                    style='TodoText.TLabel')
            deadline_label.pack(side=tk.RIGHT, padx=5)
            
            # Überprüfe ob überfällig
            if self._is_overdue(todo['deadline']):
                deadline_label.configure(foreground=self.colors['error'])
        
        # Speichere den Index und die Kategorie für Drag & Drop
        todo_frame.todo_index = self.todo_manager.get_all().index(todo)
        todo_frame.category = todo.get('category', 'Allgemein')
        
        # Event-Bindings
        todo_frame.bind('<Button-1>', lambda e: self.start_drag(e, todo_frame))
        todo_frame.bind('<B1-Motion>', self.on_drag)
        todo_frame.bind('<ButtonRelease-1>', self.end_drag)
        
        # Doppelklick zum Bearbeiten
        todo_frame.bind('<Double-Button-1>', lambda e: self.edit_todo(todo_frame.todo_index))
        
        # Rechtsklick-Menü
        todo_frame.bind('<Button-3>', lambda e: self._show_todo_context_menu(e, todo_frame))
        
        return todo_frame

    def _on_frame_configure(self, event=None):
        """Aktualisiert die Scroll-Region wenn sich die Größe des Inhalts ändert"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Passt die Breite des inneren Frames an die Canvas-Breite an"""
        if event.width > 1:  # Vermeide 1px Breite beim Start
            self.canvas.itemconfig("todo_frame", width=event.width)

    def update_scrollbar(self, *args):
        """Aktualisiert die Sichtbarkeit der Scrollbar"""
        if self.todo_frame.winfo_height() > self.canvas.winfo_height():
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.scrollbar.pack_forget()
        self.scrollbar.set(*args)

    def _is_overdue(self, deadline):
        """Prüft, ob eine Deadline überschritten ist"""
        if not deadline:
            return False
        try:
            formats = ["%d.%m.%Y", "%d.%m.%Y %H:%M", "%Y-%m-%d", "%Y-%m-%d %H:%M"]
            for fmt in formats:
                try:
                    deadline_date = datetime.strptime(deadline, fmt)
                    return deadline_date < datetime.now()
                except ValueError:
                    continue
            return False
        except:
            return False

    def _toggle_todo_completed(self, index):
        """Ändert den Completed-Status eines Todos"""
        self.todo_manager.toggle_completed(index)
        self.show_all_todos()

    def _show_todo_context_menu(self, event, todo_frame):
        """Zeigt das Kontextmenü für ein Todo"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Bearbeiten", 
                        command=lambda: self.edit_todo(todo_frame.todo_index))
        menu.add_command(label="Löschen", 
                        command=lambda: self.delete_todo(todo_frame.todo_index))
        menu.post(event.x_root, event.y_root)

    def edit_todo(self, index):
        """Bearbeitet ein bestehendes Todo"""
        todo = self.todo_manager.get_all()[index]
        dialog = tk.Toplevel(self.root)
        dialog.title("Aufgabe bearbeiten")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Aufgabe:").pack(anchor="w")
        text_entry = ttk.Entry(main_frame, width=40)
        text_entry.insert(0, todo['text'])
        text_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(main_frame, text="Kategorie:").pack(anchor="w")
        category_var = tk.StringVar(value=todo.get('category', 'Allgemein'))
        category_combo = ttk.Combobox(main_frame, 
                                    textvariable=category_var,
                                    values=self.categories,
                                    state="readonly")
        category_combo.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(main_frame, text="Priorität:").pack(anchor="w")
        priority_var = tk.StringVar(value=todo.get('priority', '►'))
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(priority_frame, text="Hoch", value="▲", variable=priority_var).pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Normal", value="►", variable=priority_var).pack(side=tk.LEFT)
        ttk.Radiobutton(priority_frame, text="Niedrig", value="▼", variable=priority_var).pack(side=tk.LEFT)
        
        ttk.Label(main_frame, text="Deadline (optional):").pack(anchor="w")
        deadline_entry = ttk.Entry(main_frame)
        deadline_entry.insert(0, todo.get('deadline', ''))
        deadline_entry.pack(fill=tk.X, pady=(0, 20))
        
        def update_todo():
            text = text_entry.get().strip()
            if text:
                updated_todo = {
                    'text': text,
                    'category': category_var.get(),
                    'priority': priority_var.get(),
                    'deadline': deadline_entry.get().strip()
                }
                self.todo_manager.update(index, updated_todo)
                self.show_all_todos()
                dialog.destroy()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        save_btn = ttk.Button(button_frame, 
                            text="Aktualisieren",
                            command=update_todo,
                            style='Primary.TButton')
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame,
                              text="Abbrechen",
                              command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def delete_todo(self, index):
        """Löscht ein Todo"""
        if messagebox.askyesno("Löschen bestätigen", 
                              "Möchten Sie diese Aufgabe wirklich löschen?"):
            self.todo_manager.delete(index)
            self.show_all_todos()

    def save_settings(self):
        """Speichert die aktuellen Einstellungen"""
        try:
            settings = {
                'window_position': f"{self.root.winfo_x()},{self.root.winfo_y()}",
                'window_size': f"{self.root.winfo_width()},{self.root.winfo_height()}"
            }
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                for key, value in settings.items():
                    f.write(f"{key}={value}\n")
        except Exception as e:
            print(f"Fehler beim Speichern der Einstellungen: {e}")

    def show_category_menu(self, event):
        """Zeigt das Kategorie-Menü"""
        menu = tk.Menu(self.root, tearoff=0)
        
        # "Alle anzeigen" Option
        menu.add_command(label="🔍 Alle anzeigen", command=self.show_all_todos)
        menu.add_separator()
        
        # Kategorien anzeigen
        for category in self.categories:
            count = self.count_todos_in_category(category)
            menu.add_command(
                label=f"{category} ({count})",
                command=lambda cat=category: self.filter_by_category(cat)
            )
        
        menu.add_separator()
        menu.add_command(label="+ Neue Kategorie", command=self.add_category)
        menu.add_command(label="- Kategorie entfernen", command=self.remove_category)
        
        # Menü an Button-Position anzeigen
        menu.post(event.widget.winfo_rootx(), 
                 event.widget.winfo_rooty() + event.widget.winfo_height())

    def add_category(self):
        """Fügt eine neue Kategorie hinzu"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Neue Kategorie")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Name der Kategorie:").pack(anchor="w")
        name_entry = ttk.Entry(main_frame, width=40)
        name_entry.pack(fill=tk.X, pady=(0, 20))
        name_entry.focus()
        
        def save_category():
            name = name_entry.get().strip()
            if name:
                if name not in self.categories:
                    self.categories.append(name)
                    self.categories.sort()
                    self.save_categories()
                    self.show_all_todos()
                    dialog.destroy()
                else:
                    messagebox.showwarning("Warnung", "Diese Kategorie existiert bereits.")
            else:
                messagebox.showwarning("Warnung", "Bitte geben Sie einen Kategorienamen ein.")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        save_btn = ttk.Button(button_frame, text="Speichern", command=save_category)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Abbrechen", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def remove_category(self):
        """Entfernt eine Kategorie"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Kategorie entfernen")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Kategorie auswählen:").pack(anchor="w")
        
        category_var = tk.StringVar()
        category_list = ttk.Combobox(main_frame,
                                    textvariable=category_var,
                                    values=[cat for cat in self.categories if cat != "Allgemein"],
                                    state="readonly")
        category_list.pack(fill=tk.X, pady=(0, 20))
        
        def delete_category():
            category = category_var.get()
            if category:
                if messagebox.askyesno("Bestätigen", 
                                    f"Möchten Sie die Kategorie '{category}' wirklich löschen?"):
                    # Todos in dieser Kategorie nach 'Allgemein' verschieben
                    todos = self.todo_manager.get_all()
                    for i, todo in enumerate(todos):
                        if todo.get('category') == category:
                            todo['category'] = 'Allgemein'
                            self.todo_manager.update(i, todo)
                    
                    self.categories.remove(category)
                    self.save_categories()
                    self.show_all_todos()
                    dialog.destroy()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        delete_btn = ttk.Button(button_frame, text="Löschen", command=delete_category)
        delete_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Abbrechen", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def filter_by_category(self, category):
        """Filtert Todos nach Kategorie"""
        todos = self.todo_manager.get_by_category(category)
        
        # GUI aktualisieren
        for widget in self.todo_frame.winfo_children():
            widget.destroy()
        
        for todo in self._sort_by(todos):
            self._create_todo_item(self.todo_frame, todo)

    def count_todos_in_category(self, category):
        """Zählt die Todos in einer Kategorie"""
        return len(self.todo_manager.get_by_category(category))

    def save_categories(self):
        """Speichert die Kategorien in der Datei"""
        try:
            with open(self.categories_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.categories))
        except Exception as e:
            print(f"Fehler beim Speichern der Kategorien: {e}")

    def load_categories(self):
        """Lädt die Kategorien aus der Datei"""
        try:
            with open(self.categories_path, 'r', encoding='utf-8') as f:
                categories = [line.strip() for line in f.readlines() if line.strip()]
                self.categories = categories if categories else ["Allgemein"]
        except FileNotFoundError:
            self.categories = ["Allgemein"]
        
        # Stelle sicher, dass "Allgemein" immer existiert
        if "Allgemein" not in self.categories:
            self.categories.insert(0, "Allgemein")

    def start_drag(self, event, frame):
        """Startet das Drag & Drop einer Aufgabe"""
        if not hasattr(self, 'drag_data'):
            # Erstelle einen temporären Frame für das Drag & Drop
            self.drag_frame = ttk.Frame(self.root, style='TodoDrag.TFrame')
            
            # Kopiere den Inhalt des Original-Frames
            ttk.Label(self.drag_frame, 
                     text=frame.winfo_children()[2].cget("text"),
                     style='TodoText.TLabel').pack(padx=10, pady=5)
            
            # Speichere die Daten
            self.drag_data = {
                'original_frame': frame,
                'index': frame.todo_index,
                'start_x': event.x_root,
                'start_y': event.y_root,
                'original_category': frame.category
            }
            
            # Platziere den temporären Frame
            self.drag_frame.place(x=event.x_root - self.root.winfo_rootx(),
                                y=event.y_root - self.root.winfo_rooty())

    def on_drag(self, event):
        """Bewegt die Aufgabe während des Drags"""
        if hasattr(self, 'drag_data'):
            # Berechne neue Position relativ zum Hauptfenster
            x = event.x_root - self.root.winfo_rootx()
            y = event.y_root - self.root.winfo_rooty()
            self.drag_frame.place(x=x, y=y)
            
            # Finde potenzielle Drop-Zonen
            for frame in self.todo_frame.winfo_children():
                if hasattr(frame, 'category'):
                    bbox = frame.bbox()
                    if bbox:
                        x1, y1, x2, y2 = bbox
                        if (x1 < event.x_root < x2 and 
                            y1 < event.y_root < y2):
                            self.highlight_dropzone(frame, True)
                        else:
                            self.highlight_dropzone(frame, False)

    def end_drag(self, event):
        """Beendet das Drag & Drop einer Aufgabe"""
        if hasattr(self, 'drag_data'):
            # Finde die Zielkategorie
            target_found = False
            
            # Durchsuche alle Frames im todo_frame
            for category_frame in self.todo_frame.winfo_children():
                if isinstance(category_frame, ttk.Frame):
                    # Suche nach dem Container-Frame
                    for container in category_frame.winfo_children():
                        if isinstance(container, ttk.Frame) and hasattr(container, 'category'):
                            x = container.winfo_rootx()
                            y = container.winfo_rooty()
                            width = container.winfo_width()
                            height = container.winfo_height()
                            
                            # Prüfe, ob der Mauszeiger über diesem Container ist
                            if (x < event.x_root < x + width and
                                y < event.y_root < y + height):
                                target_category = container.category
                                
                                # Nur aktualisieren, wenn sich die Kategorie ändert
                                if target_category != self.drag_data['original_category']:
                                    todo = self.todo_manager.get_all()[self.drag_data['index']]
                                    todo['category'] = target_category
                                    self.todo_manager.update(self.drag_data['index'], todo)
                                    self.show_all_todos()
                                target_found = True
                                break
                    
                    if target_found:
                        break
            
            # Cleanup
            self.drag_frame.destroy()
            del self.drag_frame
            delattr(self, 'drag_data')

    def highlight_dropzone(self, frame, highlight=True):
        """Hebt eine potenzielle Drop-Zone hervor"""
        if highlight:
            frame.configure(style='TodoContainerHighlight.TFrame')
        else:
            frame.configure(style='TodoContainer.TFrame')

    def show_main_menu(self, event):
        """Zeigt das Hauptmenü"""
        menu = tk.Menu(self.root, tearoff=0)
        
        # Einstellungen
        menu.add_command(label="⚙ Einstellungen", command=self.show_settings)
        menu.add_separator()
        
        # Kategorien
        menu.add_command(label="📁 Kategorien verwalten", command=lambda: self.show_category_menu(event))
        menu.add_separator()
        
        # Sortierung
        sort_menu = tk.Menu(menu, tearoff=0)
        sort_menu.add_command(label="Nach Priorität", command=lambda: self.sort_todos('priority'))
        sort_menu.add_command(label="Nach Deadline", command=lambda: self.sort_todos('deadline'))
        sort_menu.add_command(label="Nach Text", command=lambda: self.sort_todos('text'))
        menu.add_cascade(label="🔄 Sortieren", menu=sort_menu)
        
        # Filter
        filter_menu = tk.Menu(menu, tearoff=0)
        filter_menu.add_command(label="Alle anzeigen", command=self.show_all_todos)
        filter_menu.add_command(label="Nur offene", command=lambda: self.filter_todos('open'))
        filter_menu.add_command(label="Nur erledigte", command=lambda: self.filter_todos('completed'))
        menu.add_cascade(label="🔍 Filter", menu=filter_menu)
        
        menu.add_separator()
        menu.add_command(label="❌ Beenden", command=self.close_app)
        
        # Menü an Button-Position anzeigen
        menu.post(event.widget.winfo_rootx(),
                 event.widget.winfo_rooty() + event.widget.winfo_height())

class TodoManager:
    """Daten-Management-Klasse für Todos"""
    
    def __init__(self):
        """Initialisiert den Todo-Manager"""
        self.storage_path = os.path.abspath('todos.txt')
        self.todos = []
        self.load()

    def load(self):
        """Lädt die Todos aus der Datei"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                # Prüfe, ob die Datei leer ist
                content = f.read().strip()
                if not content:  # Leere Datei
                    self.todos = []
                    return
                
                # Zurück zum Dateianfang
                f.seek(0)
                
                # Versuche als CSV zu lesen
                try:
                    reader = csv.DictReader(f)
                    self.todos = []
                    
                    # Prüfe, ob die erforderlichen Felder vorhanden sind
                    if not reader.fieldnames or 'text' not in reader.fieldnames:
                        # Versuche als einfache Textdatei zu lesen
                        f.seek(0)
                        lines = f.readlines()
                        self.todos = []
                        for line in lines:
                            text = line.strip()
                            if text:
                                todo = {
                                    'text': text,
                                    'category': 'Allgemein',
                                    'priority': '►',
                                    'deadline': '',
                                    'completed': False
                                }
                                self.todos.append(todo)
                    else:
                        # Lese als CSV
                        for row in reader:
                            try:
                                todo = {
                                    'text': row['text'],
                                    'category': row.get('category', 'Allgemein'),
                                    'priority': row.get('priority', '►'),
                                    'deadline': row.get('deadline', ''),
                                    'completed': row.get('completed', 'False') == 'True'
                                }
                                self.todos.append(todo)
                            except Exception as e:
                                print(f"Fehler beim Laden eines Todos: {e}")
                                continue
                
                except csv.Error:
                    # Wenn CSV-Parsing fehlschlägt, versuche als einfache Textdatei
                    f.seek(0)
                    lines = f.readlines()
                    self.todos = []
                    for line in lines:
                        text = line.strip()
                        if text:
                            todo = {
                                'text': text,
                                'category': 'Allgemein',
                                'priority': '►',
                                'deadline': '',
                                'completed': False
                            }
                            self.todos.append(todo)
                
        except FileNotFoundError:
            self.todos = []
        except Exception as e:
            print(f"Fehler beim Laden der Todos: {e}")
            self.todos = []
        
        # Speichere im CSV-Format für zukünftige Verwendung
        self.save()

    def save(self):
        """Speichert die Todos in der Datei"""
        try:
            with open(self.storage_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['text', 'category', 'priority', 'deadline', 'completed']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for todo in self.todos:
                    writer.writerow(todo)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    def add(self, todo):
        """Fügt ein neues Todo hinzu"""
        if 'text' not in todo:
            raise ValueError("Todo muss einen Text haben")
        
        # Standardwerte setzen
        todo.setdefault('category', 'Allgemein')
        todo.setdefault('priority', '►')
        todo.setdefault('deadline', '')
        todo.setdefault('completed', False)
        
        self.todos.append(todo)
        self.save()
        return len(self.todos) - 1  # Index des neuen Todos

    def update(self, index, todo):
        """Aktualisiert ein bestehendes Todo"""
        if 0 <= index < len(self.todos):
            if 'text' not in todo:
                raise ValueError("Todo muss einen Text haben")
            
            # Bestehende Werte beibehalten wenn nicht angegeben
            updated_todo = self.todos[index].copy()
            updated_todo.update(todo)
            self.todos[index] = updated_todo
            self.save()
            return True
        return False

    def delete(self, index):
        """Löscht ein Todo"""
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            self.save()
            return True
        return False

    def get_all(self):
        """Gibt alle Todos zurück"""
        return self.todos

    def get_by_category(self, category):
        """Gibt alle Todos einer Kategorie zurück"""
        return [todo for todo in self.todos 
                if todo.get('category', 'Allgemein') == category]

    def get_by_priority(self, priority):
        """Gibt alle Todos einer Priorität zurück"""
        return [todo for todo in self.todos 
                if todo.get('priority', '►') == priority]

    def search(self, query):
        """Sucht in allen Todos"""
        query = query.lower()
        return [todo for todo in self.todos 
                if query in todo['text'].lower()]

    def toggle_completed(self, index):
        """Ändert den Completed-Status eines Todos"""
        if 0 <= index < len(self.todos):
            self.todos[index]['completed'] = not self.todos[index].get('completed', False)
            self.save()
            return True
        return False

    def cleanup(self):
        """Entfernt erledigte Todos"""
        self.todos = [todo for todo in self.todos 
                     if not todo.get('completed', False)]
        self.save()

if __name__ == "__main__":
    app = TodoApp()
    app.root.mainloop()