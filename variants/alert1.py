import tkinter as tk
from tkinter import font
import threading
import time
import os
import sys

# ─── ANPASSBAR (KONFIGURATION) ───────────────────────
DAUER_SEKUNDEN = 120       # Zeit bis zum automatischen Schließen
TITEL_FENSTER = "SYSTEM ALERT"
HAUPTTEXT = "ZUGRIFF VERWEIGERT"
UNTERTEXT = "Sicherheits-Protokoll aktiv..."
HINTERGRUND = "black"
TEXTFARBE = "red"
INFOTEXT_FARBE = "white"
TIMER_FARBE = "gray"

# Selbstlöschung der Datei nach Beenden (True = Ja, False = Nein)
AUTO_DELETE = True 

# Versteckter Button Einstellungen (unten rechts)
BUTTON_TEXT = "EXIT"
BUTTON_FARBE = "#0a0a0a" # Fast unsichtbar auf Schwarz
# ─────────────────────────────────────────────────────

def beenden():
    """Schließt das Programm und löscht die Datei"""
    dateipfad = os.path.abspath(__file__)
    root.destroy()
    if AUTO_DELETE:
        try:
            os.remove(dateipfad)
        except:
            pass
    sys.exit()

def countdown(label):
    """Zählt die Sekunden im Hintergrund runter"""
    for i in range(DAUER_SEKUNDEN, -1, -1):
        if not root.winfo_exists(): break
        label.config(text=f"Automatischer Unlock in {i}s")
        time.sleep(1)
    if root.winfo_exists():
        beenden()

def erzwinge_fokus():
    """Holt das Fenster alle 200ms in den Vordergrund"""
    root.focus_force()
    root.lift()
    root.after(200, erzwinge_fokus)

# Fenster-Initialisierung
root = tk.Tk()
root.title(TITEL_FENSTER)

# ─── GRÖSSE & SPERREN ────────────────────────────────
root.attributes("-fullscreen", True, "-topmost", True)
root.resizable(False, False) # Verhindert Kleinerziehen
root.configure(bg=HINTERGRUND)
root.config(cursor="none")   # Maus unsichtbar

# System-Sperren (Windows & Mac)
root.protocol("WM_DELETE_WINDOW", lambda: None) # X-Button / Alt+F4
try:
    root.createcommand('tk::mac::Quit', lambda: None) # Mac System Quit
except:
    pass

# Tastatur-Sperren
root.bind_all("<Command-q>", lambda e: "break")
root.bind_all("<Command-h>", lambda e: "break")
root.bind_all("<Command-w>", lambda e: "break")
root.bind_all("<Alt-Tab>", lambda e: "break")

# ─── UI ELEMENTE ─────────────────────────────────────
f_gross = font.Font(family="Arial", size=60, weight="bold")
f_klein = font.Font(family="Arial", size=18)

# Texte platzieren
tk.Label(root, text=HAUPTTEXT, font=f_gross, fg=TEXTFARBE, bg=HINTERGRUND).pack(pady=120)
tk.Label(root, text=UNTERTEXT, font=f_klein, fg=INFOTEXT_FARBE, bg=HINTERGRUND).pack()

# Timer Anzeige
timer_lbl = tk.Label(root, text="", font=f_klein, fg=TIMER_FARBE, bg=HINTERGRUND)
timer_lbl.pack(side="bottom", pady=50)

# Versteckter EXIT-Button (unten rechts)
tk.Button(root, text=BUTTON_TEXT, command=beenden, 
          bg=HINTERGRUND, fg=BUTTON_FARBE, borderwidth=0, 
          highlightthickness=0, activebackground="#111").place(relx=0.98, rely=0.98, anchor="center")

# ─── START ───────────────────────────────────────────
threading.Thread(target=countdown, args=(timer_lbl,), daemon=True).start()
erzwinge_fokus()

root.mainloop()
