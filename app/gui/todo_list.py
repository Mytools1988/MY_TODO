import tkinter as tk
from tkinter import ttk
from datetime import datetime

def create_todo_list(app):
    """Erstellt den scrollbaren Todo-Listen-Bereich"""
    # Hauptcontainer
    app.main_frame = ttk.Frame(app.root)
    app.main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Scrollbarer Bereich mit dunklem Hintergrund
    app.canvas = tk.Canvas(app.main_frame, 
                         bg=app.colors['bg'],  # Hintergrundfarbe direkt setzen
                         highlightthickness=0)
    app.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Scrollbar
    app.scrollbar = ttk.Scrollbar(app.main_frame, 
                                orient=tk.VERTICAL,
                                command=app.canvas.yview)
    
    # Frame für Todos
    app.todo_frame = ttk.Frame(app.canvas)
    app.canvas.create_window((0, 0), 
                           window=app.todo_frame,
                           anchor="nw",
                           tags="todo_frame")
    
    # Scrollbar Konfiguration
    def update_scrollbar(*args):
        if app.todo_frame.winfo_height() > app.canvas.winfo_height():
            app.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            app.scrollbar.pack_forget()
        app.scrollbar.set(*args)
    
    app.canvas.configure(yscrollcommand=update_scrollbar)
    
    # Event Bindings
    def on_frame_configure(event=None):
        """Aktualisiert die Scroll-Region wenn sich die Größe des Inhalts ändert"""
        app.canvas.configure(scrollregion=app.canvas.bbox("all"))
    
    def on_canvas_configure(event):
        """Passt die Breite des inneren Frames an die Canvas-Breite an"""
        if event.width > 1:  # Vermeide 1px Breite beim Start
            app.canvas.itemconfig("todo_frame", width=event.width)
    
    app.todo_frame.bind('<Configure>', on_frame_configure)
    app.canvas.bind('<Configure>', on_canvas_configure)
    
    # Mausrad-Scrolling
    def _on_mousewheel(event):
        app.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    app.canvas.bind_all("<MouseWheel>", _on_mousewheel)

