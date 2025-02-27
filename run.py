from app.main import TodoApp

if __name__ == "__main__":
    try:
        app = TodoApp()
        app.root.mainloop()
    except Exception as e:
        print(f"Fehler beim Starten der App: {e}") 