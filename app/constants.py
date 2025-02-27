# Farben und andere Konstanten
COLORS = {
    'dark': {
        'bg': '#1a1a1a',
        'bg_secondary': '#2d2d2d',
        'bg_hover': '#3d3d3d',
        'bg_input': '#ffffff',
        'fg': '#ffffff',
        'fg_secondary': '#888888',
        'fg_tertiary': '#555555',
        'accent': '#007AFF',
        'border': '#333333',
        'error': '#ff3b30',
        'menu_bg': '#1a1a1a',
        'menu_fg': '#ffffff',
        'high_priority': '#ff3b30',    # Rot
        'medium_priority': '#ffcc00',   # Gelb
        'low_priority': '#34c759'       # Grün
    },
    'light': {
        'bg': '#ffffff',
        'bg_secondary': '#f5f5f5',
        'bg_hover': '#e5e5e5',
        'bg_input': '#ffffff',
        'fg': '#000000',
        'fg_secondary': '#666666',
        'fg_tertiary': '#999999',
        'accent': '#007AFF',
        'border': '#dddddd',
        'error': '#ff3b30',
        'menu_bg': '#ffffff',
        'menu_fg': '#000000',
        'high_priority': '#ff3b30',
        'medium_priority': '#ffcc00',
        'low_priority': '#34c759'
    },
    'midnight': {
        'bg': '#1a1b2e',
        'bg_secondary': '#2d2d4d',
        'bg_hover': '#3d3d6d',
        'bg_input': '#ffffff',
        'fg': '#ffffff',
        'fg_secondary': '#8888aa',
        'fg_tertiary': '#555577',
        'accent': '#6b8afd',
        'border': '#333355',
        'error': '#ff4444',
        'menu_bg': '#1a1b2e',
        'menu_fg': '#ffffff',
        'high_priority': '#ff4444',
        'medium_priority': '#ffcc44',
        'low_priority': '#44cc88'
    },
    'forest': {
        'bg': '#1d2a1d',
        'bg_secondary': '#2d3d2d',
        'bg_hover': '#3d4d3d',
        'bg_input': '#ffffff',
        'fg': '#ffffff',
        'fg_secondary': '#88aa88',
        'fg_tertiary': '#557755',
        'accent': '#4caf50',
        'border': '#335533',
        'error': '#ff5544',
        'menu_bg': '#1d2a1d',
        'menu_fg': '#ffffff',
        'high_priority': '#ff5544',
        'medium_priority': '#ffdd44',
        'low_priority': '#4caf50'
    }
}

