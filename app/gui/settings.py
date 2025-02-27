import os
import tkinter as tk
from tkinter import ttk
import winreg
import sys

def show_settings(app):
    """Zeigt den Einstellungsdialog"""
    dialog, main_frame = app.create_dialog("Einstellungen", width=300)
    
    # Theme-Auswahl
    theme_frame = ttk.Frame(main_frame, style='Settings.TFrame')
    theme_frame.pack(fill=tk.X, pady=(0, 20))
    
    ttk.Label(theme_frame,
             text="Theme:",
             style='SettingsLabel.TLabel').pack(side=tk.LEFT, padx=(0, 10))
    
    # Theme Variable mit aktuellem Wert
    theme_var = tk.StringVar()
    
    # Theme-Buttons Frame
    theme_buttons_frame = ttk.Frame(theme_frame, style='Settings.TFrame')
    theme_buttons_frame.pack(side=tk.LEFT)
    
    def on_theme_change():
        app.change_theme(theme_var.get())
    
    # Theme-Buttons
    themes = [('dark', 'Dunkel', '🌙'), ('light', 'Hell', '☀️')]
    for theme, text, icon in themes:
        rb = ttk.Radiobutton(theme_buttons_frame,
                           text=f"{icon} {text}",
                           value=theme,
                           variable=theme_var,
                           style='SettingsRadio.TRadiobutton',
                           command=on_theme_change)
        rb.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Trennlinie
    separator = ttk.Frame(main_frame, style='SettingsSeparator.TFrame')
    separator.pack(fill=tk.X, padx=5, pady=10)
    
    # Position
    position_frame = ttk.Frame(main_frame, style='Settings.TFrame')
    position_frame.pack(fill=tk.X, pady=(0, 10))
    
    ttk.Label(position_frame,
             text="Fensterposition:",
             style='SettingsLabel.TLabel').pack(anchor="w", pady=(0, 5))
    
    # Position Variable mit aktuellem Wert
    position_var = tk.StringVar()
    
    def on_position_change():
        pos = position_var.get()
        app.apply_window_position(pos)
        app.save_settings({'window_position': pos})
    
    # Position-Buttons
    positions = [
        ('tl', '↖️ Oben Links'),
        ('tr', '↗️ Oben Rechts'),
        ('bl', '↙️ Unten Links'),
        ('br', '↘️ Unten Rechts')
    ]
    
    for pos, text in positions:
        rb = ttk.Radiobutton(position_frame,
                           text=text,
                           value=pos,
                           variable=position_var,
                           style='SettingsRadio.TRadiobutton',
                           command=on_position_change)
        rb.pack(anchor="w", padx=10, pady=2)
    
    # Trennlinie
    separator = ttk.Frame(main_frame, style='SettingsSeparator.TFrame')
    separator.pack(fill=tk.X, padx=5, pady=10)
    
    # Autostart-Option
    autostart_frame = ttk.Frame(main_frame, style='Dark.TFrame')
    autostart_frame.pack(fill=tk.X, pady=(0, 10))
    
    autostart_var = tk.BooleanVar(value=app.is_autostart_enabled())
    autostart_check = ttk.Checkbutton(
        autostart_frame,
        text="Beim Windows-Start automatisch öffnen",
        variable=autostart_var,
        style='TodoCheck.TCheckbutton',
        command=app.toggle_autostart
    )
    autostart_check.pack(side=tk.LEFT)
    
    # Schließen-Button
    button_frame = ttk.Frame(main_frame, style='Settings.TFrame')
    button_frame.pack(fill=tk.X, pady=(10, 0))
    
    close_btn = ttk.Button(button_frame,
                         text="Schließen",
                         style='SettingsButton.TButton',
                         command=dialog.destroy)
    close_btn.pack(side=tk.RIGHT, padx=10)
    
    # Setze die initialen Werte NACH dem Erstellen aller Widgets
    theme_var.set(app.settings.get('theme', 'dark'))
    position_var.set(app.settings.get('window_position', 'br'))
    
    # Update der Radiobuttons erzwingen
    dialog.update()

