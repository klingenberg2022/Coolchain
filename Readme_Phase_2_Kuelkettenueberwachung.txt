**Readme für das IoT-Kühlkettenüberwachungsprojekt - Projektstufe 2**

**Version**: 2.0

**Autoren**: Burak Demirci, Jan Von der Heide, Malte Wessels, Tim Klingenberg, Fatih Kara, Marcel Rzondza

**Beschreibung**:
Dieses Projekt implementiert eine IoT-Kühlkettenüberwachung in Python. Die Überwachung erfolgt in zwei Hauptaufgaben: Temperaturüberwachung der Kühlstationen und Verschlüsselung von Lieferdaten mit Wetterdatenabfrage an den Auslagerorten.

**Benötigte Bibliotheken**:
- `pyodbc`: Für die Verbindung zur SQL-Datenbank.
- `datetime`: Zur Arbeit mit Zeitangaben.
- `requests`: Für HTTP-Anfragen.
- `Crypto.Cipher`: Für die AES-Verschlüsselung.
- `Crypto.Util.Padding`: Für das Entfernen von Padding.

**Initialisierung**:
- `tempdatasql`: Eine Liste für die SQL-Temperaturdaten.
- `key`: Ein 16-Byte-Passwort für die AES-Verschlüsselung.
- `iv`: Ein 16-Byte-Initialisierungsvektor.
- `transportstation_data`: Eine Liste für Transportstationsdaten.
- `cipher`: Eine AES-Verschlüsselungsinstant.

**Funktionen**:
1. `sql_verbindung_v_tempdata()`: Stellt eine Verbindung zur SQL-Datenbank her und ruft Temperaturdaten ab.
2. `temperaturueberwachung_kuehlstation(tempdatasql)`: Überprüft die Temperaturdaten auf Abweichungen und gibt sie aus.
3. `decrypt_value(encrypted_data)`: Entschlüsselt verschlüsselte Daten.
4. `datenbank_abfragen()`: Fragt Daten von der Datenbank ab und entschlüsselt sie.
5. `datenverarbeitung_aufgabe_zwei(v_coolchain_data)`: Verarbeitet die abgerufenen Daten für die zweite Aufgabe.
6. `pruefe_uebereinstimmungen_und_gebe_plz_aus(ergebnisse, transportstation_data)`: Überprüft Übereinstimmungen und gibt PLZ-Informationen aus.
7. `wetterdaten_abrufen(api_key, locations)`: Ruft Wetterdaten von Auslagerorten ab und gibt sie aus.

**Anleitung**:
- Stellen Sie sicher, dass die benötigten Bibliotheken installiert sind.
- Ändern Sie die Verbindungsparameter zur SQL-Datenbank entsprechend.
- Setzen Sie den richtigen API-Schlüssel für die Wetterdatenabfrage.
- Führen Sie den Code aus und befolgen Sie die Ausgaben.

**Beispielaufruf**:
```python
fehlerergebnisse = datenverarbeitung_aufgabe_zwei(v_coolchain_data)
locations = pruefe_uebereinstimmungen_und_gebe_plz_aus(fehlerergebnisse, transportstation_data)
wetterdaten_abrufen(api_key, locations)
```

Dieses Projekt demonstriert die Überwachung und Analyse von Temperatur- und Lieferdaten in einer Kühlkette sowie die Integration von Wetterdaten für weiterführende Analysen.