# Fügen Sie dies zur constants.py hinzu
TRANSLATIONS = {
    'de': {
        'app_name': 'MY TODO',
        'menu': {
            'home': '🏠 Startseite',
            'settings': '👤 Einstellungen',
            'filter': '📋 Filter',
            'notifications': '🔔 Benachrichtigungen',
            'language': '🌐 Sprache',
            'theme': '🎨 Design',
            'updates': '⚡ Updates',
            'about': 'ℹ️ Über uns',
            'help': '❓ Hilfe & Support'
        },
        'filters': {
            'title': 'Filter & Sortierung',
            'all': '📋 Alle Aufgaben',
            'completed': '✅ Erledigt',
            'open': '⏳ Offen',
            'important': '⭐ Wichtig',
            'by_date': '📅 Nach Datum',
            'by_category': '🏷️ Nach Kategorie',
            'sort_by': 'Sortieren nach:',
            'sort_priority': '⬆️ Priorität',
            'sort_deadline': '⏰ Deadline',
            'sort_text': '📝 Text',
            'categories': 'Kategorien:',
            'add_category': '+ Neue Kategorie',
            'remove_category': '- Kategorie entfernen'
        },
        'languages': {
            'title': 'Sprache auswählen',
            'current': 'Aktuelle Sprache',
            'german': 'Deutsch',
            'english': 'Englisch'
        },
        'help': {
            'title': 'Hilfe & Support',
            'how_to': 'So funktioniert\'s:',
            'add_task': '• Neue Aufgabe: + Button',
            'edit_task': '• Aufgabe bearbeiten: Doppelklick',
            'complete_task': '• Aufgabe erledigen: Checkbox',
            'delete_task': '• Aufgabe löschen: X Button',
            'filter_sort': '• Sortieren & Filtern: Menü',
            'drag_drop': '• Drag & Drop: Aufgaben verschieben',
            'contact': 'Kontakt & Support:',
            'email': 'support@mytodo.app',
            'website': 'www.mytodo.app'
        },
        'notifications': {
            'title': 'Benachrichtigungen',
            'sounds': 'Benachrichtigungstöne:',
            'sound1': '🔊 Standard',
            'sound2': '🔔 Glocke',
            'sound3': '📱 Handy',
            'test': 'Test-Benachrichtigung',
            'volume': 'Lautstärke:',
            'enabled': 'Benachrichtigungen aktiviert',
            'disabled': 'Benachrichtigungen deaktiviert'
        },
        'settings': {
            'title': 'Einstellungen',
            'window_position': 'Fensterposition:',
            'window_size': 'Fenstergröße:',
            'width': 'Breite:',
            'height': 'Höhe:',
            'save': 'Speichern',
            'positions': {
                'tl': '↖️ Oben Links',
                'tr': '↗️ Oben Rechts',
                'bl': '↙️ Unten Links',
                'br': '↘️ Unten Rechts'
            }
        }
    },
    'en': {
        'app_name': 'MY TODO',
        'menu': {
            'home': '🏠 Home',
            'settings': '👤 Settings',
            'filter': '📋 Filter',
            'notifications': '🔔 Notifications',
            'language': '🌐 Language',
            'theme': '🎨 Theme',
            'updates': '⚡ Updates',
            'about': 'ℹ️ About',
            'help': '❓ Help & Support'
        },
        'filters': {
            'title': 'Filter & Sort',
            'all': '📋 All Tasks',
            'completed': '✅ Completed',
            'open': '⏳ Open',
            'important': '⭐ Important',
            'by_date': '📅 By Date',
            'by_category': '🏷️ By Category',
            'sort_by': 'Sort by:',
            'sort_priority': '⬆️ Priority',
            'sort_deadline': '⏰ Deadline',
            'sort_text': '📝 Text',
            'categories': 'Categories:',
            'add_category': '+ Add Category',
            'remove_category': '- Remove Category'
        },
        'languages': {
            'title': 'Select Language',
            'current': 'Current Language',
            'german': 'German',
            'english': 'English'
        },
        'help': {
            'title': 'Help & Support',
            'how_to': 'How to use:',
            'add_task': '• New task: + Button',
            'edit_task': '• Edit task: Double click',
            'complete_task': '• Complete task: Checkbox',
            'delete_task': '• Delete task: X Button',
            'filter_sort': '• Sort & Filter: Menu',
            'drag_drop': '• Drag & Drop: Move tasks',
            'contact': 'Contact & Support:',
            'email': 'support@mytodo.app',
            'website': 'www.mytodo.app'
        },
        'notifications': {
            'title': 'Notifications',
            'sounds': 'Notification sounds:',
            'sound1': '🔊 Standard',
            'sound2': '🔔 Bell',
            'sound3': '📱 Mobile',
            'test': 'Test notification',
            'volume': 'Volume:',
            'enabled': 'Notifications enabled',
            'disabled': 'Notifications disabled'
        },
        'settings': {
            'title': 'Settings',
            'window_position': 'Window Position:',
            'window_size': 'Window Size:',
            'width': 'Width:',
            'height': 'Height:',
            'save': 'Save',
            'positions': {
                'tl': '↖️ Top Left',
                'tr': '↗️ Top Right',
                'bl': '↙️ Bottom Left',
                'br': '↘️ Bottom Right'
            }
        }
    }
} 