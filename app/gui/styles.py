from tkinter import ttk
from app.gui.menu import setup_menu_styles

def setup_styles(app):
    """Konfiguriert die Styles für die Anwendung"""
    style = ttk.Style()
    
    # Basis-Theme auf dunkel setzen
    style.configure('.',  # Der Punkt bedeutet "alle Widgets"
                   background=app.colors['bg'],
                   foreground=app.colors['fg'])
    
    # Frame Styles
    style.configure('Dark.TFrame', 
                   background=app.colors['bg'])
    
    # Kategorie-Header Style
    style.configure('Category.TFrame', 
                   background=app.colors['bg'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('Category.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Arial', 14))
    
    # Todo Container und Dropzone Styles
    style.configure('DropZone.TFrame',
                   background=app.colors['bg'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('DropZoneHighlight.TFrame',
                   background=app.colors['bg_hover'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('TodoContainer.TFrame', 
                   background=app.colors['bg'],
                   padding=5)
    
    # Moderne Frame Styles
    style.configure('TodoModern.TFrame',
                   background=app.colors['bg'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('TodoModernHover.TFrame',
                   background=app.colors['bg_hover'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('TodoInner.TFrame',
                   background=app.colors['bg'])
    
    # Label Styles
    style.configure('Title.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Arial', 12, 'bold'))
    
    style.configure('TodoText.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Arial', 11))
    
    style.configure('Close.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Arial', 14))
    
    style.configure('Menu.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Arial', 16))
    
    style.configure('Add.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Arial', 16))
    
    style.configure('Search.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_secondary'],
                   font=('Arial', 12))
    
    style.configure('DragHandle.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_secondary'],
                   font=('Arial', 16, 'bold'))
    
    style.configure('Priority.TLabel',
                   background=app.colors['bg'],
                   font=('Arial', 12, 'bold'))
    
    style.configure('TodoInfo.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_secondary'],
                   font=('Arial', 9))
    
    # Entry Style
    style.configure('Search.TEntry',
                   fieldbackground=app.colors['bg_input'],
                   foreground='black',
                   insertcolor='black')
    
    # Entry Styles
    style.configure('TodoEntry.TEntry',
                   fieldbackground=app.colors['bg_secondary'],
                   foreground='black',
                   insertcolor='black',
                   borderwidth=1,
                   relief='solid')
    
    # Button Style
    style.configure('Primary.TButton',
                   background=app.colors['accent'],
                   foreground=app.colors['fg'])
    
    # Menü Styles
    style.configure('Menu.TFrame',
                   background=app.colors['bg'])
    
    style.configure('MenuHeader.TFrame',
                   background=app.colors['bg'])
    
    style.configure('MenuItem.TFrame',
                   background=app.colors['bg'])
    
    style.configure('SubMenu.TFrame',
                   background=app.colors['bg'])
    
    style.configure('MenuItem.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Arial', 11))
    
    style.configure('MenuClose.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Arial', 16))
    
    # Combobox Styles
    style.configure('TodoCombobox.TCombobox',
                   fieldbackground=app.colors['bg_secondary'],
                   background=app.colors['bg_secondary'],
                   foreground='black',
                   arrowcolor='black',
                   selectbackground=app.colors['bg_hover'],
                   selectforeground='black')
    
    # Radiobutton Styles
    style.configure('TodoRadio.TRadiobutton',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   indicatorcolor=app.colors['accent'])
    
    style.map('TodoRadio.TRadiobutton',
              background=[('active', app.colors['bg_hover'])],
              foreground=[('active', app.colors['fg'])])
    
    # Button Styles
    style.configure('TodoButton.TButton',
                   background=app.colors['bg_secondary'],
                   foreground='black',
                   padding=(10, 5),
                   relief='flat',
                   borderwidth=0)
    
    style.map('TodoButton.TButton',
              background=[('active', app.colors['bg_hover']),
                        ('pressed', app.colors['bg_hover'])],
              foreground=[('active', 'black'),
                        ('pressed', 'black')])
    
    # Moderne Frame Styles
    style.configure('TodoModern.TFrame',
                   background=app.colors['bg'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('TodoModernHover.TFrame',
                   background=app.colors['bg_hover'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('TodoInner.TFrame',
                   background=app.colors['bg'])
    
    style.configure('MetaBadge.TFrame',
                   background=app.colors['bg_secondary'],
                   relief='flat',
                   borderwidth=0)
    
    # Moderne Label Styles
    style.configure('TodoTextModern.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Segoe UI', 11))
    
    style.configure('TodoTextCompleted.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_secondary'],
                   font=('Segoe UI', 11),
                   overstrike=1)
    
    style.configure('DragHandleModern.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_tertiary'],
                   font=('Segoe UI', 16, 'bold'))
    
    style.configure('DragHandleHover.TLabel',
                   background=app.colors['bg_hover'],
                   foreground=app.colors['accent'],
                   font=('Segoe UI', 16, 'bold'))
    
    style.configure('PriorityDot.TLabel',
                   background=app.colors['bg'],
                   font=('Segoe UI', 14))
    
    style.configure('MetaIcon.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_secondary'],
                   font=('Segoe UI', 9))
    
    style.configure('MetaIconAlert.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['error'],
                   font=('Segoe UI', 9))
    
    style.configure('MetaText.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_secondary'],
                   font=('Segoe UI', 9))
    
    # Checkbox Style
    style.configure('TodoCheckbox.TCheckbutton',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   indicatorcolor=app.colors['accent'])
    
    style.map('TodoCheckbox.TCheckbutton',
              background=[('active', app.colors['bg_hover'])],
              foreground=[('active', app.colors['fg'])],
              indicatorcolor=[('selected', app.colors['accent']),
                            ('!selected', app.colors['fg_secondary'])])
    
    # Löschen-Button Styles
    style.configure('TodoDelete.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_secondary'],
                   font=('Segoe UI', 16, 'bold'))
    
    style.configure('TodoDeleteHover.TLabel',
                   background=app.colors['bg_hover'],
                   foreground=app.colors['error'],
                   font=('Segoe UI', 16, 'bold'))
    
    # Messagebox Style
    style.configure('Dialog.TFrame',
                   background=app.colors['bg'])
    
    # Dialog Button Style
    style.configure('Dialog.TButton',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   padding=(10, 5))
    
    style.map('Dialog.TButton',
              background=[('active', app.colors['bg_hover'])])
    
    # Kategorie Header Styles
    style.configure('CategoryHeader.TFrame',
                   background=app.colors['bg_secondary'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('CategoryExpand.TLabel',
                   background=app.colors['bg_secondary'],
                   foreground=app.colors['fg_secondary'],
                   font=('Segoe UI', 8))  # Kleinere Schrift
    
    style.configure('CategoryTitle.TLabel',
                   background=app.colors['bg_secondary'],
                   foreground=app.colors['fg'],
                   font=('Segoe UI', 9, 'bold'))  # Kleinere, fette Schrift
    
    # Prioritäts-spezifische Styles für Deadlines
    style.configure('DeadlineHigh.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['high_priority'],  # Rot für hohe Priorität
                   font=('Segoe UI', 9))
    
    style.configure('DeadlineMedium.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['medium_priority'],  # Gelb für mittlere Priorität
                   font=('Segoe UI', 9))
    
    style.configure('DeadlineLow.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['low_priority'],  # Grün für niedrige Priorität
                   font=('Segoe UI', 9))
    
    # Moderne Menü-Styles
    style.configure('MenuModern.TFrame',
                   background=app.colors['bg_secondary'],
                   relief='solid',
                   borderwidth=1)
    
    style.configure('MenuHeaderModern.TFrame',
                   background=app.colors['bg_secondary'])
    
    style.configure('MenuHeaderModern.TLabel',
                   background=app.colors['bg_secondary'],
                   foreground=app.colors['fg'],
                   font=('Segoe UI', 10, 'bold'))
    
    style.configure('MenuCloseModern.TLabel',
                   background=app.colors['bg_secondary'],
                   foreground=app.colors['fg_secondary'],
                   font=('Segoe UI', 16))
    
    style.configure('MenuItemModern.TFrame',
                   background=app.colors['bg_secondary'])
    
    style.configure('MenuItemModern.TLabel',
                   background=app.colors['bg_secondary'],
                   foreground=app.colors['fg'],
                   font=('Segoe UI', 10))
    
    style.configure('MenuItemHover.TFrame',
                   background=app.colors['bg_hover'])
    
    style.configure('MenuSeparator.TFrame',
                   background=app.colors['fg_tertiary'],
                   height=1)
    
    # Einstellungs-Styles
    style.configure('Settings.TFrame',
                   background=app.colors['bg'])
    
    style.configure('SettingsItem.TFrame',
                   background=app.colors['bg_secondary'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('SettingsItemHover.TFrame',
                   background=app.colors['bg_hover'],
                   relief='flat',
                   borderwidth=0)
    
    style.configure('SettingsLabel.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Segoe UI', 10))
    
    style.configure('SettingsRadio.TRadiobutton',
                   background=app.colors['bg_secondary'],
                   foreground=app.colors['fg'],
                   font=('Segoe UI', 10))
    
    style.map('SettingsRadio.TRadiobutton',
             background=[('active', app.colors['bg_hover'])])
    
    style.configure('SettingsSeparator.TFrame',
                   background=app.colors['fg_tertiary'],
                   height=1)
    
    style.configure('SettingsButton.TButton',
                   background=app.colors['bg_secondary'],
                   foreground=app.colors['fg'],
                   padding=(10, 5))
    
    style.map('SettingsButton.TButton',
             background=[('active', app.colors['bg_hover'])])
    
    # Menü-Styles hinzufügen
    styles = setup_menu_styles(app)
    
    # Styles anwenden... 

    style.configure('MenuToggle.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg'],
                   font=('Segoe UI', 16))

    # Theme-Preview Styles
    style.configure('ThemeContainer.TFrame',
                   background=app.colors['bg'])

    style.configure('ThemePreviewDark.TFrame',
                   background='#1a1a1a',
                   relief='solid',
                   borderwidth=1)

    style.configure('ThemePreviewLight.TFrame',
                   background='#ffffff',
                   relief='solid',
                   borderwidth=1)

    style.configure('ThemePreviewMidnight.TFrame',
                   background='#1a1b2e',
                   relief='solid',
                   borderwidth=1)

    style.configure('ThemePreviewForest.TFrame',
                   background='#1d2a1d',
                   relief='solid',
                   borderwidth=1)

    style.configure('ThemePreviewHover.TFrame',
                   background=app.colors['bg_hover'],
                   relief='solid',
                   borderwidth=2)

    style.configure('ThemeActive.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['accent'],
                   font=('Segoe UI', 10))

    style.configure('ThemeColorLabel.TLabel',
                   background=app.colors['bg'],
                   foreground=app.colors['fg_secondary'],
                   font=('Segoe UI', 9))

    # Theme-spezifische Farb-Samples
    for theme_id in ['Dark', 'Light', 'Midnight', 'Forest']:
        style.configure(f'ThemeColor{theme_id}.TFrame',
                       relief='solid',
                       borderwidth=1)

    # Sprach-Auswahl Styles
    style.configure('LanguageContainer.TFrame',
                   background=app.colors['bg'])

    style.configure('LanguageItem.TFrame',
                   background=app.colors['bg_secondary'],
                   relief='solid',
                   borderwidth=1)

    style.configure('LanguageItemHover.TFrame',
                   background=app.colors['bg_hover'],
                   relief='solid',
                   borderwidth=2)

    style.configure('LanguageActive.TLabel',
                   background=app.colors['bg_secondary'],
                   foreground=app.colors['accent'],
                   font=('Segoe UI', 10))

def setup_menu_styles(app):
    """TV-ähnliche Menü-Styles"""
    styles = {
        'TVMenu.TFrame': {
            'configure': {
                'background': '#1a1a1a',  # Dunklerer Hintergrund
                'relief': 'flat'
            }
        },
        'TVMenuHeader.TFrame': {
            'configure': {
                'background': '#1a1a1a'
            }
        },
        'TVMenuTitle.TLabel': {
            'configure': {
                'background': '#1a1a1a',
                'foreground': '#ffffff',
                'font': ('Segoe UI', 24, 'bold')  # Größere Schrift
            }
        },
        'TVMenuItem.TFrame': {
            'configure': {
                'background': '#1a1a1a'
            }
        },
        'TVMenuItem.TLabel': {
            'configure': {
                'background': '#1a1a1a',
                'foreground': '#ffffff',
                'font': ('Segoe UI', 14),  # Größere Schrift
                'padding': (10, 8)
            }
        },
        'TVMenuItemHover.TFrame': {
            'configure': {
                'background': '#2d2d2d'  # Hellerer Hover-Effekt
            }
        },
        'TVMenuItemHover.TLabel': {
            'configure': {
                'background': '#2d2d2d',
                'foreground': '#ffffff',
                'font': ('Segoe UI', 14)
            }
        }
    }
    return styles 