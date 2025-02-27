import tkinter as tk
from tkinter import ttk, messagebox
from app.gui.settings import SettingsDialog
from app.constants import TRANSLATIONS

def create_menu(app, event):
    """Erstellt ein modernes, TV-ähnliches Menü innerhalb der App"""
    try:
        # Bestehende Menüs schließen oder umschalten
        if hasattr(app, 'menu_frame'):
            if app.menu_frame.winfo_exists():
                close_menu_with_animation(app)
            else:
                delattr(app, 'menu_frame')
            return
        
        # Menü-Frame erstellen
        app.menu_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
        
        # Feste Größe und Position
        menu_width = 300
        app.menu_frame.place(x=-menu_width, y=0, width=menu_width, height=app.root.winfo_height())
        
        # Hauptframe
        main_frame = ttk.Frame(app.menu_frame, style='TVMenu.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header mit Zurück-Button
        header_frame = ttk.Frame(main_frame, style='TVMenuHeader.TFrame')
        header_frame.pack(fill=tk.X, pady=(10, 20))
        
        # Zurück-Button
        back_btn = ttk.Label(header_frame,
                          text="←",
                          style='TVMenuTitle.TLabel',
                          cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=20)
        back_btn.bind('<Button-1>', lambda e: close_menu_with_animation(app))
        
        # App-Logo und Name
        ttk.Label(header_frame,
                 text="MY TODO",
                 style='TVMenuTitle.TLabel').pack(side=tk.LEFT, padx=20)
        
        # Aktuelle Sprache
        lang = app.settings.get('language', 'de')
        texts = TRANSLATIONS[lang]
        
        # Menüeinträge mit übersetzten Texten
        menu_items = [
            (texts['menu']['home'], lambda: (close_menu_with_animation(app), app.show_all_todos())),
            (texts['menu']['settings'], lambda: create_settings_menu(app, app.menu_frame)),
            (texts['menu']['filter'], lambda: create_filter_menu(app, app.menu_frame)),
            (texts['menu']['notifications'], lambda: create_notification_menu(app, app.menu_frame)),
            (texts['menu']['language'], lambda: create_language_menu(app, app.menu_frame)),
            (texts['menu']['theme'], lambda: create_theme_menu(app, app.menu_frame)),
            (texts['menu']['updates'], lambda: (close_menu_with_animation(app), app.check_for_updates())),
            (texts['menu']['help'], lambda: create_help_menu(app, app.menu_frame)),
            (texts['menu']['about'], lambda: create_about_menu(app, app.menu_frame))
        ]
        
        # Separator nach dem Header
        separator = ttk.Frame(main_frame, style='MenuSeparator.TFrame', height=1)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Menüeinträge erstellen
        for icon_text, command in menu_items:
            item_frame = ttk.Frame(main_frame, style='TVMenuItem.TFrame')
            item_frame.pack(fill=tk.X, pady=2)
            
            label = ttk.Label(item_frame,
                             text=icon_text,
                             style='TVMenuItem.TLabel',
                             cursor="hand2")
            label.pack(fill=tk.X, padx=25, pady=12)
            
            setup_hover_effects(item_frame, label)
            label.bind('<Button-1>', lambda e, cmd=command: cmd())
        
        # Animation zum Einblenden
        def animate_menu(current_x):
            if current_x < 0:
                current_x += 20
                app.menu_frame.place(x=current_x)
                app.root.after(10, lambda: animate_menu(current_x))
            else:
                app.menu_frame.place(x=0)
        
        animate_menu(-menu_width)
        
    except Exception as e:
        print(f"Fehler beim Erstellen des Menüs: {e}")

def close_menu_with_animation(app):
    """Schließt das Menü mit Animation"""
    try:
        if not hasattr(app, 'menu_frame') or not app.menu_frame.winfo_exists():
            if hasattr(app, 'menu_frame'):
                delattr(app, 'menu_frame')
            return
        
        menu_width = app.menu_frame.winfo_width()
        
        def animate_close(current_x):
            if current_x > -menu_width:
                current_x -= 20
                app.menu_frame.place(x=current_x)
                app.root.after(10, lambda: animate_close(current_x))
            else:
                app.menu_frame.destroy()
                delattr(app, 'menu_frame')
        
        animate_close(0)
        
    except Exception as e:
        print(f"Fehler beim Schließen des Menüs: {e}")

def create_filter_menu(app, parent_frame):
    """Erstellt die Filter & Sortierung Seite"""
    # Bestehende Filter-Seite schließen
    if hasattr(app, 'filter_frame'):
        app.filter_frame.destroy()
        delattr(app, 'filter_frame')
        return
    
    # Filter-Frame erstellen
    app.filter_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
    app.filter_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Header mit Zurück-Button
    header_frame = ttk.Frame(app.filter_frame, style='TVMenuHeader.TFrame')
    header_frame.pack(fill=tk.X, pady=(10, 20))
    
    # Zurück-Button
    back_btn = ttk.Label(header_frame,
                        text="←",
                        style='TVMenuTitle.TLabel',
                        cursor="hand2")
    back_btn.pack(side=tk.LEFT, padx=20)
    back_btn.bind('<Button-1>', lambda e: app.filter_frame.destroy())
    
    # Aktuelle Sprache
    lang = app.settings.get('language', 'de')
    texts = TRANSLATIONS[lang]['filters']
    
    # Titel
    ttk.Label(header_frame,
             text=texts['title'],
             style='TVMenuTitle.TLabel').pack(side=tk.LEFT, padx=20)
    
    # Content Frame
    content_frame = ttk.Frame(app.filter_frame, style='TVMenu.TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30)
    
    # Filter-Optionen
    filters = [
        ('all', texts['all'], app.show_all_todos),
        ('completed', texts['completed'], lambda: app.filter_todos('completed')),
        ('open', texts['open'], lambda: app.filter_todos('open')),
        ('important', texts['important'], lambda: app.filter_todos('high'))
    ]
    
    for filter_id, filter_name, filter_command in filters:
        filter_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
        filter_frame.pack(fill=tk.X, pady=2)
        
        # Filter-Label
        filter_label = ttk.Label(filter_frame,
                               text=filter_name,
                               style='TVMenuItem.TLabel',
                               cursor="hand2")
        filter_label.pack(side=tk.LEFT, padx=20, pady=12)
        
        # Click-Handler
        def apply_filter(cmd=filter_command):
            cmd()
            app.filter_frame.destroy()
        
        filter_label.bind('<Button-1>', lambda e, cmd=filter_command: apply_filter(cmd))
        setup_hover_effects(filter_frame, filter_label)
    
    # Separator
    ttk.Frame(content_frame,
             style='MenuSeparator.TFrame',
             height=1).pack(fill=tk.X, pady=20)
    
    # Sortier-Optionen
    ttk.Label(content_frame,
             text=texts['sort_by'],
             style='TVMenuTitle.TLabel').pack(anchor='w', pady=(0, 10))
    
    sorts = [
        ('priority', texts['sort_priority'], lambda: app.sort_todos('priority')),
        ('deadline', texts['sort_deadline'], lambda: app.sort_todos('deadline')),
        ('text', texts['sort_text'], lambda: app.sort_todos('text'))
    ]
    
    for sort_id, sort_name, sort_command in sorts:
        sort_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
        sort_frame.pack(fill=tk.X, pady=2)
        
        # Sort-Label
        sort_label = ttk.Label(sort_frame,
                             text=sort_name,
                             style='TVMenuItem.TLabel',
                             cursor="hand2")
        sort_label.pack(side=tk.LEFT, padx=20, pady=12)
        
        def apply_sort(cmd=sort_command):
            cmd()
            app.filter_frame.destroy()
        
        sort_label.bind('<Button-1>', lambda e, cmd=sort_command: apply_sort(cmd))
        setup_hover_effects(sort_frame, sort_label)

def create_notification_menu(app, parent_frame):
    """Erstellt die Benachrichtigungsseite"""
    # Bestehende Benachrichtigungsseite schließen
    if hasattr(app, 'notification_frame'):
        app.notification_frame.destroy()
        delattr(app, 'notification_frame')
        return
    
    # Benachrichtigungsframe erstellen
    app.notification_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
    app.notification_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Header mit Zurück-Button
    header_frame = ttk.Frame(app.notification_frame, style='TVMenuHeader.TFrame')
    header_frame.pack(fill=tk.X, pady=(10, 20))
    
    # Zurück-Button
    back_btn = ttk.Label(header_frame,
                        text="←",
                        style='TVMenuTitle.TLabel',
                        cursor="hand2")
    back_btn.pack(side=tk.LEFT, padx=20)
    back_btn.bind('<Button-1>', lambda e: app.notification_frame.destroy())
    
    # Aktuelle Sprache
    lang = app.settings.get('language', 'de')
    texts = TRANSLATIONS[lang]['notifications']
    
    # Titel
    ttk.Label(header_frame,
             text=texts['title'],
             style='TVMenuTitle.TLabel').pack(side=tk.LEFT, padx=20)
    
    # Content Frame
    content_frame = ttk.Frame(app.notification_frame, style='TVMenu.TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30)
    
    # Benachrichtigungen aktivieren/deaktivieren
    enabled = app.settings.get('notifications_enabled', True)
    toggle_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
    toggle_frame.pack(fill=tk.X, pady=10)
    
    toggle_label = ttk.Label(toggle_frame,
                           text=texts['enabled'] if enabled else texts['disabled'],
                           style='TVMenuItem.TLabel')
    toggle_label.pack(side=tk.LEFT)
    
    toggle_btn = ttk.Label(toggle_frame,
                         text="✓" if enabled else "✗",
                         style='TVMenuItem.TLabel',
                         cursor="hand2")
    toggle_btn.pack(side=tk.RIGHT)
    
    def toggle_notifications():
        nonlocal enabled
        enabled = not enabled
        app.settings['notifications_enabled'] = enabled
        app.save_settings()
        toggle_label.configure(text=texts['enabled'] if enabled else texts['disabled'])
        toggle_btn.configure(text="✓" if enabled else "✗")
    
    toggle_btn.bind('<Button-1>', lambda e: toggle_notifications())
    
    # Separator
    ttk.Frame(content_frame,
             style='MenuSeparator.TFrame',
             height=1).pack(fill=tk.X, pady=20)
    
    # Benachrichtigungstöne
    ttk.Label(content_frame,
             text=texts['sounds'],
             style='TVMenuTitle.TLabel').pack(anchor='w', pady=(0, 10))
    
    current_sound = app.settings.get('notification_sound', 'sound1')
    sounds = [
        ('sound1', texts['sound1']),
        ('sound2', texts['sound2']),
        ('sound3', texts['sound3'])
    ]
    
    for sound_id, sound_name in sounds:
        sound_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
        sound_frame.pack(fill=tk.X, pady=2)
        
        # Sound-Label
        sound_label = ttk.Label(sound_frame,
                              text=sound_name,
                              style='TVMenuItem.TLabel',
                              cursor="hand2")
        sound_label.pack(side=tk.LEFT, padx=20, pady=12)
        
        # Aktiv-Marker
        if sound_id == current_sound:
            ttk.Label(sound_frame,
                     text="✓",
                     style='TVMenuItem.TLabel').pack(side=tk.RIGHT, padx=20)
        
        def change_sound(sid=sound_id):
            app.settings['notification_sound'] = sid
            app.save_settings()
            app.play_notification_sound()  # Test-Sound abspielen
            app.notification_frame.destroy()
            create_notification_menu(app, parent_frame)
        
        sound_label.bind('<Button-1>', lambda e, sid=sound_id: change_sound(sid))
        setup_hover_effects(sound_frame, sound_label)
    
    # Separator
    ttk.Frame(content_frame,
             style='MenuSeparator.TFrame',
             height=1).pack(fill=tk.X, pady=20)
    
    # Test-Button
    test_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
    test_frame.pack(fill=tk.X, pady=10)
    
    test_label = ttk.Label(test_frame,
                          text=texts['test'],
                          style='TVMenuItem.TLabel',
                          cursor="hand2")
    test_label.pack(fill=tk.X, padx=20, pady=12)
    
    test_label.bind('<Button-1>', lambda e: app.play_notification_sound())
    setup_hover_effects(test_frame, test_label)

def create_language_menu(app, parent_frame):
    """Erstellt die Sprachauswahl-Seite"""
    # Bestehende Sprachauswahl-Seite schließen
    if hasattr(app, 'language_frame'):
        app.language_frame.destroy()
        delattr(app, 'language_frame')
        return
    
    # Sprachauswahl-Frame erstellen
    app.language_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
    app.language_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Header mit Zurück-Button
    header_frame = ttk.Frame(app.language_frame, style='TVMenuHeader.TFrame')
    header_frame.pack(fill=tk.X, pady=(10, 20))
    
    # Zurück-Button
    back_btn = ttk.Label(header_frame,
                        text="←",
                        style='TVMenuTitle.TLabel',
                        cursor="hand2")
    back_btn.pack(side=tk.LEFT, padx=20)
    back_btn.bind('<Button-1>', lambda e: app.language_frame.destroy())
    
    # Titel
    current_lang = app.settings.get('language', 'de')
    title_text = TRANSLATIONS[current_lang]['languages']['title']
    ttk.Label(header_frame,
             text=title_text,
             style='TVMenuTitle.TLabel').pack(side=tk.LEFT, padx=20)
    
    # Content Frame
    content_frame = ttk.Frame(app.language_frame, style='TVMenu.TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30)
    
    # Verfügbare Sprachen
    languages = [
        {
            'code': 'de',
            'name': 'Deutsch',
            'icon': '🇩🇪',
            'native': 'Deutsch'
        },
        {
            'code': 'en',
            'name': 'English',
            'icon': '🇬🇧',
            'native': 'English'
        }
    ]
    
    current_language = app.settings.get('language', 'de')
    
    for lang in languages:
        # Sprach-Container
        lang_container = ttk.Frame(content_frame, style='LanguageContainer.TFrame')
        lang_container.pack(fill=tk.X, pady=10)
        
        # Sprach-Frame
        lang_frame = ttk.Frame(lang_container, style='LanguageItem.TFrame')
        lang_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Sprach-Info
        info_frame = ttk.Frame(lang_frame, style='LanguageItem.TFrame')
        info_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Icon und Name
        ttk.Label(info_frame,
                 text=f"{lang['icon']} {lang['native']}",
                 style='TVMenuItem.TLabel').pack(side=tk.LEFT)
        
        # Aktiv-Marker
        if lang['code'] == current_language:
            ttk.Label(info_frame,
                     text="✓ " + TRANSLATIONS[current_lang]['languages']['current'],
                     style='LanguageActive.TLabel').pack(side=tk.RIGHT)
        
        # Click-Handler
        def apply_language(lang_code=lang['code']):
            app.change_language(lang_code)
            app.language_frame.destroy()
        
        # Hover-Effekte und Click-Handler
        lang_frame.bind('<Button-1>', lambda e, code=lang['code']: apply_language(code))
        
        def on_enter(e, frame=lang_frame):
            frame.configure(style='LanguageItemHover.TFrame')
            
        def on_leave(e, frame=lang_frame, is_current=lang['code']==current_language):
            frame.configure(style='LanguageItem.TFrame')
        
        lang_frame.bind('<Enter>', on_enter)
        lang_frame.bind('<Leave>', on_leave)

def create_theme_menu(app, parent_frame):
    """Erstellt die Theme-Auswahlseite"""
    # Bestehende Theme-Seite schließen
    if hasattr(app, 'theme_frame'):
        app.theme_frame.destroy()
        delattr(app, 'theme_frame')
        return
    
    # Theme-Frame erstellen
    app.theme_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
    app.theme_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Header mit Zurück-Button
    header_frame = ttk.Frame(app.theme_frame, style='TVMenuHeader.TFrame')
    header_frame.pack(fill=tk.X, pady=(10, 20))
    
    # Zurück-Button
    back_btn = ttk.Label(header_frame,
                        text="←",
                        style='TVMenuTitle.TLabel',
                        cursor="hand2")
    back_btn.pack(side=tk.LEFT, padx=20)
    back_btn.bind('<Button-1>', lambda e: app.theme_frame.destroy())
    
    # Titel
    ttk.Label(header_frame,
             text="Theme auswählen",
             style='TVMenuTitle.TLabel').pack(side=tk.LEFT, padx=20)
    
    # Content Frame
    content_frame = ttk.Frame(app.theme_frame, style='TVMenu.TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30)
    
    # Theme-Optionen
    themes = [
        {
            'name': 'Dark Mode',
            'id': 'dark',
            'icon': '🌙',
            'colors': {
                'primary': '#1a1a1a',
                'secondary': '#2d2d2d',
                'accent': '#007AFF'
            }
        },
        {
            'name': 'Light Mode',
            'id': 'light',
            'icon': '☀️',
            'colors': {
                'primary': '#ffffff',
                'secondary': '#f5f5f5',
                'accent': '#007AFF'
            }
        },
        {
            'name': 'Midnight Blue',
            'id': 'midnight',
            'icon': '🌃',
            'colors': {
                'primary': '#1a1b2e',
                'secondary': '#2d2d4d',
                'accent': '#6b8afd'
            }
        },
        {
            'name': 'Forest Green',
            'id': 'forest',
            'icon': '🌲',
            'colors': {
                'primary': '#1d2a1d',
                'secondary': '#2d3d2d',
                'accent': '#4caf50'
            }
        }
    ]
    
    current_theme = app.settings.get('theme', 'dark')
    
    for theme in themes:
        # Theme-Container
        theme_container = ttk.Frame(content_frame, style='ThemeContainer.TFrame')
        theme_container.pack(fill=tk.X, pady=10)
        
        # Preview-Frame
        preview_frame = ttk.Frame(theme_container, style=f'ThemePreview{theme["id"].capitalize()}.TFrame')
        preview_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Theme-Info
        info_frame = ttk.Frame(preview_frame, style=f'ThemePreview{theme["id"].capitalize()}.TFrame')
        info_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Icon und Name
        ttk.Label(info_frame,
                 text=f"{theme['icon']} {theme['name']}",
                 style='TVMenuItem.TLabel').pack(side=tk.LEFT)
        
        # Aktiv-Marker
        if theme['id'] == current_theme:
            ttk.Label(info_frame,
                     text="✓ Aktiv",
                     style='ThemeActive.TLabel').pack(side=tk.RIGHT)
        
        # Farbvorschau
        color_frame = ttk.Frame(preview_frame, style=f'ThemeColor{theme["id"].capitalize()}.TFrame')
        color_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        for color_name, color_value in theme['colors'].items():
            color_sample = ttk.Frame(color_frame, style=f'ThemeColor{theme["id"].capitalize()}.TFrame')
            color_sample.configure(width=30, height=20)
            color_sample.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(color_frame,
                     text=color_name.capitalize(),
                     style='ThemeColorLabel.TLabel').pack(side=tk.LEFT, padx=5)
        
        # Click-Handler
        def apply_theme(theme_id=theme['id']):
            app.change_theme(theme_id)
            app.theme_frame.destroy()
        
        # Hover-Effekte und Click-Handler
        preview_frame.bind('<Button-1>', lambda e, t=theme['id']: apply_theme(t))
        
        def on_enter(e, frame=preview_frame):
            frame.configure(style='ThemePreviewHover.TFrame')
            
        def on_leave(e, frame=preview_frame, theme_id=theme['id']):
            frame.configure(style=f'ThemePreview{theme_id.capitalize()}.TFrame')
        
        preview_frame.bind('<Enter>', on_enter)
        preview_frame.bind('<Leave>', on_leave)

def create_about_menu(app, parent_frame):
    """Erstellt die About-Seite"""
    # Bestehende About-Seite schließen
    if hasattr(app, 'about_frame'):
        app.about_frame.destroy()
        delattr(app, 'about_frame')
        return
    
    # About-Frame erstellen
    app.about_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
    app.about_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Header mit Zurück-Button
    header_frame = ttk.Frame(app.about_frame, style='TVMenuHeader.TFrame')
    header_frame.pack(fill=tk.X, pady=(10, 20))
    
    # Zurück-Button
    back_btn = ttk.Label(header_frame,
                        text="←",
                        style='TVMenuTitle.TLabel',
                        cursor="hand2")
    back_btn.pack(side=tk.LEFT, padx=20)
    back_btn.bind('<Button-1>', lambda e: app.about_frame.destroy())
    
    # Titel
    ttk.Label(header_frame,
             text="Über uns",
             style='TVMenuTitle.TLabel').pack(side=tk.LEFT, padx=20)
    
    # Content Frame
    content_frame = ttk.Frame(app.about_frame, style='TVMenu.TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30)
    
    # App Logo/Icon
    ttk.Label(content_frame,
             text="MY TODO",
             style='TVMenuTitle.TLabel').pack(pady=(0, 20))
    
    # Version
    ttk.Label(content_frame,
             text=f"Version {app.updater.current_version}",
             style='TVMenuItem.TLabel').pack(pady=(0, 30))
    
    # Team-Bereich
    team_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
    team_frame.pack(fill=tk.X, pady=20)
    
    ttk.Label(team_frame,
             text="👥 Entwickelt von",
             style='TVMenuTitle.TLabel').pack(anchor='w', pady=(0, 10))
    
    team_text = """
    MY TODO Team
    
    Kontakt:
    support@mytodo.app
    """
    
    ttk.Label(team_frame,
             text=team_text,
             style='TVMenuItem.TLabel',
             justify=tk.LEFT).pack(anchor='w', padx=20)
    
    # Copyright & Lizenz
    license_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
    license_frame.pack(fill=tk.X, pady=20)
    
    ttk.Label(license_frame,
             text="📄 Copyright & Lizenz",
             style='TVMenuTitle.TLabel').pack(anchor='w', pady=(0, 10))
    
    license_text = """
    MY TODO
    Copyright © 2024
    Alle Rechte vorbehalten.
    """
    
    ttk.Label(license_frame,
             text=license_text,
             style='TVMenuItem.TLabel',
             justify=tk.LEFT).pack(anchor='w', padx=20)

def create_help_menu(app, parent_frame):
    """Erstellt die Hilfe & Support Seite"""
    # Bestehende Hilfe-Seite schließen
    if hasattr(app, 'help_frame'):
        app.help_frame.destroy()
        delattr(app, 'help_frame')
        return
    
    # Hilfe-Frame erstellen
    app.help_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
    app.help_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Header mit Zurück-Button
    header_frame = ttk.Frame(app.help_frame, style='TVMenuHeader.TFrame')
    header_frame.pack(fill=tk.X, pady=(10, 20))
    
    # Zurück-Button
    back_btn = ttk.Label(header_frame,
                        text="←",
                        style='TVMenuTitle.TLabel',
                        cursor="hand2")
    back_btn.pack(side=tk.LEFT, padx=20)
    back_btn.bind('<Button-1>', lambda e: app.help_frame.destroy())
    
    # Aktuelle Sprache
    lang = app.settings.get('language', 'de')
    texts = TRANSLATIONS[lang]['help']
    
    # Titel
    ttk.Label(header_frame,
             text=texts['title'],
             style='TVMenuTitle.TLabel').pack(side=tk.LEFT, padx=20)
    
    # Content Frame
    content_frame = ttk.Frame(app.help_frame, style='TVMenu.TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30)
    
    # Anleitung
    ttk.Label(content_frame,
             text=texts['how_to'],
             style='TVMenuTitle.TLabel').pack(anchor='w', pady=(0, 10))
    
    # Hilfe-Einträge
    help_items = [
        texts['add_task'],
        texts['edit_task'],
        texts['complete_task'],
        texts['delete_task'],
        texts['filter_sort'],
        texts['drag_drop']
    ]
    
    for item in help_items:
        ttk.Label(content_frame,
                 text=item,
                 style='TVMenuItem.TLabel').pack(anchor='w', pady=5)
    
    # Separator
    ttk.Frame(content_frame,
             style='MenuSeparator.TFrame',
             height=1).pack(fill=tk.X, pady=20)
    
    # Kontakt
    ttk.Label(content_frame,
             text=texts['contact'],
             style='TVMenuTitle.TLabel').pack(anchor='w', pady=(10, 10))
    
    # Email (klickbar)
    email_label = ttk.Label(content_frame,
                           text=texts['email'],
                           style='TVMenuItem.TLabel',
                           cursor="hand2")
    email_label.pack(anchor='w', pady=5)
    email_label.bind('<Button-1>', lambda e: app.open_url(f"mailto:{texts['email']}"))
    
    # Website (klickbar)
    website_label = ttk.Label(content_frame,
                             text=texts['website'],
                             style='TVMenuItem.TLabel',
                             cursor="hand2")
    website_label.pack(anchor='w', pady=5)
    website_label.bind('<Button-1>', lambda e: app.open_url(f"https://{texts['website']}"))

# Hilfsfunktionen
def create_submenu(app, parent_frame):
    """Erstellt ein Untermenü innerhalb des Hauptmenüs"""
    if hasattr(app, 'submenu_frame'):
        app.submenu_frame.destroy()
    
    app.submenu_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
    submenu_width = 250
    
    # Positioniere Untermenü rechts neben dem Hauptmenü
    app.submenu_frame.place(
        x=parent_frame.winfo_width(),
        y=0,
        width=submenu_width,
        height=app.root.winfo_height()
    )
    
    return app.submenu_frame

def create_menu_items(items, submenu, parent_app):
    """Erstellt Menüeinträge mit einheitlichem Styling"""
    for icon_text, command in items:
        item_frame = ttk.Frame(submenu, style='TVMenuItem.TFrame')
        item_frame.pack(fill=tk.X, pady=2)
        
        label = ttk.Label(item_frame,
                         text=icon_text,
                         style='TVMenuItem.TLabel',
                         cursor="hand2")
        label.pack(fill=tk.X, padx=25, pady=12)
        
        setup_hover_effects(item_frame, label)
        label.bind('<Button-1>', lambda e, cmd=command: (cmd(), parent_app.root.destroy()))

def setup_hover_effects(frame, label):
    """Richtet die Hover-Effekte für Menüeinträge ein"""
    def on_enter(e):
        frame.configure(style='TVMenuItemHover.TFrame')
        label.configure(style='TVMenuItemHover.TLabel')
        
    def on_leave(e):
        frame.configure(style='TVMenuItem.TFrame')
        label.configure(style='TVMenuItem.TLabel')
    
    frame.bind('<Enter>', on_enter)
    frame.bind('<Leave>', on_leave)
    label.bind('<Enter>', on_enter)
    label.bind('<Leave>', on_leave)

# Hilfsdialoge
def show_help():
    messagebox.showinfo("Hilfe", 
        "MY TODO - Ihre Aufgabenverwaltung\n\n"
        "1. Aufgabe hinzufügen: + Button\n"
        "2. Aufgabe bearbeiten: Doppelklick\n"
        "3. Aufgabe erledigen: Checkbox\n"
        "4. Aufgabe löschen: X Button\n"
        "5. Filtern & Sortieren: Menü")

def show_version(app):
    messagebox.showinfo("Version", f"MY TODO v{app.updater.current_version}")

def show_team():
    messagebox.showinfo("Team", 
        "Entwickelt von:\n"
        "- Entwickler-Team\n\n"
        "Kontakt: support@mytodo.app")

def show_license():
    messagebox.showinfo("Lizenz", 
        "MY TODO\n"
        "Copyright © 2024\n\n"
        "Alle Rechte vorbehalten.")

def show_category_menu(app, event):
    """Zeigt das Kategorie-Menü"""
    menu = tk.Menu(app.root, tearoff=0)
    menu.configure(bg=app.colors['menu_bg'], fg=app.colors['menu_fg'])
    
    # "Alle anzeigen" Option
    menu.add_command(
        label="🔍 Alle anzeigen",
        command=app.show_all_todos
    )
    menu.add_separator()
    
    # Kategorien anzeigen
    for category in app.categories:
        count = app.count_todos_in_category(category)
        menu.add_command(
            label=f"{category} ({count})",
            command=lambda cat=category: app.filter_by_category(cat)
        )
    
    menu.add_separator()
    menu.add_command(
        label="+ Neue Kategorie",
        command=app.add_category
    )
    menu.add_command(
        label="- Kategorie entfernen",
        command=app.remove_category
    )
    
    # Menü an Button-Position anzeigen
    menu.post(event.widget.winfo_rootx(),
             event.widget.winfo_rooty() + event.widget.winfo_height())

def create_sort_menu(app, parent_menu, parent_frame):
    """Erstellt das Sortier-Untermenü mit Animation"""
    # Schließe bestehendes Untermenü
    if app.active_submenu:
        app.active_submenu.destroy()
    
    submenu = tk.Toplevel(app.root)
    app.active_submenu = submenu  # Speichere Referenz
    
    # Position berechnen (neben dem Hauptmenü)
    x = parent_menu.winfo_x() + parent_frame.winfo_width()
    y = parent_menu.winfo_y() + parent_frame.winfo_y()
    
    # Hauptframe
    main_frame = ttk.Frame(submenu, style='MenuModern.TFrame')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Sortieroptionen
    sort_items = [
        ("⬆️ Nach Priorität", lambda: app.sort_todos('priority')),
        ("⏰ Nach Deadline", lambda: app.sort_todos('deadline')),
        ("📝 Nach Text", lambda: app.sort_todos('text'))
    ]
    
    for icon_text, command in sort_items:
        item_frame = ttk.Frame(main_frame, style='MenuItemModern.TFrame')
        item_frame.pack(fill=tk.X, padx=2)
        
        label = ttk.Label(item_frame,
                         text=icon_text,
                         style='MenuItemModern.TLabel',
                         cursor="hand2")
        label.pack(fill=tk.X, padx=10, pady=8)
        
        # Hover-Effekte
        def on_enter(e, frame=item_frame):
            frame.configure(style='MenuItemHover.TFrame')
            
        def on_leave(e, frame=item_frame):
            frame.configure(style='MenuItemModern.TFrame')
        
        item_frame.bind('<Enter>', on_enter)
        item_frame.bind('<Leave>', on_leave)
        
        def execute_command(cmd=command):
            cmd()
            parent_menu.destroy()  # Hauptmenü schließen
        
        label.bind('<Button-1>', lambda e, cmd=command: execute_command(cmd))
    
    # Animation
    submenu_width = 200
    final_x = parent_menu.winfo_x() + parent_frame.winfo_width()
    y = parent_menu.winfo_y() + parent_frame.winfo_y()
    
    # Animation
    def animate_submenu(current_x, target_x):
        if current_x < target_x:
            current_x += 15
            submenu.geometry(f"{submenu_width}x300+{current_x}+{y}")
            submenu.after(10, lambda: animate_submenu(current_x, target_x))
        else:
            submenu.geometry(f"{submenu_width}x300+{target_x}+{y}")
    
    # Start-Position
    start_x = parent_menu.winfo_x() + parent_frame.winfo_width() - submenu_width
    submenu.geometry(f"{submenu_width}x300+{start_x}+{y}")
    
    # Animation starten
    animate_submenu(start_x, final_x)
    
    # Schließen wenn außerhalb geklickt
    def on_submenu_click_outside(event):
        if not submenu.winfo_containing(event.x_root, event.y_root):
            submenu.destroy()
            app.active_submenu = None
    
    submenu.bind('<Button-1>', on_submenu_click_outside)

# Styles für das moderne Menü in app/gui/styles.py hinzufügen:
def setup_menu_styles(app):
    """Richtet die Styles für das moderne Menü ein"""
    styles = {
        'MenuModern.TFrame': {
            'configure': {
                'background': app.colors['menu_bg'],
                'relief': 'flat'
            }
        },
        'MenuHeaderModern.TFrame': {
            'configure': {
                'background': app.colors['menu_bg'],
                'relief': 'flat'
            }
        },
        'MenuHeaderModern.TLabel': {
            'configure': {
                'background': app.colors['menu_bg'],
                'foreground': app.colors['menu_fg'],
                'font': ('Segoe UI', 10, 'bold')
            }
        },
        'MenuCloseModern.TLabel': {
            'configure': {
                'background': app.colors['menu_bg'],
                'foreground': app.colors['menu_fg'],
                'font': ('Segoe UI', 16),
                'padding': 2
            }
        },
        'MenuItemModern.TFrame': {
            'configure': {
                'background': app.colors['menu_bg'],
                'relief': 'flat'
            }
        },
        'MenuItemModern.TLabel': {
            'configure': {
                'background': app.colors['menu_bg'],
                'foreground': app.colors['menu_fg'],
                'font': ('Segoe UI', 10),
                'padding': (5, 2)
            }
        },
        'MenuItemHover.TFrame': {
            'configure': {
                'background': app.colors['bg_hover'],
                'relief': 'flat'
            }
        },
        'MenuSeparator.TFrame': {
            'configure': {
                'background': app.colors['border'],
                'height': 1
            }
        },
        'ThemeContainer.TFrame': {
            'configure': {
                'background': app.colors['menu_bg'],
                'relief': 'flat'
            }
        },
        'ThemePreviewDark.TFrame': {
            'configure': {
                'background': '#1a1a1a'
            }
        },
        'ThemePreviewLight.TFrame': {
            'configure': {
                'background': '#ffffff'
            }
        },
        'ThemePreviewMidnight.TFrame': {
            'configure': {
                'background': '#1a1b2e'
            }
        },
        'ThemePreviewForest.TFrame': {
            'configure': {
                'background': '#1d2a1d'
            }
        },
        'ThemePreviewHover.TFrame': {
            'configure': {
                'background': app.colors['bg_hover']
            }
        },
        'ThemeActive.TLabel': {
            'configure': {
                'background': app.colors['accent'],
                'foreground': app.colors['menu_fg'],
                'font': ('Segoe UI', 10, 'bold')
            }
        },
        'ThemeColor.TFrame': {
            'configure': {
                'background': app.colors['menu_bg'],
                'relief': 'flat'
            }
        },
        'ThemeColorLabel.TLabel': {
            'configure': {
                'background': app.colors['menu_fg'],
                'foreground': app.colors['menu_bg'],
                'font': ('Segoe UI', 10)
            }
        },
        'LanguageContainer.TFrame': {
            'configure': {
                'background': app.colors['menu_bg'],
                'relief': 'flat'
            }
        },
        'LanguageItem.TFrame': {
            'configure': {
                'background': app.colors['menu_bg'],
                'relief': 'flat'
            }
        },
        'LanguageItemHover.TFrame': {
            'configure': {
                'background': app.colors['bg_hover'],
                'relief': 'flat'
            }
        },
        'LanguageActive.TLabel': {
            'configure': {
                'background': app.colors['accent'],
                'foreground': app.colors['menu_fg'],
                'font': ('Segoe UI', 10, 'bold')
            }
        }
    }
    
    return styles 

def create_settings_menu(app, parent_frame):
    """Erstellt die Einstellungsseite"""
    # Bestehende Einstellungsseite schließen
    if hasattr(app, 'settings_frame'):
        app.settings_frame.destroy()
        delattr(app, 'settings_frame')
        return
    
    # Settings-Frame erstellen
    app.settings_frame = ttk.Frame(app.root, style='TVMenu.TFrame')
    app.settings_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Header mit Zurück-Button
    header_frame = ttk.Frame(app.settings_frame, style='TVMenuHeader.TFrame')
    header_frame.pack(fill=tk.X, pady=(10, 20))
    
    # Aktuelle Sprache
    lang = app.settings.get('language', 'de')
    texts = TRANSLATIONS[lang]['settings']
    
    # Zurück-Button
    back_btn = ttk.Label(header_frame,
                        text="←",
                        style='TVMenuTitle.TLabel',
                        cursor="hand2")
    back_btn.pack(side=tk.LEFT, padx=20)
    back_btn.bind('<Button-1>', lambda e: app.settings_frame.destroy())
    
    # Titel
    ttk.Label(header_frame,
             text=texts['title'],
             style='TVMenuTitle.TLabel').pack(side=tk.LEFT, padx=20)
    
    # Content Frame
    content_frame = ttk.Frame(app.settings_frame, style='TVMenu.TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30)
    
    # Fensterposition
    position_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
    position_frame.pack(fill=tk.X, pady=10)
    
    ttk.Label(position_frame,
             text=texts['window_position'],
             style='TVMenuTitle.TLabel').pack(anchor='w', pady=(0, 10))
    
    positions = [
        ('tl', texts['positions']['tl']),
        ('tr', texts['positions']['tr']),
        ('bl', texts['positions']['bl']),
        ('br', texts['positions']['br'])
    ]
    
    current_pos = app.settings.get('window_position', 'br')
    
    for pos_id, pos_name in positions:
        pos_frame = ttk.Frame(position_frame, style='TVMenuItem.TFrame')
        pos_frame.pack(fill=tk.X, pady=2)
        
        # Position-Label
        pos_label = ttk.Label(pos_frame,
                            text=pos_name,
                            style='TVMenuItem.TLabel',
                            cursor="hand2")
        pos_label.pack(side=tk.LEFT, padx=20, pady=12)
        
        # Aktiv-Marker
        if pos_id == current_pos:
            ttk.Label(pos_frame,
                     text="✓",
                     style='TVMenuItem.TLabel').pack(side=tk.RIGHT, padx=20)
        
        def change_position(pid=pos_id):
            app.settings['window_position'] = pid
            app.save_settings()
            app.apply_window_position(pid)
            app.settings_frame.destroy()
            create_settings_menu(app, parent_frame)
        
        pos_label.bind('<Button-1>', lambda e, pid=pos_id: change_position(pid))
        setup_hover_effects(pos_frame, pos_label)
    
    # Separator
    ttk.Frame(content_frame,
             style='MenuSeparator.TFrame',
             height=1).pack(fill=tk.X, pady=20)
    
    # Fenstergröße
    size_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
    size_frame.pack(fill=tk.X, pady=10)
    
    ttk.Label(size_frame,
             text=texts['window_size'],
             style='TVMenuTitle.TLabel').pack(anchor='w', pady=(0, 10))
    
    # Größen-Eingabe
    input_frame = ttk.Frame(size_frame, style='TVMenuItem.TFrame')
    input_frame.pack(fill=tk.X, padx=20, pady=5)
    
    # Breite
    ttk.Label(input_frame,
             text=texts['width'],
             style='TVMenuItem.TLabel').pack(side=tk.LEFT)
    
    width_var = tk.StringVar(value=str(app.window_width))
    width_entry = ttk.Entry(input_frame,
                          textvariable=width_var,
                          width=5,
                          style='Settings.TEntry')
    width_entry.pack(side=tk.LEFT, padx=10)
    
    # Höhe
    ttk.Label(input_frame,
             text=texts['height'],
             style='TVMenuItem.TLabel').pack(side=tk.LEFT, padx=(20, 0))
    
    height_var = tk.StringVar(value=str(app.window_height))
    height_entry = ttk.Entry(input_frame,
                           textvariable=height_var,
                           width=5,
                           style='Settings.TEntry')
    height_entry.pack(side=tk.LEFT, padx=10)
    
    # Speichern-Button
    save_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
    save_frame.pack(fill=tk.X, pady=20)
    
    save_btn = ttk.Label(save_frame,
                        text=texts['save'],
                        style='TVMenuItem.TLabel',
                        cursor="hand2")
    save_btn.pack(anchor='e', padx=20, pady=10)
    
    def save_settings():
        try:
            # Größe speichern
            width = int(width_var.get())
            height = int(height_var.get())
            if width >= 200 and height >= 300:  # Minimale Größe
                app.settings['window_size'] = f"{width},{height}"
                app.window_width = width
                app.window_height = height
                app.root.geometry(f"{width}x{height}")
                app.save_settings()
                app.settings_frame.destroy()
        except ValueError:
            pass
    
    save_btn.bind('<Button-1>', lambda e: save_settings())
    setup_hover_effects(save_frame, save_btn)
    
    # Autostart-Option
    autostart_frame = ttk.Frame(content_frame, style='TVMenuItem.TFrame')
    autostart_frame.pack(fill=tk.X, pady=10)
    
    # Autostart Label und Status
    autostart_label = ttk.Label(autostart_frame,
                              text="Mit Windows starten",
                              style='TVMenuItem.TLabel')
    autostart_label.pack(side=tk.LEFT, padx=20, pady=12)
    
    # Status-Label (✓ oder ✗)
    status_label = ttk.Label(autostart_frame,
                           text="✓" if app.is_autostart_enabled() else "✗",
                           style='TVMenuItem.TLabel')
    status_label.pack(side=tk.RIGHT, padx=20)
    
    def toggle_autostart_status():
        if app.toggle_autostart():
            # GUI aktualisieren
            status_label.configure(text="✓" if app.is_autostart_enabled() else "✗")
    
    # Klick-Handler
    autostart_frame.bind('<Button-1>', lambda e: toggle_autostart_status())
    autostart_label.bind('<Button-1>', lambda e: toggle_autostart_status())
    status_label.bind('<Button-1>', lambda e: toggle_autostart_status())
    
    # Hover-Effekte
    setup_hover_effects(autostart_frame, autostart_label) 