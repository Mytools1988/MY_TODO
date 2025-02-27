import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import winreg

# Füge das Hauptverzeichnis zum Python-Path hinzu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.constants import COLORS, TRANSLATIONS
from app.todo_manager import TodoManager
from app.gui import styles, title_bar, todo_list
from app.gui.menu import create_menu, show_category_menu
from app.gui.settings import SettingsDialog
from app.updater import Updater

class TodoApp:
    def __init__(self):
        # Hauptfenster erstellen
        self.root = tk.Tk()
        
        # Pfade definieren
        self.storage_path = os.path.abspath('todos.txt')
        self.categories_path = os.path.abspath('categories.txt')
        self.settings_path = os.path.abspath('settings.txt')
        
        try:
            # 1. Standardwerte laden
            self.load_initial_settings()
            
            # 2. Kategorien laden
            self.load_categories()
            
            # 3. Datenmanager initialisieren
            self.todo_manager = TodoManager()
            
            # 4. Fenster einrichten
            self.setup_window()
            
            # 5. Styles einrichten
            styles.setup_styles(self)
            
            # 6. GUI erstellen
            self.create_gui()
            
            # 7. Todos laden und anzeigen
            self.load_todos()
            
            # Updater initialisieren
            self.updater = Updater()
            
            # Auf Updates prüfen
            self.check_for_updates()
            
            
        except Exception as e:
            print(f"Fehler beim Initialisieren der App: {e}")
            raise

    def load_initial_settings(self):
        """Lädt die initialen Einstellungen"""
        try:
            # Standardwerte
            self.settings = {
                'window_position': 'br',
                'window_size': '300,700',
                'theme': 'dark'
            }
            
            # Fenstergröße aus Standardwerten
            self.window_width = 300
            self.window_height = 700
            
            # Versuche gespeicherte Einstellungen zu laden
            try:
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    saved_settings = dict(line.strip().split('=') for line in f if '=' in line)
                    self.settings.update(saved_settings)
                    
                    # Fenstergröße aus gespeicherten Einstellungen
                    if 'window_size' in saved_settings:
                        width, height = saved_settings['window_size'].split(',')
                        self.window_width = int(width)
                        self.window_height = int(height)
            except FileNotFoundError:
                pass
            
            # Theme setzen
            self.colors = COLORS[self.settings.get('theme', 'dark')]
            
        except Exception as e:
            print(f"Fehler beim Laden der initialen Einstellungen: {e}")
            # Fallback zu Standardwerten
            self.colors = COLORS['dark']
            self.window_width = 300
            self.window_height = 700

    def setup_window(self):
        """Initialisiert das Hauptfenster"""
        try:
            self.root.title("Actiontext")
            self.root.configure(bg=self.colors['bg'])
            
            # Fenster im Hintergrund halten
            if sys.platform == "win32":  # Windows
                self.root.attributes('-topmost', False)
                self.root.wm_attributes("-topmost", 0)
            elif sys.platform == "darwin":  # macOS
                self.root.attributes('-topmost', False)
            else:  # Linux und andere
                self.root.attributes('-topmost', False)
            
            self.root.overrideredirect(True)
            self.root.attributes('-alpha', 0.95)
            
            # Fenstergröße setzen
            self.root.geometry(f"{self.window_width}x{self.window_height}")
            
            # Gespeicherte Position anwenden
            saved_position = self.settings.get('window_position', 'br')
            self.apply_window_position(saved_position)
            
            # Fenster in den Hintergrund
            self.root.lower()
            
            # Event-Binding für Fenster-Fokus
            self.root.bind('<FocusIn>', self.on_focus_gained)
            
        except Exception as e:
            print(f"Fehler beim Setup des Fensters: {e}")

    def on_focus_gained(self, event):
        """Wird aufgerufen, wenn das Fenster den Fokus erhält"""
        try:
            # Fenster wieder in den Hintergrund
            self.root.lower()
        except Exception as e:
            print(f"Fehler beim Fokus-Management: {e}")

    def create_gui(self):
        """Erstellt die komplette GUI"""
        try:
            # 1. Titelleiste
            title_bar.create_title_bar(self)
            
            # 2. Todo-Liste
            todo_list.create_todo_list(self)
            
            # 3. Untere Leiste
            self.create_bottom_bar()
            
            # 4. Event-Bindings
            self._setup_bindings()
            
            # 5. Todos sofort anzeigen
            if hasattr(self, 'todo_frame'):
                # Todos nach Kategorien gruppieren
                todos_by_category = {}
                for todo in self.todo_manager.get_all():
                    category = todo.get('category', 'Allgemein')
                    if category not in todos_by_category:
                        todos_by_category[category] = []
                    todos_by_category[category].append(todo)
                
                # Alle Kategorien anzeigen
                for category in sorted(self.categories):
                    # Container für diese Kategorie
                    category_container = ttk.Frame(self.todo_frame, style='DropZone.TFrame')
                    category_container.pack(fill=tk.X, pady=(5, 2))
                    category_container.category = category
                    
                    # Header-Frame für Kategorie
                    header_frame = ttk.Frame(category_container, style='CategoryHeader.TFrame')
                    header_frame.pack(fill=tk.X, padx=8, pady=1)
                    
                    # Expand/Collapse Button
                    expand_btn = ttk.Label(header_frame,
                                        text="▼",
                                        style='CategoryExpand.TLabel',
                                        cursor="hand2")
                    expand_btn.pack(side=tk.LEFT, padx=(2, 5))
                    
                    # Kategorie-Label mit Anzahl
                    count = len(todos_by_category.get(category, []))
                    category_label = ttk.Label(header_frame,
                                            text=f"{category} ({count})",
                                            style='CategoryTitle.TLabel')
                    category_label.pack(side=tk.LEFT, fill=tk.X)
                    
                    # Container für Todos dieser Kategorie
                    todos_frame = ttk.Frame(category_container, style='Dark.TFrame')
                    todos_frame.pack(fill=tk.X, expand=True)
                    
                    # Todos anzeigen
                    if category in todos_by_category:
                        for todo in self._sort_by(todos_by_category[category]):
                            todo_list.create_todo_item(self, todos_frame, todo)
                    
                    # Expand/Collapse Funktionalität
                    def toggle_category(frame=todos_frame, btn=expand_btn):
                        if frame.winfo_viewable():
                            frame.pack_forget()
                            btn.configure(text="▶")
                        else:
                            frame.pack(fill=tk.X, expand=True)
                            btn.configure(text="▼")
                    
                    expand_btn.bind('<Button-1>', lambda e, t=toggle_category: t())
                    
                    # Dropzone-Effekte
                    category_container.bind('<Enter>', 
                        lambda e, f=category_container: self.highlight_dropzone(f, True))
                    category_container.bind('<Leave>', 
                        lambda e, f=category_container: self.highlight_dropzone(f, False))
                
                # Fensterhöhe anpassen
                self.adjust_height()
            
        except Exception as e:
            print(f"Fehler beim Erstellen der GUI: {e}")

    def create_main_area(self):
        """Erstellt den Hauptbereich"""
        todo_list.create_todo_list(self)

    def create_title_bar(self):
        """Erstellt die Titelleiste"""
        title_bar.create_title_bar(self)

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

    def _setup_bindings(self):
        """Richtet die Event-Bindings ein"""
        try:
            # Fenster verschieben
            self.title_bar.bind('<Button-1>', self.start_move)
            self.title_bar.bind('<B1-Motion>', self.on_move)
            
            # Suche
            if hasattr(self, 'search_entry'):
                self.search_entry.bind('<KeyRelease>', self.on_search)
        except Exception as e:
            print(f"Fehler beim Einrichten der Bindings: {e}")

    def show_settings(self):
        """Öffnet den Einstellungsdialog"""
        from app.gui.settings import show_settings
        show_settings(self)

    def load_categories(self):
        """Lädt die Kategorien aus der Datei"""
        try:
            with open(self.categories_path, 'r', encoding='utf-8') as f:
                categories = [line.strip() for line in f.readlines() if line.strip()]
                self.categories = categories if categories else ["Allgemein"]
        except FileNotFoundError:
            self.categories = ["Allgemein"]
            self.save_categories()  # Erstelle die Datei mit Standardkategorie
        
        # Stelle sicher, dass "Allgemein" immer existiert
        if "Allgemein" not in self.categories:
            self.categories.insert(0, "Allgemein")

    def save_categories(self):
        """Speichert die Kategorien in der Datei"""
        try:
            with open(self.categories_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.categories))
        except Exception as e:
            print(f"Fehler beim Speichern der Kategorien: {e}")

    def load_todos(self):
        """Lädt und zeigt die Todos an"""
        try:
            # Todos laden
            self.todo_manager.load()
            
            # Warten bis GUI bereit ist
            if not hasattr(self, 'todo_frame'):
                self.root.after(100, self.load_todos)
                return
            
            # GUI aktualisieren
            for widget in self.todo_frame.winfo_children():
                widget.destroy()
            
            # Todos nach Kategorien gruppieren
            todos_by_category = {}
            for todo in self.todo_manager.get_all():
                # Stelle sicher, dass jedes Todo eine Kategorie hat
                category = todo.get('category', 'Allgemein')
                if not category or category not in self.categories:
                    category = 'Allgemein'
                    todo['category'] = category
                
                if category not in todos_by_category:
                    todos_by_category[category] = []
                todos_by_category[category].append(todo)
            
            # Alle Kategorien anzeigen
            for category in sorted(self.categories):
                # Container für diese Kategorie
                category_container = ttk.Frame(self.todo_frame, style='DropZone.TFrame')
                category_container.pack(fill=tk.X, pady=(5, 2))
                category_container.category = category
                
                # Header-Frame für Kategorie
                header_frame = ttk.Frame(category_container, style='CategoryHeader.TFrame')
                header_frame.pack(fill=tk.X, padx=8, pady=1)
                
                # Expand/Collapse Button
                expand_btn = ttk.Label(header_frame,
                                    text="▼",
                                    style='CategoryExpand.TLabel',
                                    cursor="hand2")
                expand_btn.pack(side=tk.LEFT, padx=(2, 5))
                
                # Kategorie-Label mit Anzahl
                count = len(todos_by_category.get(category, []))
                category_label = ttk.Label(header_frame,
                                        text=f"{category} ({count})",
                                        style='CategoryTitle.TLabel')
                category_label.pack(side=tk.LEFT, fill=tk.X)
                
                # Container für Todos dieser Kategorie
                todos_frame = ttk.Frame(category_container, style='Dark.TFrame')
                todos_frame.pack(fill=tk.X, expand=True)
                
                # Todos anzeigen
                if category in todos_by_category:
                    # Sortiere Todos nach Priorität und Deadline
                    sorted_todos = self._sort_by(todos_by_category[category])
                    for todo in sorted_todos:
                        todo_list.create_todo_item(self, todos_frame, todo)
                
                # Expand/Collapse Funktionalität
                def toggle_category(frame=todos_frame, btn=expand_btn):
                    if frame.winfo_viewable():
                        frame.pack_forget()
                        btn.configure(text="▶")
                    else:
                        frame.pack(fill=tk.X, expand=True)
                        btn.configure(text="▼")
                
                expand_btn.bind('<Button-1>', lambda e, t=toggle_category: t())
                
                # Dropzone-Effekte
                category_container.bind('<Enter>', 
                    lambda e, f=category_container: self.highlight_dropzone(f, True))
                category_container.bind('<Leave>', 
                    lambda e, f=category_container: self.highlight_dropzone(f, False))
            
            # Fensterhöhe anpassen
            self.adjust_height()
            
        except Exception as e:
            print(f"Fehler beim Laden der Todos: {e}")

    def save_settings(self, settings=None):
        """Speichert die Einstellungen"""
        try:
            # Aktuelle Einstellungen aus self.settings laden
            current_settings = self.settings.copy()
            
            # Neue Einstellungen übernehmen wenn vorhanden
            if settings:
                current_settings.update(settings)
                # Auch die internen Einstellungen aktualisieren
                self.settings.update(settings)
            
            # Speichern
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                for key, value in current_settings.items():
                    f.write(f"{key}={value}\n")
                
        except Exception as e:
            print(f"Fehler beim Speichern der Einstellungen: {e}")

    def apply_window_position(self, position):
        """Wendet die Fensterposition an"""
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            padding = 10
            
            # Position setzen
            if position == "tr":  # Oben Rechts
                x = screen_width - self.window_width - padding
                y = padding
            elif position == "br":  # Unten Rechts
                x = screen_width - self.window_width - padding
                y = screen_height - self.window_height - padding
            elif position == "bl":  # Unten Links
                x = padding
                y = screen_height - self.window_height - padding
            elif position == "tl":  # Oben Links
                x = padding
                y = padding
            elif position == "custom":  # Benutzerdefinierte Position
                # Lade gespeicherte Position
                x = int(self.settings.get('custom_x', 0))
                y = int(self.settings.get('custom_y', 0))
                
                # Stelle sicher, dass das Fenster auf dem Bildschirm bleibt
                x = max(0, min(x, screen_width - self.window_width))
                y = max(0, min(y, screen_height - self.window_height))
            else:
                # Standardposition: Unten Rechts
                x = screen_width - self.window_width - padding
                y = screen_height - self.window_height - padding
                position = "br"
            
            # Fensterposition setzen
            self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
            
            # Position in Einstellungen speichern
            self.settings['window_position'] = position
            if position == "custom":
                self.settings['custom_x'] = x
                self.settings['custom_y'] = y
            
            # Einstellungen speichern
            self.save_settings()
            
        except Exception as e:
            print(f"Fehler beim Anwenden der Fensterposition: {e}")

    def show_main_menu(self, event):
        """Zeigt das Hauptmenü"""
        try:
            create_menu(self, event)
        except Exception as e:
            print(f"Fehler beim Anzeigen des Menüs: {e}")

    def sort_todos(self, sort_by):
        """Sortiert die Todos nach verschiedenen Kriterien"""
        try:
            todos = self.todo_manager.get_all()
            
            if sort_by == 'priority':
                # Prioritätsreihenfolge: ▲ (hoch), ► (mittel), ▼ (niedrig)
                priority_order = {'▲': 1, '►': 2, '▼': 3}
                todos.sort(key=lambda x: priority_order.get(x.get('priority', '►'), 2))
            
            elif sort_by == 'deadline':
                # Todos mit Deadline zuerst, dann nach Datum sortiert
                def deadline_key(todo):
                    if not todo.get('deadline'):
                        return (1, '')  # Todos ohne Deadline ans Ende
                    return (0, todo['deadline'])
                todos.sort(key=deadline_key)
            
            elif sort_by == 'text':
                # Alphabetisch nach Text sortieren
                todos.sort(key=lambda x: x.get('text', '').lower())
            
            # Sortierte Liste speichern und anzeigen
            self.todo_manager.todos = todos  # Aktualisiere die Liste direkt
            self.todo_manager.save()  # Nutze die vorhandene save Methode
            self.show_all_todos()
            
        except Exception as e:
            print(f"Fehler beim Sortieren der Todos: {e}")

    def filter_todos(self, filter_type):
        """Filtert die Todos nach Status"""
        try:
            todos = self.todo_manager.get_all()
            filtered_todos = []
            
            if filter_type == 'open':
                filtered_todos = [todo for todo in todos if not todo.get('completed', False)]
            elif filter_type == 'completed':
                filtered_todos = [todo for todo in todos if todo.get('completed', False)]
            else:
                filtered_todos = todos
            
            # GUI aktualisieren
            for widget in self.todo_frame.winfo_children():
                widget.destroy()
            
            # Gefilterte Todos anzeigen
            for todo in self._sort_by(filtered_todos):
                todo_list.create_todo_item(self, self.todo_frame, todo)
            
            self.adjust_height()
            
        except Exception as e:
            print(f"Fehler beim Filtern der Todos: {e}")

    def _sort_by(self, todos):
        """Interne Sortiermethode für die Anzeige"""
        # Standardsortierung: Nicht erledigte zuerst, dann nach Priorität
        priority_order = {'▲': 1, '►': 2, '▼': 3}
        return sorted(todos,
                     key=lambda x: (x.get('completed', False),
                                  priority_order.get(x.get('priority', '►'), 2)))

    def show_all_todos(self):
        """Zeigt alle Todos an"""
        try:
            if not hasattr(self, 'todo_frame'):
                return
            
            # GUI aktualisieren
            for widget in self.todo_frame.winfo_children():
                widget.destroy()
            
            # Todos nach Kategorien gruppieren
            todos_by_category = {}
            for todo in self.todo_manager.get_all():
                category = todo.get('category', 'Allgemein')
                if category not in todos_by_category:
                    todos_by_category[category] = []
                todos_by_category[category].append(todo)
            
            # Alle Kategorien anzeigen (auch leere)
            for category in sorted(self.categories):
                # Container für diese Kategorie
                category_container = ttk.Frame(self.todo_frame, style='DropZone.TFrame')
                category_container.pack(fill=tk.X, pady=(5, 2))
                category_container.category = category
                
                # Header-Frame für Kategorie
                header_frame = ttk.Frame(category_container, style='CategoryHeader.TFrame')
                header_frame.pack(fill=tk.X, padx=8, pady=1)
                
                # Expand/Collapse Button
                expand_btn = ttk.Label(header_frame,
                                    text="▼",
                                    style='CategoryExpand.TLabel',
                                    cursor="hand2")
                expand_btn.pack(side=tk.LEFT, padx=(2, 5))
                
                # Kategorie-Label mit Anzahl
                count = len(todos_by_category.get(category, []))
                category_label = ttk.Label(header_frame,
                                        text=f"{category} ({count})",
                                        style='CategoryTitle.TLabel')
                category_label.pack(side=tk.LEFT, fill=tk.X)
                
                # Container für Todos dieser Kategorie
                todos_frame = ttk.Frame(category_container, style='Dark.TFrame')
                todos_frame.pack(fill=tk.X, expand=True)
                
                # Todos anzeigen
                if category in todos_by_category:
                    for todo in self._sort_by(todos_by_category[category]):
                        todo_list.create_todo_item(self, todos_frame, todo)
                
                # Expand/Collapse Funktionalität
                def toggle_category(frame=todos_frame, btn=expand_btn):
                    if frame.winfo_viewable():
                        frame.pack_forget()
                        btn.configure(text="▶")
                    else:
                        frame.pack(fill=tk.X, expand=True)
                        btn.configure(text="▼")
                
                expand_btn.bind('<Button-1>', lambda e, t=toggle_category: t())
                
                # Dropzone-Effekte
                category_container.bind('<Enter>', 
                    lambda e, f=category_container: self.highlight_dropzone(f, True))
                category_container.bind('<Leave>', 
                    lambda e, f=category_container: self.highlight_dropzone(f, False))
            
            # Fensterhöhe anpassen
            self.adjust_height()
            
        except Exception as e:
            print(f"Fehler beim Anzeigen der Todos: {e}")

    def _is_overdue(self, deadline):
        """Prüft, ob eine Deadline überschritten ist"""
        if not deadline:
            return False
        try:
            # Versuche zuerst mit Uhrzeit zu parsen
            try:
                deadline_date = datetime.strptime(deadline, "%d.%m.%Y %H:%M")
            except ValueError:
                # Wenn keine Uhrzeit, dann nur Datum mit 23:59 als Zeit
                deadline_date = datetime.strptime(deadline, "%d.%m.%Y")
                deadline_date = deadline_date.replace(hour=23, minute=59)
            
            return deadline_date < datetime.now()
        except:
            return False

    def start_drag(self, event, frame):
        """Startet das Drag & Drop einer Aufgabe"""
        try:
            self.drag_data = {
                'x': event.x_root,
                'y': event.y_root,
                'frame': frame,
                'original_style': frame.cget('style')  # Speichere den originalen Style
            }
            frame.configure(style='TodoModernHover.TFrame')
        except Exception as e:
            print(f"Fehler beim Starten des Drag & Drop: {e}")

    def on_drag(self, event):
        """Bewegt eine Aufgabe während des Drag & Drop"""
        try:
            if hasattr(self, 'drag_data'):
                # Berechne die Bewegung
                dx = event.x_root - self.drag_data['x']
                dy = event.y_root - self.drag_data['y']
                
                # Bewege das Frame
                frame = self.drag_data['frame']
                x = frame.winfo_x() + dx
                y = frame.winfo_y() + dy
                frame.place(x=x, y=y)
                
                # Aktualisiere die Position
                self.drag_data['x'] = event.x_root
                self.drag_data['y'] = event.y_root
                
                # Finde mögliche Dropzones
                self.find_dropzone(event)
        except Exception as e:
            print(f"Fehler während des Drag & Drop: {e}")

    def end_drag(self, event):
        """Beendet das Drag & Drop einer Aufgabe"""
        try:
            if hasattr(self, 'drag_data'):
                frame = self.drag_data['frame']
                original_style = self.drag_data.get('original_style', 'TodoModern.TFrame')
                
                # Setze den ursprünglichen Style zurück
                frame.configure(style=original_style)
                frame.pack(fill=tk.X, pady=3, padx=8)  # Zurück zum normalen Layout
                
                # Führe Drop-Aktion aus wenn über einer Kategorie
                if hasattr(self, 'current_dropzone'):
                    self.drop_todo(frame.todo_index, self.current_dropzone.category)
                    delattr(self, 'current_dropzone')
                
                # Cleanup
                delattr(self, 'drag_data')
        except Exception as e:
            print(f"Fehler beim Beenden des Drag & Drop: {e}")

    def find_dropzone(self, event):
        """Findet mögliche Dropzones während des Drag & Drop"""
        try:
            # Finde das Widget unter dem Cursor
            x = event.x_root
            y = event.y_root
            target = event.widget.winfo_containing(x, y)
            
            # Suche nach dem nächsten Frame mit category Attribut
            while target and not hasattr(target, 'category'):
                target = target.master
            
            # Alte Dropzone zurücksetzen
            if hasattr(self, 'current_dropzone'):
                self.highlight_dropzone(self.current_dropzone, False)
            
            # Neue Dropzone markieren
            if target and hasattr(target, 'category'):
                self.current_dropzone = target
                self.highlight_dropzone(target, True)
        except Exception as e:
            print(f"Fehler beim Suchen der Dropzone: {e}")

    def drop_todo(self, todo_index, new_category):
        """Verschiebt ein Todo in eine neue Kategorie"""
        try:
            todos = self.todo_manager.get_all()
            if 0 <= todo_index < len(todos):
                todos[todo_index]['category'] = new_category
                self.todo_manager.save()
                self.show_all_todos()
        except Exception as e:
            print(f"Fehler beim Verschieben des Todos: {e}")

    def show_category_menu(self, event):
        """Zeigt das Kategorie-Menü"""
        show_category_menu(self, event)

    def create_dialog(self, title, width=400, height=350):
        """Erstellt ein einheitlich gestyltes Dialog-Fenster"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry(f"{width}x{height}")
        dialog.transient(self.root)
        
        # Dunkles Theme
        dialog.configure(bg=self.colors['bg'])
        
        # Hauptframe
        main_frame = ttk.Frame(dialog, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        return dialog, main_frame

    def add_todo(self, event=None):
        """Fügt ein neues Todo hinzu"""
        dialog, main_frame = self.create_dialog("Neue Aufgabe")
        
        # Text
        ttk.Label(main_frame, 
                 text="Aufgabe:",
                 style='TodoText.TLabel').pack(anchor="w")
        text_entry = ttk.Entry(main_frame,
                              width=40,
                              style='TodoEntry.TEntry')
        text_entry.pack(fill=tk.X, pady=(0, 20))
        text_entry.focus()
        
        # Kategorie
        ttk.Label(main_frame, 
                 text="Kategorie:",
                 style='TodoText.TLabel').pack(anchor="w")
        category_var = tk.StringVar(value="Allgemein")
        category_combo = ttk.Combobox(main_frame,
                                    textvariable=category_var,
                                    values=self.categories,
                                    state="readonly",
                                    style='TodoCombobox.TCombobox')
        category_combo.pack(fill=tk.X, pady=(0, 20))
        
        # Priorität
        ttk.Label(main_frame, 
                 text="Priorität:",
                 style='TodoText.TLabel').pack(anchor="w")
        priority_var = tk.StringVar(value="►")
        priority_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        priority_frame.pack(fill=tk.X, pady=(0, 20))
        
        for text, value in [("Hoch", "▲"), ("Mittel", "►"), ("Niedrig", "▼")]:
            ttk.Radiobutton(priority_frame,
                           text=text,
                           value=value,
                           variable=priority_var,
                           style='TodoRadio.TRadiobutton').pack(side=tk.LEFT, padx=5)
        
        # Deadline
        ttk.Label(main_frame, 
                 text="Deadline:",
                 style='TodoText.TLabel').pack(anchor="w")
        
        deadline_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        deadline_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Datum
        date_frame = ttk.Frame(deadline_frame, style='Dark.TFrame')
        date_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(date_frame, 
                 text="Datum (z.B. 31.12.2024):",
                 style='TodoText.TLabel').pack(anchor="w")
        date_entry = ttk.Entry(date_frame,
                              style='TodoEntry.TEntry')
        date_entry.pack(fill=tk.X)
        
        # Uhrzeit
        time_frame = ttk.Frame(deadline_frame, style='Dark.TFrame')
        time_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        ttk.Label(time_frame, 
                 text="Uhrzeit (optional, z.B. 14:30):",
                 style='TodoText.TLabel').pack(anchor="w")
        time_entry = ttk.Entry(time_frame,
                              style='TodoEntry.TEntry')
        time_entry.pack(fill=tk.X)
        
        def save_todo():
            text = text_entry.get().strip()
            if text:
                # Deadline zusammensetzen
                date = date_entry.get().strip()
                time = time_entry.get().strip()
                
                deadline = ""
                if date:
                    deadline = date
                    if time:
                        deadline += f" {time}"
                
                todo = {
                    'text': text,
                    'category': category_var.get(),
                    'priority': priority_var.get(),
                    'deadline': deadline,
                    'completed': False
                }
                self.todo_manager.add(todo)
                self.show_all_todos()
                dialog.destroy()
            else:
                messagebox.showwarning("Warnung", "Bitte geben Sie einen Text ein.")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_btn = ttk.Button(button_frame,
                             text="Speichern",
                             style='TodoButton.TButton',
                             command=save_todo)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame,
                               text="Abbrechen",
                               style='TodoButton.TButton',
                               command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def confirm_delete(self):
        """Bestätigt das Löschen einer Aufgabe"""
        return messagebox.askyesno(
            "Aufgabe löschen",
            "Möchten Sie diese Aufgabe wirklich löschen?",
            icon='warning'
        )

    def toggle_todo_completed(self, index):
        """Ändert den Completed-Status eines Todos"""
        try:
            # Hole das Todo
            todos = self.todo_manager.get_all()
            if 0 <= index < len(todos):
                todo = todos[index]
                
                # Ändere den Status
                todo['completed'] = not todo.get('completed', False)
                
                # Aktualisiere das Todo
                self.todo_manager.update(index, todo)
                
                # Speichere die Änderungen
                self.todo_manager.save()
                
                # GUI nur bei Bedarf aktualisieren
                # self.show_all_todos()  # Diese Zeile auskommentieren
                
                return True
        except Exception as e:
            print(f"Fehler beim Ändern des Todo-Status: {e}")
            return False

    def add_category(self):
        """Fügt eine neue Kategorie hinzu"""
        dialog, main_frame = self.create_dialog("Neue Kategorie", width=300, height=150)
        
        ttk.Label(main_frame, 
                 text="Name der Kategorie:",
                 style='TodoText.TLabel').pack(anchor="w")
        
        name_entry = ttk.Entry(main_frame,
                              width=40,
                              style='TodoEntry.TEntry')
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
        
        button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        button_frame.pack(fill=tk.X)
        
        save_btn = ttk.Button(button_frame,
                             text="Speichern",
                             style='TodoButton.TButton',
                             command=save_category)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame,
                               text="Abbrechen",
                               style='TodoButton.TButton',
                               command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def remove_category(self):
        """Entfernt eine Kategorie"""
        dialog, main_frame = self.create_dialog("Kategorie entfernen", width=300, height=200)
        
        ttk.Label(main_frame, 
                 text="Kategorie auswählen:",
                 style='TodoText.TLabel').pack(anchor="w")
        
        category_var = tk.StringVar()
        category_list = ttk.Combobox(main_frame,
                                    textvariable=category_var,
                                    values=[cat for cat in self.categories if cat != "Allgemein"],
                                    state="readonly",
                                    style='TodoCombobox.TCombobox')
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
        
        button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        delete_btn = ttk.Button(button_frame,
                               text="Löschen",
                               style='TodoButton.TButton',
                               command=delete_category)
        delete_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame,
                               text="Abbrechen",
                               style='TodoButton.TButton',
                               command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def filter_by_category(self, category):
        """Filtert Todos nach Kategorie"""
        todos = self.todo_manager.get_by_category(category)
        
        # GUI aktualisieren
        for widget in self.todo_frame.winfo_children():
            widget.destroy()
        
        for todo in self._sort_by(todos):
            todo_list.create_todo_item(self, self.todo_frame, todo)
        
        self.adjust_height()  # Am Ende der Methode hinzufügen

    def count_todos_in_category(self, category):
        """Zählt die Todos in einer Kategorie"""
        return len([todo for todo in self.todo_manager.get_all() 
                   if todo.get('category', 'Allgemein') == category])

    def highlight_dropzone(self, frame, highlight):
        """Hebt eine potenzielle Dropzone hervor"""
        try:
            if highlight:
                frame.configure(style='DropZoneHighlight.TFrame')
                # Cursor ändern
                for child in frame.winfo_children():
                    child.configure(cursor='hand2')
            else:
                frame.configure(style='DropZone.TFrame')
                # Cursor zurücksetzen
                for child in frame.winfo_children():
                    child.configure(cursor='')
        except Exception as e:
            print(f"Fehler beim Hervorheben der Dropzone: {e}")

    def adjust_height(self):
        """Behält die feste Fensterhöhe bei"""
        # Feste Höhe beibehalten
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def on_search(self, event=None):
        """Sucht in den Todos"""
        query = self.search_entry.get().strip()
        if query:
            results = self.todo_manager.search(query)
            # Ergebnisse anzeigen
            for widget in self.todo_frame.winfo_children():
                widget.destroy()
            for todo in self._sort_by(results):
                todo_list.create_todo_item(self, self.todo_frame, todo)
        else:
            self.show_all_todos()

    def start_move(self, event):
        """Startet das Verschieben des Fensters"""
        self._drag_data = {
            'x': event.x_root - self.root.winfo_x(),
            'y': event.y_root - self.root.winfo_y()
        }

    def on_move(self, event):
        """Bewegt das Fenster"""
        if hasattr(self, '_drag_data'):
            x = event.x_root - self._drag_data['x']
            y = event.y_root - self._drag_data['y']
            self.root.geometry(f"+{x}+{y}")
            
            # Position als 'custom' speichern
            self.settings['window_position'] = 'custom'
            self.settings['custom_x'] = x
            self.settings['custom_y'] = y
            self.save_settings()

    def edit_todo(self, index):
        """Bearbeitet ein bestehendes Todo"""
        try:
            todo = self.todo_manager.get_all()[index]
            dialog, main_frame = self.create_dialog("Aufgabe bearbeiten")
            
            # Text
            ttk.Label(main_frame, 
                     text="Aufgabe:",
                     style='TodoText.TLabel').pack(anchor="w")
            text_entry = ttk.Entry(main_frame,
                                 width=40,
                                 style='TodoEntry.TEntry')
            text_entry.insert(0, todo['text'])
            text_entry.pack(fill=tk.X, pady=(0, 20))
            text_entry.focus()
            
            # Kategorie
            ttk.Label(main_frame, 
                     text="Kategorie:",
                     style='TodoText.TLabel').pack(anchor="w")
            category_var = tk.StringVar(value=todo.get('category', 'Allgemein'))
            category_combo = ttk.Combobox(main_frame,
                                        textvariable=category_var,
                                        values=self.categories,
                                        state="readonly",
                                        style='TodoCombobox.TCombobox')
            category_combo.pack(fill=tk.X, pady=(0, 20))
            
            # Priorität
            ttk.Label(main_frame, 
                     text="Priorität:",
                     style='TodoText.TLabel').pack(anchor="w")
            priority_var = tk.StringVar(value=todo.get('priority', '►'))
            priority_frame = ttk.Frame(main_frame, style='Dark.TFrame')
            priority_frame.pack(fill=tk.X, pady=(0, 20))
            
            for text, value in [("Hoch", "▲"), ("Mittel", "►"), ("Niedrig", "▼")]:
                ttk.Radiobutton(priority_frame,
                               text=text,
                               value=value,
                               variable=priority_var,
                               style='TodoRadio.TRadiobutton').pack(side=tk.LEFT, padx=5)
            
            # Deadline
            ttk.Label(main_frame, 
                     text="Deadline:",
                     style='TodoText.TLabel').pack(anchor="w")
            
            deadline_frame = ttk.Frame(main_frame, style='Dark.TFrame')
            deadline_frame.pack(fill=tk.X, pady=(0, 20))
            
            # Datum und Zeit aus dem bestehenden Deadline extrahieren
            date_str = ""
            time_str = ""
            if todo.get('deadline'):
                parts = todo['deadline'].split()
                date_str = parts[0]
                if len(parts) > 1:
                    time_str = parts[1]
            
            # Datum
            date_frame = ttk.Frame(deadline_frame, style='Dark.TFrame')
            date_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            ttk.Label(date_frame, 
                     text="Datum (z.B. 31.12.2024):",
                     style='TodoText.TLabel').pack(anchor="w")
            date_entry = ttk.Entry(date_frame,
                                 style='TodoEntry.TEntry')
            date_entry.insert(0, date_str)
            date_entry.pack(fill=tk.X)
            
            # Uhrzeit
            time_frame = ttk.Frame(deadline_frame, style='Dark.TFrame')
            time_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            
            ttk.Label(time_frame, 
                     text="Uhrzeit (optional, z.B. 14:30):",
                     style='TodoText.TLabel').pack(anchor="w")
            time_entry = ttk.Entry(time_frame,
                                 style='TodoEntry.TEntry')
            time_entry.insert(0, time_str)
            time_entry.pack(fill=tk.X)
            
            def save_changes():
                text = text_entry.get().strip()
                if text:
                    # Deadline zusammensetzen
                    date = date_entry.get().strip()
                    time = time_entry.get().strip()
                    
                    deadline = ""
                    if date:
                        deadline = date
                        if time:
                            deadline += f" {time}"
                    
                    # Todo aktualisieren
                    updated_todo = {
                        'text': text,
                        'category': category_var.get(),
                        'priority': priority_var.get(),
                        'deadline': deadline,
                        'completed': todo.get('completed', False)
                    }
                    
                    self.todo_manager.update(index, updated_todo)
                    self.show_all_todos()
                    dialog.destroy()
                else:
                    messagebox.showwarning("Warnung", "Bitte geben Sie einen Text ein.")
            
            # Buttons
            button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
            button_frame.pack(fill=tk.X, pady=(20, 0))
            
            save_btn = ttk.Button(button_frame,
                                 text="Speichern",
                                 style='TodoButton.TButton',
                                 command=save_changes)
            save_btn.pack(side=tk.RIGHT, padx=5)
            
            cancel_btn = ttk.Button(button_frame,
                                   text="Abbrechen",
                                   style='TodoButton.TButton',
                                   command=dialog.destroy)
            cancel_btn.pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            print(f"Fehler beim Bearbeiten des Todos: {e}")

    def close_app(self):
        """Beendet die Anwendung"""
        if messagebox.askyesno("Beenden", "Möchten Sie die Anwendung wirklich beenden?"):
            self.save_settings()
            self.root.destroy()

    def change_theme(self, theme='dark'):
        """Ändert das Theme der Anwendung"""
        try:
            # Theme aktualisieren
            self.colors = COLORS[theme]
            
            # Styles neu laden
            styles.setup_styles(self)
            
            # Hintergrundfarben aktualisieren
            self.root.configure(bg=self.colors['bg'])
            self.canvas.configure(bg=self.colors['bg'])
            
            # Alle Todos neu laden um Styles anzuwenden
            self.show_all_todos()
            
            # Theme in Einstellungen speichern
            self.save_settings({'theme': theme})
            
        except Exception as e:
            print(f"Fehler beim Ändern des Themes: {e}")

    def load_and_apply_settings(self):
        """Lädt und wendet die gespeicherten Einstellungen an"""
        try:
            # Standardwerte
            settings = {
                'window_position': 'br',
                'custom_x': 0,
                'custom_y': 0,
                'window_size': f"{self.window_width},{self.window_height}",
                'theme': 'dark'
            }
            
            # Versuche gespeicherte Einstellungen zu laden
            try:
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    saved_settings = dict(line.strip().split('=') for line in f if '=' in line)
                    settings.update(saved_settings)
            except FileNotFoundError:
                pass
            
            # Fenstergröße setzen
            try:
                width, height = settings['window_size'].split(',')
                self.window_width = int(width)
                self.window_height = int(height)
            except:
                pass  # Behalte Standardgrößen bei
            
            # Position anwenden
            if settings['window_position'] == 'custom':
                # Stelle sicher, dass das Fenster auf dem Bildschirm bleibt
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                
                x = max(0, min(int(settings['custom_x']), screen_width - self.window_width))
                y = max(0, min(int(settings['custom_y']), screen_height - self.window_height))
                
                self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
            else:
                # Standard-Position anwenden
                self.apply_window_position(settings['window_position'])
            
            # Theme anwenden
            if settings.get('theme'):
                self.colors = COLORS[settings['theme']]
                styles.setup_styles(self)
            
        except Exception as e:
            print(f"Fehler beim Laden der Einstellungen: {e}")
            # Fallback zu Standardposition
            self.root.geometry(f"{self.window_width}x{self.window_height}")
            self.apply_window_position('br')

    def check_for_updates(self):
        """Prüft auf verfügbare Updates"""
        try:
            has_update, new_version = self.updater.check_for_updates()
            if has_update:
                if messagebox.askyesno(
                    "Update verfügbar",
                    f"Version {new_version} ist verfügbar. Jetzt installieren?"
                ):
                    self.updater.download_and_install_update()
        except Exception as e:
            print(f"Fehler beim Update-Check: {e}")

    def open_url(self, url):
        """Öffnet eine URL im Standard-Browser"""
        import webbrowser
        webbrowser.open(url)

    def change_language(self, lang):
        """Ändert die Sprache der App"""
        try:
            # Sprache in Einstellungen speichern
            self.settings['language'] = lang
            self.save_settings()
            
            # GUI-Texte aktualisieren
            self.update_gui_texts()
            
            # Todos neu laden um Texte zu aktualisieren
            self.show_all_todos()
            
        except Exception as e:
            print(f"Fehler beim Ändern der Sprache: {e}")

    def update_gui_texts(self):
        """Aktualisiert alle GUI-Texte nach Sprachänderung"""
        try:
            lang = self.settings.get('language', 'de')
            texts = TRANSLATIONS[lang]
            
            # App-Titel
            self.root.title(texts['app_name'])
            
            # Menü-Texte aktualisieren
            if hasattr(self, 'menu_frame'):
                # Menü neu erstellen um Texte zu aktualisieren
                self.menu_frame.destroy()
                self.show_main_menu(None)
            
            # Filter-Texte aktualisieren
            if hasattr(self, 'filter_label'):
                self.filter_label.configure(text=texts['filters']['all'])
            
            # Dialog-Texte
            self.dialog_texts = {
                'add_todo': {
                    'title': 'Neue Aufgabe' if lang == 'de' else 'New Task',
                    'text': 'Text:',
                    'category': 'Kategorie:' if lang == 'de' else 'Category:',
                    'priority': 'Priorität:' if lang == 'de' else 'Priority:',
                    'deadline': 'Deadline:',
                    'save': 'Speichern' if lang == 'de' else 'Save',
                    'cancel': 'Abbrechen' if lang == 'de' else 'Cancel'
                },
                'edit_todo': {
                    'title': 'Aufgabe bearbeiten' if lang == 'de' else 'Edit Task',
                    'save': 'Speichern' if lang == 'de' else 'Save',
                    'cancel': 'Abbrechen' if lang == 'de' else 'Cancel'
                },
                'confirm': {
                    'delete': 'Löschen bestätigen' if lang == 'de' else 'Confirm Delete',
                    'exit': 'Beenden bestätigen' if lang == 'de' else 'Confirm Exit'
                },
                'priority': {
                    'high': 'Hoch' if lang == 'de' else 'High',
                    'medium': 'Mittel' if lang == 'de' else 'Medium',
                    'low': 'Niedrig' if lang == 'de' else 'Low'
                }
            }
            
            # Menü-Items aktualisieren
            self.menu_items = [
                (texts['menu']['home'], lambda: (self.close_menu_with_animation(), self.show_all_todos())),
                (texts['menu']['settings'], lambda: (self.close_menu_with_animation(), SettingsDialog(self))),
                (texts['menu']['filter'], lambda: self.create_filter_menu()),
                (texts['menu']['notifications'], lambda: self.create_notification_menu()),
                (texts['menu']['language'], lambda: self.create_language_menu()),
                (texts['menu']['theme'], lambda: self.create_theme_menu()),
                (texts['menu']['updates'], lambda: (self.close_menu_with_animation(), self.check_for_updates())),
                (texts['menu']['about'], lambda: self.create_about_menu())
            ]
            
            # Alle Todos neu laden um übersetzte Texte anzuzeigen
            self.show_all_todos()
            
        except Exception as e:
            print(f"Fehler beim Aktualisieren der GUI-Texte: {e}")

    def play_notification_sound(self):
        """Spielt den ausgewählten Benachrichtigungston ab"""
        try:
            if not self.settings.get('notifications_enabled', True):
                return
            
            sound_id = self.settings.get('notification_sound', 'sound1')
            if sound_id == 'mute':
                return
            
            # Hier können Sie die tatsächlichen Sounddateien einbinden
            # Beispiel mit winsound unter Windows:
            if sys.platform == "win32":
                import winsound
                frequency = {
                    'sound1': 1000,
                    'sound2': 800,
                    'sound3': 600
                }.get(sound_id, 1000)
                winsound.Beep(frequency, 200)
            
        except Exception as e:
            print(f"Fehler beim Abspielen des Benachrichtigungstons: {e}")

    def is_autostart_enabled(self):
        """Prüft ob die App im Autostart ist"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, "MY TODO")
                return True
            except WindowsError:
                return False
            finally:
                winreg.CloseKey(key)
        except WindowsError:
            return False

    def toggle_autostart(self):
        """Aktiviert/Deaktiviert Autostart"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            if self.is_autostart_enabled():
                # Autostart deaktivieren
                try:
                    winreg.DeleteValue(key, "MY TODO")
                except WindowsError:
                    pass
            else:
                # Autostart aktivieren
                exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(sys.argv[0])
                winreg.SetValueEx(key, "MY TODO", 0, winreg.REG_SZ, f'"{exe_path}"')
            
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Fehler beim Setzen des Autostarts: {e}")
            return False

if __name__ == "__main__":
    app = TodoApp()  # mainloop wird jetzt in run.py aufgerufen 