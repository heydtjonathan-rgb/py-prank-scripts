import tkinter as tk
from tkinter import font
import threading
import time
import os

# --- EINSTELLUNGEN ---
DAUER = 60 # Sekunden bis zum Schließen
TEXT = "SYSTEM KRITISCH - ZUGRIFF VERWEIGERT"
INFO = "Ihre Hardware wird synchronisiert... Bitte warten."

def timer(root, label):
    for i in range(DAUER, -1, -1):
        if not root.winfo_exists(): break
        label.config(text=f"Automatischer Unlock in {i}s")
        time.sleep(1)
    if root.winfo_exists(): root.destroy()

root = tk.Tk()
root.attributes("-fullscreen", True, "-topmost", True)
root.config(bg="black", cursor="none") # Maus unsichtbar
root.protocol("WM_DELETE_WINDOW", lambda: None) # Unschließbar

f1 = font.Font(family="Arial", size=50, weight="bold")
f2 = font.Font(family="Arial", size=15)

tk.Label(root, text=TEXT, font=f1, fg="red", bg="black").pack(pady=100)
tk.Label(root, text=INFO, font=f2, fg="white", bg="black").pack()
lbl = tk.Label(root, text="", font=f2, fg="gray", bg="black")
lbl.pack(side="bottom", pady=20)

# Notfall-Hinweis (kleingedruckt)
hinweis = "NOTFALL: [Win] Strg+Alt+Entf -> Task-Manager | [Mac] Cmd+Opt+Esc -> Sofort beenden"
tk.Label(root, text=hinweis, font=("Arial", 8), fg="#222", bg="black").pack(side="bottom")

threading.Thread(target=timer, args=(root, lbl), daemon=True).start()
root.mainloop()
