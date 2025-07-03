import calendar
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Dark theme colors
DARK_BG = "#181c24"
DARK_FG = "#f1f1f1"
ACCENT = "#e10600"  # Ferrari red for accent
GRID_BG = "#23272f"
TODAY_BG = "#2e8b57"
REMINDER_BG = "#3a3f4b"
REMINDER_ACCENT = "#ffb300"
BUTTON_BG = "#23272f"
BUTTON_FG = "#f1f1f1"
BUTTON_ACTIVE_BG = "#e10600"
BUTTON_ACTIVE_FG = "#fff"

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule Calendar")
        self.root.geometry("520x650")
        self.root.configure(bg=DARK_BG)
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.selected_day = None
        self.reminders = {}

        # App Icon/Title
        self.icon_label = tk.Label(self.root, text="📅 Schedule Calendar", font=("Segoe UI", 20, "bold"), bg=DARK_BG, fg=ACCENT)
        self.icon_label.pack(pady=(10, 0))

        # Header
        self.header_frame = tk.Frame(self.root, bg=DARK_BG)
        self.header_frame.pack(fill="x", pady=(10, 0))
        self.prev_button = tk.Button(self.header_frame, text="◀", width=3, command=self.prev_month,
                                     font=("Segoe UI", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                                     activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG, bd=0, relief="flat")
        self.prev_button.pack(side="left", padx=(10, 5))
        self.month_year_label = tk.Label(self.header_frame, text="", font=("Segoe UI", 15, "bold"), bg=DARK_BG, fg=ACCENT)
        self.month_year_label.pack(side="left", expand=True)
        self.next_button = tk.Button(self.header_frame, text="▶", width=3, command=self.next_month,
                                     font=("Segoe UI", 12, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                                     activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG, bd=0, relief="flat")
        self.next_button.pack(side="right", padx=(5, 10))

        # Calendar grid
        self.calendar_frame = tk.Frame(self.root, bg=DARK_BG)
        self.calendar_frame.pack(fill="both", expand=False, pady=(10, 0))

        # Reminders
        self.reminder_label = tk.Label(self.root, text="Reminders for selected day:", font=("Segoe UI", 12, "bold"), bg=DARK_BG, fg=ACCENT)
        self.reminder_label.pack(pady=(15, 0))
        self.reminder_listbox = tk.Listbox(self.root, width=40, height=5, font=("Segoe UI", 10),
                                           bg=REMINDER_BG, fg=DARK_FG, selectbackground=ACCENT, selectforeground="#fff",
                                           highlightthickness=0, bd=0, relief="flat")
        self.reminder_listbox.pack(pady=(0, 10))

        # Buttons
        self.button_frame = tk.Frame(self.root, bg=DARK_BG)
        self.button_frame.pack(fill="x", pady=(0, 10))
        self.add_reminder_button = tk.Button(self.button_frame, text="Add Reminder", command=self.add_reminder,
                                             font=("Segoe UI", 10, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                                             activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG, bd=0, relief="flat")
        self.add_reminder_button.pack(side="left", padx=10)
        self.delete_reminder_button = tk.Button(self.button_frame, text="Delete Reminder", command=self.delete_reminder,
                                                font=("Segoe UI", 10, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                                                activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG, bd=0, relief="flat")
        self.delete_reminder_button.pack(side="left", padx=10)

        # Log area
        self.log_label = tk.Label(self.root, text="Log:", font=("Segoe UI", 11, "bold"), bg=DARK_BG, fg=ACCENT)
        self.log_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.log_text = tk.Text(self.root, height=3, font=("Segoe UI", 10), bg=REMINDER_BG, fg=DARK_FG, bd=0, relief="flat")
        self.log_text.pack(fill="x", padx=10, pady=(0, 10))
        self.log_text.insert("end", "Welcome to the Schedule Calendar!\n")
        self.log_text.config(state="disabled")

        # Status bar
        self.status_label = tk.Label(self.root, text="", font=("Segoe UI", 9), bg=DARK_BG, fg="#888888")
        self.status_label.pack(fill="x", pady=(0, 5))

        self.update_calendar()

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        self.month_year_label.config(text=f"{calendar.month_name[self.month]} {self.year}")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            lbl = tk.Label(self.calendar_frame, text=day, font=("Segoe UI", 10, "bold"), bg=GRID_BG, fg=ACCENT, bd=0, relief="flat")
            lbl.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
        month_days = calendar.monthcalendar(self.year, self.month)
        today = datetime.now()
        for r, week in enumerate(month_days, 1):
            for c, day in enumerate(week):
                if day == 0:
                    lbl = tk.Label(self.calendar_frame, text="", width=4, height=2, bg=DARK_BG, bd=0, relief="flat")
                    lbl.grid(row=r, column=c, padx=2, pady=2)
                else:
                    has_reminder = (self.year, self.month) in self.reminders and day in self.reminders[(self.year, self.month)]
                    is_today = (self.year == today.year and self.month == today.month and day == today.day)
                    bg = TODAY_BG if is_today else (REMINDER_ACCENT if has_reminder else GRID_BG)
                    fg = DARK_FG if is_today or has_reminder else DARK_FG
                    btn = tk.Button(self.calendar_frame, text=("🏁" if has_reminder else "") + str(day), width=4, height=2, bg=bg, fg=fg,
                                    relief="groove", bd=0, font=("Segoe UI", 10, "bold"),
                                    activebackground=ACCENT, activeforeground="#fff",
                                    command=lambda d=day: self.select_day(d), cursor="hand2")
                    btn.grid(row=r, column=c, padx=2, pady=2)
                    btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BUTTON_ACTIVE_BG))
                    btn.bind("<Leave>", lambda e, b=btn, bg=bg: b.config(bg=bg))
                    btn.bind("<Double-Button-1>", lambda e, d=day: self.add_reminder(day=d))
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        self.update_reminder_listbox()

    def select_day(self, day):
        self.selected_day = day
        self.update_reminder_listbox()
        self.status_label.config(text=f"Selected day: {day}")
        self.log(f"Selected {calendar.month_name[self.month]} {day}")

    def update_reminder_listbox(self):
        self.reminder_listbox.delete(0, tk.END)
        if self.selected_day is not None:
            reminders = self.reminders.get((self.year, self.month), {}).get(self.selected_day, [])
            if reminders:
                for rem in reminders:
                    self.reminder_listbox.insert(tk.END, rem)
            else:
                self.reminder_listbox.insert(tk.END, "No reminders for this day.")
        else:
            self.reminder_listbox.insert(tk.END, "Select a day to view reminders.")

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.selected_day = None
        self.update_calendar()
        self.status_label.config(text="")
        self.log(f"Moved to {calendar.month_name[self.month]} {self.year}")

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.selected_day = None
        self.update_calendar()
        self.status_label.config(text="")
        self.log(f"Moved to {calendar.month_name[self.month]} {self.year}")

    def add_reminder(self, day=None):
        if day is None:
            if self.selected_day is None:
                messagebox.showinfo("Select Day", "Please select a day to add a reminder.")
                return
            day = self.selected_day
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title(f"Add Reminder for {calendar.month_name[self.month]} {day}, {self.year}")
        reminder_window.geometry("320x160")
        reminder_window.configure(bg=DARK_BG)
        tk.Label(reminder_window, text=f"Day: {day}", font=("Segoe UI", 11), bg=DARK_BG, fg=ACCENT).pack(pady=(10, 2))
        tk.Label(reminder_window, text="Reminder:", font=("Segoe UI", 10), bg=DARK_BG, fg=DARK_FG).pack()
        reminder_entry = tk.Entry(reminder_window, font=("Segoe UI", 10), width=30, bg=REMINDER_BG, fg=DARK_FG, insertbackground=DARK_FG)
        reminder_entry.pack(pady=5)
        def save_reminder():
            reminder = reminder_entry.get().strip()
            if not reminder:
                messagebox.showwarning("Input Error", "Reminder cannot be empty.")
                return
            self.reminders.setdefault((self.year, self.month), {}).setdefault(day, []).append(reminder)
            self.update_calendar()
            self.status_label.config(text=f"Added reminder for {calendar.month_name[self.month]} {day}.")
            self.log(f"Added reminder for {calendar.month_name[self.month]} {day}: {reminder}")
            reminder_window.destroy()
        tk.Button(reminder_window, text="Save", command=save_reminder,
                  font=("Segoe UI", 10, "bold"), bg=BUTTON_BG, fg=BUTTON_FG,
                  activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG, bd=0, relief="flat").pack(pady=10)

    def delete_reminder(self):
        if self.selected_day is None:
            messagebox.showinfo("Select Day", "Please select a day to delete a reminder.")
            return
        selected_index = self.reminder_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Select Reminder", "Please select a reminder to delete.")
            return
        reminders = self.reminders.get((self.year, self.month), {}).get(self.selected_day, [])
        if reminders:
            removed = reminders[selected_index[0]]
            del reminders[selected_index[0]]
            if not reminders:
                del self.reminders[(self.year, self.month)][self.selected_day]
            self.update_calendar()
            self.status_label.config(text=f"Deleted reminder for {calendar.month_name[self.month]} {self.selected_day}.")
            self.log(f"Deleted reminder: {removed}")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop() 