import tkinter as tk
import threading
from monitor import monitor_loop
from report import show_report_window
from settings_window import show_settings_window
from tray_icon import build_tray_icon

stop_event = threading.Event()

def start_monitoring():
    thread = threading.Thread(target=monitor_loop, args=(stop_event,), daemon=True)
    thread.start()

def quit_app(icon, item):
    stop_event.set()
    icon.stop()
    root.after(0, root.destroy)

def open_report(icon, item):
    root.after(0, show_report_window)

def open_settings(icon, item):
    root.after(0, show_settings_window)

root = tk.Tk()
root.withdraw()  # hide the main window completely, only the tray icon is visible

start_monitoring()

tray = build_tray_icon(open_report, open_settings, quit_app)
threading.Thread(target=tray.run, daemon=True).start()

root.mainloop()