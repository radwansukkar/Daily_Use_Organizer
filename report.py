import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from storage import load_usage_data
from datetime import date, timedelta

def build_weekly_dataframe():
    data = load_usage_data()
    last_7_days = [str(date.today() - timedelta(days=i)) for i in range(7)]

    rows = []
    for day in last_7_days:
        day_data = data.get(day, {})
        for app, seconds in day_data.items():
            rows.append({"date": day, "app": app, "minutes": round(seconds / 60, 1)})

    return pd.DataFrame(rows)

def weekly_report():
    df = build_weekly_dataframe()
    if df.empty:
        print("Not enough data yet")
        return
    pivot = df.pivot_table(index="date", columns="app", values="minutes", fill_value=0)
    print(pivot.sort_index())

def show_report_window():
    df = build_weekly_dataframe()

    win = tk.Toplevel()
    win.title("Weekly Report")
    win.geometry("600x450")

    if df.empty:
        tk.Label(win, text="Not enough data yet to build a report",
                 font=("Arial", 12)).pack(pady=50)
        return

    totals = df.groupby("app")["minutes"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(5, 4))
    totals.plot(kind="bar", ax=ax, color="#4a7dbd")
    ax.set_ylabel("Minutes (weekly total)")
    ax.set_title("Usage by app")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    weekly_report()