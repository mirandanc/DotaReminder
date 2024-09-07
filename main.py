import time
import tkinter as tk

def countdown():
    global timer
    if timer > 0:
        mins, secs = divmod(timer, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        display_label.config(text=timeformat)
        timer -= 1
        root.after(1000, countdown)
    else:
        display_label.config(text="DING!")

def start_timer():
    global timer
    try:
        timer = int(entry.get())
        countdown()
    except ValueError:
        display_label.config(text="Entre o tempo")

# Create the main window
root = tk.Tk()
root.title("Dota Reminder")

# Create and pack the input field
entry = tk.Entry(root, width=10)
entry.pack(pady=10)

# Create and pack the start button
start_button = tk.Button(root, text="Start", command=start_timer)
start_button.pack(pady=5)

# Create and pack the display label
display_label = tk.Label(root, text="00:00", font=("Arial", 48))
display_label.pack(pady=20)

# Initialize the timer variable
timer = 0

# Start the GUI event loop
root.mainloop()
