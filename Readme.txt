**README**

Dieses Repository enthält Python-Code zur Verarbeitung von Daten aus einer SQL-Datenbank im Kontext einer Kältemittelanlage. 
Der Code adressiert spezifische Aufgaben im Zusammenhang mit der Datenverarbeitung und Fehlererkennung während des Transports von Kältemitteln.

### Funktionsweise

1. **Datenabruf und -verarbeitung**
    - Die Funktion `sql_datenbank_verbindung()` stellt eine Verbindung zur SQL-Datenbank her und ruft die benötigten Daten ab.
    - Die Daten werden in der globalen Liste `datasql` gespeichert.
   
2. **Datenverarbeitung für Aufgabe eins**
    - Die Funktion `datenverarbeitung_aufgabe_eins(datasql)` überprüft die Transport-IDs, Richtungen, Zeitstempel und Transportstationen, um etwaige Fehler in den Daten zu erkennen.
   
3. **Datenverarbeitung für Aufgabe zwei**
    - Die Funktion `datenverarbeitung_aufgabe_zwei(datasql)` identifiziert mögliche Unterbrechungen in der Kühlkette, indem sie die Transportdauern zwischen Ein- und Ausgängen überprüft.
   
4. **Datenverarbeitung für Aufgabe drei**
    - Die Funktion `datenverarbeitung_aufgabe_drei(datasql)` ermittelt Transporte, deren Dauer mehr als 48 Stunden beträgt, und gibt die entsprechenden Transport-IDs aus.

5. **Datenverarbeitung für Korrekte Ergebnisse**
    - Die Funktion datenverarbeitung_korrekt_ergebnisse(datasql, ergebnis_aufgabe_eins, ergebnis_aufgabe_zwei, ergebnis_aufgabe_drei) ermittelt die IDs die den Transportbediengungen entsprechen.
### Anforderungen

Um den Code auszuführen, müssen die folgenden Pakete installiert sein:
- `pyodbc`: Zur Verbindung mit der SQL-Datenbank und Ausführung von Abfragen.
- `datetime`: Zur Verarbeitung von Datum und Uhrzeit.

### Verwendung

1. Sicherstellen, dass die erforderlichen Pakete installiert sind.
2. Die Verbindungsdaten zur SQL-Datenbank (`server`, `database`, `username`, `password`) in der Funktion `sql_datenbank_verbindung()` anpassen.
3. Den Code ausführen, um die definierten Aufgaben zu bearbeiten.

### Beispiel

Ein Beispiel für die Ausführung des Codes:

```python
import pyodbc
from datetime import timedelta

# Verbindung zur SQL-Datenbank herstellen und Daten abrufen
sql_datenbank_verbindung()

# Datenverarbeitung für Aufgabe eins durchführen
datenverarbeitung_aufgabe_eins(datasql)

# Datenverarbeitung für Aufgabe zwei durchführen
datenverarbeitung_aufgabe_zwei(datasql)

# Datenverarbeitung für Aufgabe drei durchführen
datenverarbeitung_aufgabe_drei(datasql)
# Datenverarbeitung für die Ausgabe der Korrekten Ergebnisse durchführen
datenverarbeitung_korrekt_ergebnisse(datasql, ergebnis_aufgabe_eins, ergebnis_aufgabe_zwei, ergebnis_aufgabe_drei)
```

### Autor

Dieser Code wurde von Tim K.+N entwickelt.

### Lizenz

Dieser Code ist unter der Tim K+N  lizenziert.

Für weitere Informationen und Support kontaktieren Sie bitte den Support :(#).