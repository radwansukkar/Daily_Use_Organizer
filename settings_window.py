import tkinter as tk
from tkinter import messagebox
from storage import load_config
import json

from storage import CONFIG_FILE

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def show_settings_window():
    config = load_config()

    win = tk.Toplevel()
    win.title("Settings")
    win.geometry("400x400")

    tk.Label(win, text="Monitored Apps (process name -> limit in minutes)",
              font=("Arial", 11, "bold")).pack(pady=10)

    
    rows_frame = tk.Frame(win)
    rows_frame.pack(fill="x", padx=10)

    row_widgets = []  

    def add_row(app_name="", limit_minutes=""):
        row = tk.Frame(rows_frame)
        row.pack(fill="x", pady=2)

        app_entry = tk.Entry(row, width=20)
        app_entry.insert(0, app_name)
        app_entry.pack(side="left", padx=2)

        limit_entry = tk.Entry(row, width=8)
        limit_entry.insert(0, str(limit_minutes))
        limit_entry.pack(side="left", padx=2)

        def remove_row():
            row.destroy()
            row_widgets.remove((app_entry, limit_entry, row))

        tk.Button(row, text="Remove", command=remove_row).pack(side="left", padx=2)

        row_widgets.append((app_entry, limit_entry, row))

   
    for app_name, limit_minutes in config["monitored_apps"].items():
        add_row(app_name, limit_minutes)

    tk.Button(win, text="+ Add App", command=lambda: add_row()).pack(pady=10)

    tk.Label(win, text="Poll interval (seconds)").pack(pady=(10, 0))
    interval_entry = tk.Entry(win, width=8)
    interval_entry.insert(0, str(config["poll_interval_sec"]))
    interval_entry.pack(pady=5)

    def on_save():
        new_apps = {}
        for app_entry, limit_entry, _ in row_widgets:
            app_name = app_entry.get().strip()
            limit_text = limit_entry.get().strip()

            if not app_name or not limit_text:
                continue

            try:
                new_apps[app_name] = int(limit_text)
            except ValueError:
                messagebox.showerror("Invalid input", f"Limit for '{app_name}' must be a number")
                return

        try:
            new_interval = int(interval_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid input", "Poll interval must be a number")
            return

        new_config = {
            "monitored_apps": new_apps,
            "poll_interval_sec": new_interval
        }
        save_config(new_config)
        messagebox.showinfo("Saved", "Settings saved. Restart the app for changes to take effect.")
        win.destroy()

    tk.Button(win, text="Save", command=on_save, font=("Arial", 11, "bold")).pack(pady=15)