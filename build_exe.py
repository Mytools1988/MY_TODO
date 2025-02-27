import os
import subprocess
import shutil

def clean_build():
    """Löscht alte Build-Dateien"""
    paths = ['dist', 'build', 'TodoApp.spec']
    for path in paths:
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except:
            pass

def build_exe():
    # Erst aufräumen
    clean_build()
    
    # Pfad zur todo.py
    script_path = 'todo.py'
    
    # PyInstaller Kommando
    command = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=TodoApp',
        '--noconsole',
        '--hidden-import=tkinter',
        '--hidden-import=json',
        script_path
    ]
    
    # Ausführen des Befehls
    try:
        subprocess.run(command, check=True)
        print("EXE wurde erfolgreich erstellt! Schauen Sie im 'dist' Ordner nach.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Erstellen der EXE: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    build_exe()