def create_todo_item(app, parent_frame, todo):
    """Erstellt ein einzelnes Todo-Item mit modernem Design"""
    # Hauptcontainer mit Schatten-Effekt
    todo_frame = ttk.Frame(parent_frame, style='TodoModern.TFrame')
    todo_frame.pack(fill=tk.X, pady=3, padx=8)
    
    # Speichere den Index und die Kategorie für Drag & Drop
    todo_frame.todo_index = app.todo_manager.get_all().index(todo)
    todo_frame.category = todo.get('category', 'Allgemein')
    
    # Innerer Container für Padding
    inner_frame = ttk.Frame(todo_frame, style='TodoInner.TFrame')
    inner_frame.pack(fill=tk.X, padx=2, pady=2)
    
    # Linke Seite: Handle, Checkbox und Priorität
    left_frame = ttk.Frame(inner_frame, style='TodoInner.TFrame')
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    
    # Drag Handle mit subtilerem Design
    drag_handle = ttk.Label(left_frame,
                          text="⋮",
                          style='DragHandleModern.TLabel',
                          cursor="fleur")
    drag_handle.pack(side=tk.LEFT, padx=(5, 3))
    
    # Hauptinhalt mit fester Breite für Text
    content_frame = ttk.Frame(inner_frame, style='TodoInner.TFrame')
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 30))
    
    # Text mit besserer Formatierung
    text_frame = ttk.Frame(content_frame, style='TodoInner.TFrame')
    text_frame.pack(fill=tk.X)
    
    text_label = ttk.Label(text_frame,
                          text=todo['text'],
                          style='TodoTextModern.TLabel',
                          wraplength=200)
    text_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(2, 0))
    
    # Doppelklick zum Bearbeiten
    text_label.bind('<Double-Button-1>', lambda e: app.edit_todo(todo_frame.todo_index))
    
    # Checkbox mit angepasstem Design
    completed_var = tk.BooleanVar(value=todo.get('completed', False))
    checkbox = ttk.Checkbutton(left_frame,
                              variable=completed_var,
                              style='TodoCheckbox.TCheckbutton',
                              command=lambda: on_toggle_completed())
    checkbox.pack(side=tk.LEFT, padx=(0, 5))
    
    def on_toggle_completed():
        try:
            app.toggle_todo_completed(todo_frame.todo_index)
            # Visuelles Feedback direkt aktualisieren
            if completed_var.get():
                text_label.configure(style='TodoTextCompleted.TLabel')
            else:
                text_label.configure(style='TodoTextModern.TLabel')
        except Exception as e:
            print(f"Fehler beim Umschalten des Status: {e}")
    
    # Initialer Status
    if todo.get('completed', False):
        text_label.configure(style='TodoTextCompleted.TLabel')
    
    # Prioritätsindikator als farbiger Punkt
    priority_colors = {
        '▲': app.colors['high_priority'],
        '►': app.colors['medium_priority'],
        '▼': app.colors['low_priority']
    }
    priority = todo.get('priority', '►')
    priority_dot = ttk.Label(left_frame,
                           text="●",
                           style='PriorityDot.TLabel')
    priority_dot.configure(foreground=priority_colors[priority])
    priority_dot.pack(side=tk.LEFT, padx=(0, 8))
    
    # Rechte Seite für Löschen-Button (absolut positioniert)
    right_frame = ttk.Frame(inner_frame, style='TodoInner.TFrame')
    right_frame.place(relx=1.0, rely=0.0, anchor='ne')  # Absolute Positionierung
    
    # Löschen-Button
    delete_btn = ttk.Label(right_frame,
                          text="×",
                          style='TodoDelete.TLabel',
                          cursor="hand2")
    delete_btn.pack(padx=5)
    
    # Löschen-Button Events
    def on_delete_enter(e):
        delete_btn.configure(style='TodoDeleteHover.TLabel')
        
    def on_delete_leave(e):
        delete_btn.configure(style='TodoDelete.TLabel')
        
    def delete_todo(e):
        if app.confirm_delete():
            app.todo_manager.delete(todo_frame.todo_index)
            app.show_all_todos()
    
    delete_btn.bind('<Enter>', on_delete_enter)
    delete_btn.bind('<Leave>', on_delete_leave)
    delete_btn.bind('<Button-1>', delete_todo)
    
    # Metadaten-Bereich (nur noch für Deadline)
    if todo.get('deadline'):
        meta_frame = ttk.Frame(content_frame, style='TodoInner.TFrame')
        meta_frame.pack(fill=tk.X, pady=(4, 2))
        
        deadline_frame = ttk.Frame(meta_frame, style='MetaBadge.TFrame')
        deadline_frame.pack(side=tk.LEFT, padx=(0, 6))
        
        is_overdue = app._is_overdue(todo['deadline'])
        deadline_icon = "⚠️" if is_overdue else "⏰"
        icon_style = 'MetaIconAlert.TLabel' if is_overdue else 'MetaIcon.TLabel'
        
        # Icon
        ttk.Label(deadline_frame,
                 text=deadline_icon,
                 style=icon_style).pack(side=tk.LEFT, padx=(4, 2))
        
        # Prioritäts-abhängiger Style für das Datum
        priority = todo.get('priority', '►')
        deadline_style = {
            '▲': 'DeadlineHigh.TLabel',    # Hohe Priorität
            '►': 'DeadlineMedium.TLabel',  # Mittlere Priorität
            '▼': 'DeadlineLow.TLabel'      # Niedrige Priorität
        }.get(priority, 'MetaText.TLabel')
        
        # Formatiere das Datum
        try:
            date_obj = datetime.strptime(todo['deadline'], "%d.%m.%Y")
            formatted_date = date_obj.strftime("%d.%m.%Y")
            formatted_time = date_obj.strftime("%H:%M")
            
            # Datum mit Prioritätsfarbe
            ttk.Label(deadline_frame,
                     text=formatted_date,
                     style=deadline_style).pack(side=tk.LEFT)
            
            # Uhrzeit falls vorhanden
            if formatted_time != "00:00":
                ttk.Label(deadline_frame,
                         text=f" {formatted_time}",
                         style=deadline_style).pack(side=tk.LEFT, padx=(0, 4))
            else:
                ttk.Label(deadline_frame,
                         text="",
                         style=deadline_style).pack(side=tk.LEFT, padx=(0, 4))
        except:
            # Fallback wenn Datum nicht geparst werden kann
            ttk.Label(deadline_frame,
                     text=todo['deadline'],
                     style=deadline_style).pack(side=tk.LEFT, padx=(0, 4))
    
    # Event Bindings
    drag_handle.bind('<Button-1>', lambda e: app.start_drag(e, todo_frame))
    drag_handle.bind('<B1-Motion>', lambda e: app.on_drag(e))
    drag_handle.bind('<ButtonRelease-1>', lambda e: app.end_drag(e))
    
    # Hover Effekte
    def on_enter(e):
        todo_frame.configure(style='TodoModernHover.TFrame')
        drag_handle.configure(style='DragHandleHover.TLabel')
    
    def on_leave(e):
        todo_frame.configure(style='TodoModern.TFrame')
        drag_handle.configure(style='DragHandleModern.TLabel')
    
    todo_frame.bind('<Enter>', on_enter)
    todo_frame.bind('<Leave>', on_leave)
    
    return todo_frame 