import tkinter as tk
from tkinter import font
import threading
import time
import os

# ─── ANPASSBAR (KONFIGURATION) ───────────────────────
TITEL = "SYSTEM GESPERRT"
HAUPTTEXT = "ZUGRIFF VERWEIGERT"
UNTERTEXT = "Sicherheits-Protokoll aktiv..."
HINTERGRUND = "black"
TEXTFARBE = "red"
DAUER_SEKUNDEN = 99
BILD_PFAD = None       # Pfad zu einem Bild (z.B. "warnung.png")
MUSIK_PFAD = None      # Pfad zu einer MP3 (z.B. "alarm.mp3")
# ─────────────────────────────────────────────────────

def beenden():
    """Schließt das Programm sofort"""
    root.destroy()

def starte_musik():
    """Versucht Musik zu laden, falls ein Pfad angegeben ist"""
    if MUSIK_PFAD and os.path.exists(MUSIK_PFAD):
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(MUSIK_PFAD)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

def countdown(label):
    """Zählt die Zeit im Hintergrund runter"""
    for i in range(DAUER_SEKUNDEN, -1, -1):
        if not root.winfo_exists(): break
        label.config(text=f"Automatischer Unlock in {i}s")
        time.sleep(1)
    if root.winfo_exists():
        root.destroy()

# Hauptfenster erstellen
root = tk.Tk()
root.title(TITEL)

# Vollbild & Immer im Vordergrund
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg=HINTERGRUND)
root.config(cursor="none") # Mauszeiger unsichtbar machen

# ─── SPERREN (WINDOWS & MAC) ─────────────────────────

# 1. Blockiert das "X" und Alt+F4 (Windows/Linux)
root.protocol("WM_DELETE_WINDOW", lambda: None)

# 2. Blockiert Cmd+Q über das Mac-Systemmenü
try:
    root.createcommand('tk::mac::Quit', lambda: None)
except:
    pass

# 3. Blockiert Cmd+Q, Cmd+W, Cmd+H auf Tastaturebene (Mac)
root.bind_all("<Command-q>", lambda e: "break")
root.bind_all("<Command-w>", lambda e: "break")
root.bind_all("<Command-h>", lambda e: "break")

# 4. Blockiert Alt+Tab (Windows) weitestgehend
root.bind_all("<Alt-Tab>", lambda e: "break")

# ─── UI ELEMENTE ─────────────────────────────────────

# Bild laden (falls konfiguriert)
if BILD_PFAD and os.path.exists(BILD_PFAD):
    try:
        from PIL import Image, ImageTk
        img = Image.open(BILD_PFAD).resize((300, 300))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(root, image=photo, bg=HINTERGRUND)
        img_label.image = photo
        img_label.pack(pady=30)
    except:
        pass

# Schriften definieren
font_gross = font.Font(family="Arial", size=60, weight="bold")
font_klein = font.Font(family="Arial", size=18)

# Haupt-Warntexte
tk.Label(root, text=HAUPTTEXT, font=font_gross, fg=TEXTFARBE, bg=HINTERGRUND).pack(pady=100)
tk.Label(root, text=UNTERTEXT, font=font_klein, fg="white", bg=HINTERGRUND).pack()

# Timer Anzeige
timer_lbl = tk.Label(root, text="", font=font_klein, fg="gray", bg=HINTERGRUND)
timer_lbl.pack(side="bottom", pady=40)

# ─── VERSTECKTER NOTAUSGANG ──────────────────────────
# Ein kleiner Button unten rechts, fast unsichtbar (Dunkelgrau auf Schwarz)
exit_btn = tk.Button(root, text="EXIT", command=beenden, 
                     bg=HINTERGRUND, fg="#0a0a0a", borderwidth=0, 
                     highlightthickness=0, activebackground="#111")
exit_btn.place(relx=0.98, rely=0.98, anchor="center")

# ─── START ───────────────────────────────────────────

# Fokus alle 200ms erzwingen (gegen Fensterwechsel)
def erzwinge_fokus():
    root.focus_force()
    root.lift()
    root.after(200, erzwinge_fokus)

# Threads starten
threading.Thread(target=countdown, args=(timer_lbl,), daemon=True).start()
threading.Thread(target=starte_musik, daemon=True).start()
erzwinge_fokus()

root.mainloop()
