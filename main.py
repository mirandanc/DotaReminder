import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import threading

class TimeCounter:
    def __init__(self, master):
        self.master = master
        self.master.title("Dota reminder")

        self.entries_frame = tk.Frame(master)
        self.entries_frame.pack(pady=10)

        self.entries = []
        self.repeat_counters = {}

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="+", command=self.add_time_entry, font=("Arial", 14))
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.go_button = tk.Button(self.button_frame, text="Go", command=self.start_countdown, font=("Arial", 18))
        self.go_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear All", command=self.clear_all, font=("Arial", 14))
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.countdown_label = tk.Label(master, text="", font=("Arial", 24))
        self.countdown_label.pack(pady=10)

        self.repeat_labels_frame = tk.Frame(master)
        self.repeat_labels_frame.pack(pady=10)

        self.countdown_id = None
        self.current_entry = 0

        # Add the first time entry
        self.add_time_entry()

    def add_time_entry(self):
        frame = tk.Frame(self.entries_frame)
        frame.pack(pady=5)

        time_var = tk.StringVar()
        seconds_var = tk.StringVar()

        time_entry = tk.Entry(frame, textvariable=time_var, font=("Arial", 24), justify="center", width=3)
        time_entry.pack(side=tk.LEFT, padx=5)

        colon_label = tk.Label(frame, text=":", font=("Arial", 24))
        colon_label.pack(side=tk.LEFT)

        seconds_entry = tk.Entry(frame, textvariable=seconds_var, font=("Arial", 24), justify="center", width=3)
        seconds_entry.pack(side=tk.LEFT, padx=5)

        index = len(self.entries)
        repeat_button = tk.Button(frame, text="Repeat", command=lambda i=index: self.start_repeat(i), font=("Arial", 12))
        repeat_button.pack(side=tk.LEFT, padx=5)

        self.entries.append((time_var, seconds_var, time_entry, seconds_entry))

        time_var.trace("w", lambda *args, i=index: self.validate_input(i, *args))

        if len(self.entries) == 1:
            time_entry.focus_set()

        # Repack the button frame to ensure it stays at the bottom
        self.button_frame.pack_forget()
        self.button_frame.pack(pady=10)

    def validate_input(self, index, *args):
        if 0 <= index < len(self.entries):
            time_var, seconds_var, _, seconds_entry = self.entries[index]
            value = time_var.get()
            if len(value) > 2:
                time_var.set(value[:2])
                seconds_var.set(value[2:])
                seconds_entry.focus()

    def start_countdown(self):
        if self.countdown_id:
            self.master.after_cancel(self.countdown_id)
        self.current_entry = 0
        self.run_next_countdown()

    def run_next_countdown(self):
        if self.current_entry < len(self.entries):
            time_var, seconds_var, _, _ = self.entries[self.current_entry]
            try:
                minutes = int(time_var.get() or "0")
                seconds = int(seconds_var.get() or "0")
                total_seconds = minutes * 60 + seconds
                if total_seconds > 0:
                    self.countdown(total_seconds)
                else:
                    self.current_entry += 1
                    self.countdown_label.config(text="Ding!")
                    self.play_sound()
                    self.run_next_countdown()
            except ValueError:
                messagebox.showwarning("Invalid Input", f"Please enter valid numbers for entry {self.current_entry + 1}.")
        else:
            self.countdown_label.config(text="All countdowns completed!")

    def countdown(self, remaining):
        if remaining > 0:
            mins, secs = divmod(remaining, 60)
            time_string = f"Entry {self.current_entry + 1}: {mins:02d}:{secs:02d}"
            self.countdown_label.config(text=time_string)
            self.countdown_id = self.master.after(1000, self.countdown, remaining - 1)
        else:
            self.countdown_label.config(text="Ding!")
            self.play_sound()
            self.current_entry += 1
            self.master.after(1000, self.run_next_countdown)

    def start_repeat(self, index):
        if 0 <= index < len(self.entries):
            time_var, seconds_var, _, _ = self.entries[index]
            try:
                minutes = int(time_var.get() or "0")
                seconds = int(seconds_var.get() or "0")
                total_seconds = minutes * 60 + seconds
                if total_seconds > 0:
                    if index in self.repeat_counters:
                        self.master.after_cancel(self.repeat_counters[index]['id'])
                    label = tk.Label(self.repeat_labels_frame, text="", font=("Arial", 18))
                    label.pack()
                    self.repeat_counters[index] = {'total': total_seconds, 'remaining': total_seconds, 'label': label}
                    self.repeat_countdown(index)
                else:
                    messagebox.showwarning("Invalid Input", f"Please enter a valid time for entry {index + 1}.")
            except ValueError:
                messagebox.showwarning("Invalid Input", f"Please enter valid numbers for entry {index + 1}.")

    def repeat_countdown(self, index):
        counter = self.repeat_counters[index]
        if counter['remaining'] > 0:
            mins, secs = divmod(counter['remaining'], 60)
            time_string = f"Repeat {index + 1}: {mins:02d}:{secs:02d}"
            counter['label'].config(text=time_string)
            counter['remaining'] -= 1
            counter['id'] = self.master.after(1000, self.repeat_countdown, index)
        else:
            self.play_sound()
            counter['remaining'] = counter['total']
            self.repeat_countdown(index)

    def play_sound(self):
        sound_thread = threading.Thread(target=playsound, args=('E:/Coding/DotaReminder/sounds/basic-ding.mp3',))
        sound_thread.start()

    def clear_all(self):
        if self.countdown_id:
            self.master.after_cancel(self.countdown_id)
        self.countdown_label.config(text="")

        for index, counter in self.repeat_counters.items():
            self.master.after_cancel(counter['id'])
            counter['label'].destroy()
        self.repeat_counters.clear()

        for widget in self.repeat_labels_frame.winfo_children():
            widget.destroy()

        self.current_entry = 0

        messagebox.showinfo("Clear All", "All countdowns have been cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeCounter(root)
    root.mainloop()