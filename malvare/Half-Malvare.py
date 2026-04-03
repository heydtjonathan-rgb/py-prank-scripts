import tkinter as tk
from tkinter import font
import threading
import time
import os
import sys

# Versuche PyAutoGUI für die Maus-Sperre zu laden
try:
    import pyautogui
    pyautogui.FAILSAFE = False # Deaktiviert Abbruch durch Ecke-Fahren
    PYAUTOGUI_FOUND = True
except ImportError:
    PYAUTOGUI_FOUND = False

# ─── ANPASSBAR (KONFIGURATION) ───────────────────────
DAUER_SEKUNDEN = 10       
HAUPTTEXT = "SYSTEM GESPERRT"
UNTERTEXT = "Sicherheits-Protokoll aktiv..."
HINTERGRUND = "black"
TEXTFARBE = "red"

# --- ZUSATZFUNKTIONEN (True = An / False = Aus) ---
MAUS_SPERRE = True         # Maus wird in der Mitte gefangen (Benötigt pip install pyautogui)
WINDOWS_TASK_KILL = True   # Killt Windows Task-Manager sofort
AUTO_DELETE = True         # Datei löscht sich nach Beenden selbst

# --- NOTAUSGANG (Da Maus gesperrt ist) ---
EXIT_TASTE = "q"           # Drücke diese Taste, um das Programm zu beenden
# ─────────────────────────────────────────────────────

def beenden(event=None):
    """Schließt das Programm und löscht die Datei"""
    dateipfad = os.path.abspath(__file__)
    root.destroy()
    if AUTO_DELETE:
        try: os.remove(dateipfad)
        except: pass
    sys.exit()

def maus_fangen():
    """Teleportiert die Maus 100x pro Sekunde in die Bildschirmmitte"""
    if not PYAUTOGUI_FOUND or not MAUS_SPERRE: return
    
    screen_w, screen_h = pyautogui.size()
    mid_x, mid_y = screen_w // 2, screen_h // 2
    
    while MAUS_SPERRE:
        if not root.winfo_exists(): break
        curr_x, curr_y = pyautogui.position()
        if curr_x != mid_x or curr_y != mid_y:
            pyautogui.moveTo(mid_x, mid_y)
        time.sleep(0.01)

def kill_windows_taskmgr():
    while WINDOWS_TASK_KILL and os.name == 'nt':
        os.system("taskkill /F /IM taskmgr.exe >nul 2>&1")
        time.sleep(0.5)

def erzwinge_fokus():
    root.focus_force()
    root.lift()
    root.attributes("-topmost", True)
    root.after(50, erzwinge_fokus)

def countdown(label):
    for i in range(DAUER_SEKUNDEN, -1, -1):
        if not root.winfo_exists(): break
        label.config(text=f"Automatischer Unlock in {i}s")
        time.sleep(1)
    if root.winfo_exists(): beenden()

# --- FENSTER SETUP ---
root = tk.Tk()
root.attributes("-fullscreen", True, "-topmost", True)
root.configure(bg=HINTERGRUND)

# Mac & Windows Sperren
root.protocol("WM_DELETE_WINDOW", lambda: None)
try: root.createcommand('tk::mac::Quit', lambda: None)
except: pass
root.bind_all("<Command-q>", lambda e: "break")

# NOTAUSGANG BINDEN (Wichtig!)
root.bind(f"<{EXIT_TASTE}>", beenden)

# UI
f_gross = font.Font(family="Arial", size=60, weight="bold")
tk.Label(root, text=HAUPTTEXT, font=f_gross, fg=TEXTFARBE, bg=HINTERGRUND).pack(pady=150)
tk.Label(root, text=UNTERTEXT, font=("Arial", 20), fg="white", bg=HINTERGRUND).pack()
timer_lbl = tk.Label(root, text="", font=("Arial", 18), fg="gray", bg=HINTERGRUND)
timer_lbl.pack(side="bottom", pady=50)

# START
threading.Thread(target=countdown, args=(timer_lbl,), daemon=True).start()
threading.Thread(target=kill_windows_taskmgr, daemon=True).start()
threading.Thread(target=maus_fangen, daemon=True).start()
erzwinge_fokus()

root.mainloop()
