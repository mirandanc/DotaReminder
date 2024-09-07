import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import threading

class TimeCounter:
    def __init__(self, master):
        self.master = master
        self.master.title("Dota reminder")

        self.entries = []
        self.add_time_entry()

        self.time_var = tk.StringVar()
        self.time_var.trace("w", self.validate_input)

        self.minute_entry = tk.Entry(master, textvariable=self.time_var, font=("Arial", 24), justify="center", width=3)
        self.minute_entry.grid(row=0, column=0, padx=10, pady=10)
        self.minute_entry.focus_set()

        self.colon_label = tk.Label(master, text=":", font=("Arial", 24))
        self.colon_label.grid(row=0, column=1)

        self.seconds_var = tk.StringVar()
        self.seconds_entry = tk.Entry(master, textvariable=self.seconds_var, font=("Arial", 24), justify="center", width=3)
        self.seconds_entry.grid(row=0, column=2, padx=10, pady=10)

        self.add_button = tk.Button(master, text="+", command=self.add_time_entry, font=("Arial", 14))
        self.add_button.pack(pady=10)

        self.go_button = tk.Button(master, text="Go", command=self.start_countdown, font=("Arial", 18))
        self.go_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.countdown_label = tk.Label(master, text="", font=("Arial", 24))
        self.countdown_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.countdown_id = None

    def add_time_entry(self):
        frame = tk.Frame(self.master)
        frame.pack(pady=5)

        time_var = tk.StringVar()
        time_var.trace("w", lambda *args, index=len(self.entries): self.validate_input(index, *args))

        time_entry = tk.Entry(frame, textvariable=time_var, font=("Arial", 24), justify="center", width=4)
        time_entry.pack(side=tk.LEFT, padx=5)

        colon_label = tk.Label(frame, text=":", font=("Arial", 24))
        colon_label.pack(side=tk.LEFT)

        seconds_var = tk.StringVar()
        seconds_entry = tk.Entry(frame, textvariable=seconds_var, font=("Arial", 24), justify="center", width=2)
        seconds_entry.pack(side=tk.LEFT, padx=5)

        self.entries.append((time_var, seconds_var, time_entry, seconds_entry))

        if len(self.entries) == 1:
            time_entry.focus_set()    

    def validate_input(self, *args):
        value = self.time_var.get()
        if len(value) > 4:
            self.time_var.set(value[:4])
        if len(value) >= 2:
            self.time_var.set(value[:2])
            self.seconds_var.set(value[2:])
            self.seconds_entry.focus()

    def start_countdown(self):
        # Cancel any existing countdown
        if self.countdown_id:
            self.master.after_cancel(self.countdown_id)
        try:
            minutes = int(self.time_var.get() or "0")
            seconds = int(self.seconds_var.get() or "0")
            total_seconds = minutes * 60 + seconds
            if total_seconds > 0:
                self.countdown(total_seconds)
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid time.")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid numbers.")
            

    def countdown(self, remaining):
        def play_sound(file_path):
            playsound(file_path)
        if remaining > 0:
            mins, secs = divmod(remaining, 60)
            time_string = f"{mins:02d}:{secs:02d}"
            self.countdown_label.config(text=time_string)
            self.countdown_id = self.master.after(1000, self.countdown, remaining - 1)
        else:
            self.countdown_label.config(text="Ding!")
            sound_thread = threading.Thread(target=play_sound, args=('E:/Coding/DotaReminder/sounds/basic-ding.mp3',))
            sound_thread.start()
            self.countdown_id = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeCounter(root)
    root.mainloop() 