class SettingsDialog:
    def __init__(self, app):
        self.app = app
        self.dialog = tk.Toplevel(app.root)
        self.dialog.title("Einstellungen")
        
        # Dialog-Größe und Position
        dialog_width = 400
        dialog_height = 300
        x = app.root.winfo_x() + (app.root.winfo_width() - dialog_width) // 2
        y = app.root.winfo_y() + (app.root.winfo_height() - dialog_height) // 2
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Styles anwenden
        self.dialog.configure(bg=app.colors['bg'])
        
        # Hauptframe
        main_frame = ttk.Frame(self.dialog, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Fensterposition
        position_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        position_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(position_frame,
                 text="Fensterposition:",
                 style='Settings.TLabel').pack(side=tk.LEFT)
        
        positions = {
            'tl': 'Oben Links',
            'tr': 'Oben Rechts',
            'bl': 'Unten Links',
            'br': 'Unten Rechts'
        }
        
        current_pos = app.settings.get('window_position', 'br')
        self.position_var = tk.StringVar(value=current_pos)
        
        position_menu = ttk.OptionMenu(
            position_frame,
            self.position_var,
            current_pos,
            *positions.keys(),
            style='Settings.TMenubutton'
        )
        position_menu.pack(side=tk.RIGHT)
        
        # Fenstergröße
        size_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        size_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(size_frame,
                 text="Fenstergröße:",
                 style='Settings.TLabel').pack(side=tk.LEFT)
        
        # Breite
        width_frame = ttk.Frame(size_frame, style='Dark.TFrame')
        width_frame.pack(side=tk.RIGHT)
        
        ttk.Label(width_frame,
                 text="B:",
                 style='Settings.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.width_var = tk.StringVar(value=str(app.window_width))
        width_entry = ttk.Entry(width_frame,
                              textvariable=self.width_var,
                              width=5,
                              style='Settings.TEntry')
        width_entry.pack(side=tk.LEFT, padx=5)
        
        # Höhe
        ttk.Label(width_frame,
                 text="H:",
                 style='Settings.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.height_var = tk.StringVar(value=str(app.window_height))
        height_entry = ttk.Entry(width_frame,
                               textvariable=self.height_var,
                               width=5,
                               style='Settings.TEntry')
        height_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame,
                  text="Speichern",
                  style='Settings.TButton',
                  command=self.save_settings).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame,
                  text="Abbrechen",
                  style='Settings.TButton',
                  command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Dialog modal machen
        self.dialog.transient(app.root)
        self.dialog.grab_set()
        
        # Zentrieren
        self.dialog.update_idletasks()
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        x = app.root.winfo_x() + (app.root.winfo_width() - dialog_width) // 2
        y = app.root.winfo_y() + (app.root.winfo_height() - dialog_height) // 2
        self.dialog.geometry(f"+{x}+{y}")
    
    def save_settings(self):
        """Speichert die Einstellungen"""
        try:
            # Fensterposition
            self.app.settings['window_position'] = self.position_var.get()
            
            # Fenstergröße
            try:
                width = int(self.width_var.get())
                height = int(self.height_var.get())
                if width >= 200 and height >= 300:  # Minimale Größe
                    self.app.settings['window_size'] = f"{width},{height}"
                    self.app.window_width = width
                    self.app.window_height = height
                    self.app.root.geometry(f"{width}x{height}")
            except ValueError:
                pass
            
            # Position anwenden
            self.app.apply_window_position(self.app.settings['window_position'])
            
            # Einstellungen speichern
            self.app.save_settings()
            
            self.dialog.destroy()
            
        except Exception as e:
            print(f"Fehler beim Speichern der Einstellungen: {e}")

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
            
            if self.autostart_var.get():
                app_path = os.path.abspath(sys.argv[0])
                winreg.SetValueEx(
                    key,
                    "MY TODO",
                    0,
                    winreg.REG_SZ,
                    f'"{app_path}"'
                )
            else:
                try:
                    winreg.DeleteValue(key, "MY TODO")
                except WindowsError:
                    pass
            
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Fehler beim Setzen des Autostarts: {e}")