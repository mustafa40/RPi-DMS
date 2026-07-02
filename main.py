import tkinter as tk
import random
import time

root = tk.Tk()
root.title("RPi-DMS")
root.geometry("800x480")
root.configure(bg="black")

title = tk.Label(root, text="DRIVER MONITORING SYSTEM",
                 fg="white", bg="black", font=("Arial", 24, "bold"))
title.pack(pady=20)

status = tk.Label(root, text="SYSTEM READY",
                  fg="lime", bg="black", font=("Arial", 36, "bold"))
status.pack(pady=35)

info = tk.Label(root, text="Camera: Waiting...\nFatigue Score: %0",
                fg="white", bg="black", font=("Arial", 22))
info.pack(pady=20)

def update():
    fatigue = random.randint(0, 100)

    if fatigue < 40:
        text, color = "NORMAL", "lime"
    elif fatigue < 70:
        text, color = "YORGUNLUK BASLADI", "orange"
    else:
        text, color = "UYARI! MOLA VER", "red"

    status.config(text=text, fg=color)
    info.config(text=f"Camera: Waiting...\nFatigue Score: %{fatigue}\nTime: {time.strftime('%H:%M:%S')}")
    root.after(1000, update)

update()
root.mainloop()
