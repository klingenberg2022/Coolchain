#---------------------------------------------
#IoT-Kühlkettenüberwachung – Projektstufe 2
#Version 2.0  
#Autor: Burak Demirci
#       Jan Von der Heide
#       Malte Wessels
#       Tim Klingenberg
#       Fatih Kara
#       Marcel Rzondza
#------------------------------------------------------------------------------------------------------------

import pyodbc  # Importiert das pyodbc-Modul für die Datenbankverbindung.
from datetime import timedelta, datetime  # Importiert timedelta und datetime für die Arbeit mit Zeitangaben.
import requests  # Importiert das requests-Modul für HTTP-Anfragen.
from Crypto.Cipher import AES  # Importiert AES für die Verschlüsselung.
from Crypto.Util.Padding import unpad  # Importiert unpad für das Entfernen von Padding.
#------------------------------------------------------------------------------------------------------------

#Inizalisierung
tempdatasql = []
transportstation_data =[]
key = b'mysecretpassword'  # 16 Byte Passwort
iv = b'passwort-salzen!'   # 16 Byte Initialization Vektor

cipher = AES.new(key, AES.MODE_CBC, iv)  # Initialize encryption

# API-Schlüssel und Standortinformationen
api_key = "WRWDCV4PS8X4A27XRMM3F4ESP"  # Stellen Sie sicher, dass dieser Schlüssel korrekt ist

#Aufgabe 1
def sql_verbindung_v_tempdata():
    
    # Verbindungsdaten zur SQL Datenbank
    server = 'sc-db-server.database.windows.net'
    database = 'supplychain'  # Der Name der Datenbank
    username = 'rse'
    password = 'Pa$$w0rd'
    # Verbindungsstring zur SQL-Datenbank
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )

    # Verbindung zur Datenbank herstellen
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # SQL-Statement ausführen, um eindeutige Transport IDs, Temperaturen, Datum und Zeit abzurufen
    cursor.execute('SELECT * FROM v_tempdata ORDER BY transportstationID, transportstation, datetime, temperature ')

    # Liste für Transport IDs mit richtigen Temperaturen und eine für abweichende Temperaturen erstellen
    # Ergebnisse verarbeiten
    for row in cursor:
        
        tempdatasql.append(row)
    # Verbindung schließen
    cursor.close()
    conn.close()
    return tempdatasql

def temperaturueberwachung_kuehlstation(tempdatasql):
    richtige_ids= set()
    abweichende_daten= set()
    for x in range(len(tempdatasql)): 
        # Transport IDs mit Temperaturen im richtigen Bereich zu den richtigen IDs hinzufügen
            if 2 <= tempdatasql[x][4] <= 4:
        # richtige_ids.add(transportstationID)
                richtige_ids.add(tempdatasql[x][0] )
        # Transport IDs mit abweichenden Temperaturen und den zugehörigen Daten speichern
            else:
                abweichende_daten.add(tempdatasql[x][0])
    # Richtige IDs ausgeben
    print("Aufgabe 1: Temperaturüberwachung der Kühlstationen")
    print("korrekte Transport IDs:", richtige_ids)

    # Abweichende Daten ausgeben
    print("\nAbweichende Transport IDs" ,abweichende_daten)

    for a in range (len(tempdatasql)):
        if tempdatasql[a][0] in abweichende_daten:
            if not 2 <= tempdatasql[a][4] <= 4:
                print("Transport ID:",tempdatasql[a][0], "Abweichende Temperatur:", tempdatasql[a][4], "°C, Datum/Uhrzeit:", tempdatasql[a][3]) #Ausgabe der Fehlerhaften Einträge
    return tempdatasql

sql_verbindung_v_tempdata()
temperaturueberwachung_kuehlstation(tempdatasql)
#---------------------------------------------------------------------------------------------------------


#Aufgabe 2 und 3 zusammen

# Entschlüsselungsfunktion
def decrypt_value(encrypted_data): 
        return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode() 

def datenbank_abfragen():
    print()
    print()
    print("Aufgabe 2 und 3: Lieferdatenverschlüsselung mit Wetterdatenabfrage an den Auslagerorten:")
    print()
    # Definiert eine Funktion, die keine Argumente nimmt.
    server = 'sc-db-server.database.windows.net'  # Serveradresse.
    database = 'supplychain'  # Name der Datenbank.
    username = 'rse'  # Benutzername für die Datenbank.
    password = 'Pa$$w0rd'  # Passwort für die Datenbank.
    # Aufbau des Verbindungsstrings für ODBC.
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )

    conn = pyodbc.connect(conn_str)  # Stellt die Verbindung zur Datenbank her.
    cursor = conn.cursor()  # Erstellt einen Cursor, um Befehle auszuführen.

    cursor.execute('SELECT * FROM v_coolchain ORDER BY transportstation, transportid, datetime')
    # Führt SQL-Befehl aus, um Daten zu holen und nach bestimmten Spalten zu ordnen.
    v_coolchain_data = [row for row in cursor]
    # Speichert die abgefragten Daten in einer Liste.

    #cursor.execute('SELECT transportstationID, transportstation, category, plz FROM transportstation ORDER BY transportstationID')
    cursor.execute('SELECT transportstationID, transportstation, category, plz FROM transportstation_crypt  ORDER BY transportstationID')
    # Führt einen weiteren SQL-Befehl aus, um Daten von der Tabelle 'transportstation' zu holen.

    # For each row, decrypt and print the company
    for row in cursor.fetchall():
        transportstationID, encrypted_transportstation, encrypted_category, encrypted_plz = row
        decrypted_transportstation = decrypt_value(encrypted_transportstation)  # Assuming the encrypted data is in the first column directly
        decrypted_category = decrypt_value(encrypted_category)
        decrypted_plz = decrypt_value(encrypted_plz)
        data =[transportstationID, decrypted_transportstation, decrypted_category,decrypted_plz ]
        transportstation_data.append(data)
    #transportstation_data = [row for row in cursor]
    # Speichert die Ergebnisse in einer anderen Liste.

    cursor.close()  # Schließt den Cursor.
    conn.close()  # Schließt die Verbindung zur Datenbank.

    return v_coolchain_data, transportstation_data
    # Gibt die abgefragten Daten zurück.

