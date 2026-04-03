import tkinter as tk
from tkinter import font
import threading
import time
import os
import sys

# ─── ANPASSBAR (KONFIGURATION) ───────────────────────
DAUER_SEKUNDEN = 120       
HAUPTTEXT = "SYSTEM GESPERRT"
UNTERTEXT = "Sicherheits-Protokoll aktiv..."
HINTERGRUND = "black"
TEXTFARBE = "red"
AUTO_DELETE = True         

# ZUSATZFUNKTIONEN
WINDOWS_TASK_KILL = True   
MAC_ULTRA_LOCK = True      # Schaltet den extremen Fokus-Zwang für Mac ein
# ─────────────────────────────────────────────────────

def beenden():
    dateipfad = os.path.abspath(__file__)
    root.destroy()
    if AUTO_DELETE:
        try: os.remove(dateipfad)
        except: pass
    sys.exit()

def kill_windows_taskmgr():
    while WINDOWS_TASK_KILL and os.name == 'nt':
        os.system("taskkill /F /IM taskmgr.exe >nul 2>&1")
        time.sleep(0.5)

def erzwinge_fokus():
    """Hält das Fenster mit Gewalt im Vordergrund"""
    root.focus_force()
    root.lift()
    root.attributes("-topmost", True)
    # Intervall auf 50ms verkürzt für maximale Aggressivität auf dem Mac
    root.after(50, erzwinge_fokus)

def countdown(label):
    for i in range(DAUER_SEKUNDEN, -1, -1):
        if not root.winfo_exists(): break
        label.config(text=f"Automatischer Unlock in {i}s")
        time.sleep(1)
    if root.winfo_exists(): beenden()

root = tk.Tk()
root.title("System Alert")

# --- DER MAC-TRICK: OVERRIDEREDIRECT ---
# Dies entfernt die Menüleiste und das Dock im Vordergrund komplett.
if sys.platform == "darwin" and MAC_ULTRA_LOCK:
    root.overrideredirect(True) 

root.attributes("-fullscreen", True, "-topmost", True)
root.configure(bg=HINTERGRUND)

# SPERREN
root.protocol("WM_DELETE_WINDOW", lambda: None)
try: root.createcommand('tk::mac::Quit', lambda: None)
except: pass

root.bind_all("<Command-q>", lambda e: "break")
root.bind_all("<Command-Option-Escape>", lambda e: "break") # Funktioniert selten, aber schadet nicht
root.bind_all("<Alt-Tab>", lambda e: "break")

# UI
f_gross = font.Font(family="Arial", size=60, weight="bold")
tk.Label(root, text=HAUPTTEXT, font=f_gross, fg=TEXTFARBE, bg=HINTERGRUND).pack(pady=150)
timer_lbl = tk.Label(root, text="", font=("Arial", 18), fg="gray", bg=HINTERGRUND)
timer_lbl.pack(side="bottom", pady=50)

# Versteckter EXIT-Button
tk.Button(root, text="EXIT", command=beenden, bg=HINTERGRUND, fg="#0a0a0a", borderwidth=0).place(relx=0.98, rely=0.98, anchor="center")

# START
threading.Thread(target=countdown, args=(timer_lbl,), daemon=True).start()
threading.Thread(target=kill_windows_taskmgr, daemon=True).start()
erzwinge_fokus()

root.mainloop()
