import tkinter as tk
from tkinter import font
import threading
import time
import os

# ─── ANPASSBAR ───────────────────────────────────────
TITEL = "SYSTEM GESPERRT"
HAUPTTEXT = "ZUGRIFF VERWEIGERT"
UNTERTEXT = "Sicherheits-Protokoll aktiv..."
HINTERGRUND = "black"
TEXTFARBE = "red"
DAUER_SEKUNDEN = 60
BILD_PFAD = None       # z.B. "bild.png" oder None
MUSIK_PFAD = None      # z.B. "alarm.mp3" oder None
# ─────────────────────────────────────────────────────

def beenden():
    root.destroy()

def starte_musik():
    if MUSIK_PFAD and os.path.exists(MUSIK_PFAD):
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(MUSIK_PFAD)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Musik-Fehler: {e}")

def countdown(label):
    for i in range(DAUER_SEKUNDEN, -1, -1):
        if not root.winfo_exists(): break
        label.config(text=f"Automatischer Unlock in {i}s")
        time.sleep(1)
    if root.winfo_exists():
        root.destroy()

# Fenster erstellen
root = tk.Tk()
root.attributes("-fullscreen", True, "-topmost", True)
root.configure(bg=HINTERGRUND)
root.config(cursor="none") # Maus unsichtbar

# --- SPERREN ---
root.protocol("WM_DELETE_WINDOW", lambda: None) # X-Button / Alt+F4
root.bind("<Command-q>", lambda e: "break")     # Mac Beenden
root.bind("<Command-h>", lambda e: "break")     # Mac Verstecken
root.bind("<Alt-Tab>", lambda e: "break")       # Windows Wechseln

# Bild (optional)
if BILD_PFAD and os.path.exists(BILD_PFAD):
    try:
        from PIL import Image, ImageTk
        img = ImageTk.PhotoImage(Image.open(BILD_PFAD).resize((300,300)))
        tk.Label(root, image=img, bg=HINTERGRUND).pack(pady=20)
    except: pass

# Texte
f_gross = font.Font(family="Arial", size=60, weight="bold")
f_klein = font.Font(family="Arial", size=18)

tk.Label(root, text=HAUPTTEXT, font=f_gross, fg=TEXTFARBE, bg=HINTERGRUND).pack(pady=100)
tk.Label(root, text=UNTERTEXT, font=f_klein, fg="white", bg=HINTERGRUND).pack()

timer_lbl = tk.Label(root, text="", font=f_klein, fg="gray", bg=HINTERGRUND)
timer_lbl.pack(side="bottom", pady=40)

# --- DER VERSTECKTE BUTTON (UNTEN RECHTS) ---
# Fast schwarz auf schwarz
exit_btn = tk.Button(root, text="EXIT", command=beenden, 
                     bg=HINTERGRUND, fg="#0a0a0a", borderwidth=0, 
                     highlightthickness=0, activebackground="#111")
exit_btn.place(relx=0.98, rely=0.98, anchor="center")

# Threads starten
threading.Thread(target=countdown, args=(timer_lbl,), daemon=True).start()
threading.Thread(target=starte_musik, daemon=True).start()

root.mainloop()
