import os
import csv
from datetime import datetime

class TodoManager:
    """Daten-Management-Klasse für Todos"""
    
    def __init__(self):
        """Initialisiert den TodoManager"""
        self.todos = []
        self.storage_path = 'todos.txt'
        self.load()

    def load(self):
        """Lädt alle Todos aus der Datei"""
        try:
            self.todos = []
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():  # Ignoriere leere Zeilen
                            parts = line.strip().split('|')
                            if len(parts) >= 5:  # Stelle sicher, dass alle Felder vorhanden sind
                                todo = {
                                    'text': parts[0],
                                    'category': parts[1],
                                    'priority': parts[2],
                                    'deadline': parts[3],
                                    'completed': parts[4] == '1'
                                }
                                self.todos.append(todo)
            except FileNotFoundError:
                # Erstelle eine leere Datei wenn sie nicht existiert
                open(self.storage_path, 'w', encoding='utf-8').close()
        except Exception as e:
            print(f"Fehler beim Laden der Todos: {e}")
            self.todos = []  # Fallback zu leerer Liste

    def save(self):
        """Speichert alle Todos in die Datei"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                for todo in self.todos:
                    # Stelle sicher, dass alle erforderlichen Felder existieren
                    text = todo.get('text', '')
                    category = todo.get('category', 'Allgemein')
                    priority = todo.get('priority', '►')
                    deadline = todo.get('deadline', '')
                    completed = '1' if todo.get('completed', False) else '0'
                    
                    # Schreibe eine Zeile pro Todo
                    line = f"{text}|{category}|{priority}|{deadline}|{completed}\n"
                    f.write(line)
        except Exception as e:
            print(f"Fehler beim Speichern der Todos: {e}")

    def add(self, todo):
        """Fügt ein neues Todo hinzu"""
        self.todos.append(todo)
        self.save()

    def update(self, index, todo):
        """Aktualisiert ein bestehendes Todo"""
        if 0 <= index < len(self.todos):
            self.todos[index] = todo
            self.save()

    def delete(self, index):
        """Löscht ein Todo"""
        if 0 <= index < len(self.todos):
            del self.todos[index]
            self.save()

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
        """Sucht in den Todos"""
        query = query.lower()
        return [todo for todo in self.todos 
                if query in todo.get('text', '').lower() or 
                   query in todo.get('category', '').lower()]

    def toggle_completed(self, index):
        """Schaltet den Status eines Todos um"""
        if 0 <= index < len(self.todos):
            self.todos[index]['completed'] = not self.todos[index].get('completed', False)
            self.save()

    def cleanup(self):
        """Entfernt erledigte Todos"""
        self.todos = [todo for todo in self.todos 
                     if not todo.get('completed', False)]
        self.save()

    def save_todos(self, todos):
        """Speichert eine neue Todo-Liste"""
        self.todos = todos  # Aktualisiere die interne Liste
        self.save()  # Speichere in die Datei 