def datenverarbeitung_aufgabe_zwei(v_coolchain_data):
    # Definiert eine weitere Funktion, die die Daten von 'v_coolchain_data' verarbeitet.
    idliste = []  # Initialisiert eine Liste, um eindeutige IDs zu speichern.
    liste_abfrage = []  # Liste, um Abfragedaten zu speichern.
    ergebnis_aufgabe_zwei = []  # Liste für die Endresultate.

    for i in range(len(v_coolchain_data)-1):
        if v_coolchain_data[i][2] not in idliste:
            idliste.append(v_coolchain_data[i][2])
            # Fügt eindeutige IDs zur Liste hinzu.

    for z in range(len(idliste)-1):
        for x in range(len(v_coolchain_data) - 1):
            if idliste[z] == v_coolchain_data[x][2]:
                liste_abfrage.append(v_coolchain_data[x])
                # Sammelt Daten für jede ID.

        for w in range(len(liste_abfrage)-1):
            liste_abfrage.sort(key=lambda x: x[5])
            # Sortiert die Daten nach der sechsten Spalte (Datum/Uhrzeit).
            if liste_abfrage[w][2] == liste_abfrage[w+1][2] and liste_abfrage[w][4] == "'out'" and liste_abfrage[w+1][4] == "'in'":
                if liste_abfrage[w+1][5] - liste_abfrage[w][5] > timedelta(minutes=10):
                    time = liste_abfrage[w+1][5] - liste_abfrage[w][5]
                    datum = liste_abfrage[w][5]  # Speichert das Datum der Transaktion.
                    ergebnis_aufgabe_zwei.append((liste_abfrage[w][2], liste_abfrage[w][1], datum))
                    # Speichert das Ergebnis, wenn die Bedingungen erfüllt sind.
        liste_abfrage.clear()
        # Leert die Liste für den nächsten Durchlauf.

    return ergebnis_aufgabe_zwei
    # Gibt die finalen Ergebnisse zurück.

def pruefe_uebereinstimmungen_und_gebe_plz_aus(ergebnisse, transportstation_data):
    locations = []  # Liste zum Speichern der formatierten Ergebnisse
    for ergebnis in ergebnisse:
        fehler_id, fehler_station, fehler_datum = ergebnis  # Zerlegt jedes Ergebnis in ID, Station und Datum
        formatted_date = fehler_datum.strftime('%Y-%m-%d')  # Formatieren des Datums in lesbares Format
        for station in transportstation_data:
            station_id, station_name, _, plz = station  # Zerlegen der Stationdaten
            if fehler_station.strip().lower() == station_name.strip().lower():
                # Überprüft, ob die Station aus den Ergebnissen mit einer in den Daten übereinstimmt
                location = f"{station_name} {plz},DE {formatted_date} {fehler_id}"  # Formatierung der Ausgabe
                locations.append(location)  # Fügt die formatierte Zeile zur Liste hinzu
    return locations  # Gibt die Liste der formatierten Standortinformationen zurück

def wetterdaten_abrufen(api_key, locations):
    
    for location_info in locations:
        parts = location_info.rsplit(' ', 3)  # Trennt die letzte Zeile in ihre Bestandteile
        station_name, plz_country, date, fehler_id = parts  # Speichert die einzelnen Teile
        datetime_str = "10.07.2023 13:00"  # Definiert ein festes Datum und Zeit
        datetime_obj = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')  # Konvertiert den String in ein datetime-Objekt
        timestamp = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')  # Konvertiert das datetime-Objekt in einen String

        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{plz_country}/{timestamp}'
        # Erstellt die URL für die Wetterdatenabfrage
        response = requests.get(url, params={'unitGroup': 'metric', 'key': api_key, 'include': 'hours'})
        # Sendet die Anfrage

        if response.status_code == 200:
            data = response.json()  # Wandelt die Antwort in JSON um
            if "days" in data and len(data["days"]) > 0:
                print(f"\nTemperatur in {station_name} ({plz_country}) am {date}, Fehler ID: {fehler_id}: ", data["days"][0]["temp"], "°C\n")
                # Gibt die Temperatur aus, wenn Daten vorhanden sind
            else:
                print(f"Keine Temperaturdaten gefunden für {station_name} ({plz_country}) am {date}, Fehler ID: {fehler_id}.")
        else:
            print(f"Fehler bei der Anfrage an {station_name} ({plz_country}) am {date}, Fehler ID: {fehler_id}: {response.status_code} - {response.text}")
            # Gibt einen Fehler aus, wenn die Anfrage nicht erfolgreich war

# Aufruf der Funktionen
v_coolchain_data, transportstation_data = datenbank_abfragen()
# Ruft die Funktion auf und speichert die Rückgabewerte.
fehlerergebnisse = datenverarbeitung_aufgabe_zwei(v_coolchain_data)  # Führt die Datenverarbeitung durch
locations = pruefe_uebereinstimmungen_und_gebe_plz_aus(fehlerergebnisse, transportstation_data)  # Ermittelt Übereinstimmungen
wetterdaten_abrufen(api_key, locations)  # Ruft Wetterdaten ab


