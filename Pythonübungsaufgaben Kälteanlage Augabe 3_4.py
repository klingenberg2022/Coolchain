#-----------------------------------
#Version 1.4
#Kätemittelanlage 
#Aufgabe 3
#Stand 02.03.2024
#-----------------------------------
"""
Gruppe: 
Tim
Burak
"""
# Import von erforderlichen Bibliothekenfrom datetime import timedelta
import pyodbc
from datetime import timedelta

# Liste für Dateninitialisierung
datasql = []            # Eine leere Liste für Rohdaten aus der SQL-Datenbank

def sql_datenbank_verbindung():

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

    # SQL-Abfrage ausführen
    cursor.execute('SELECT * FROM coolchain')

    # Ergebnisse verarbeiten
    for row in cursor:
        datasql.append(row)                 # Rohdaten in eine Liste für Offline-Auswertung übertragen

    # Verbindung schließen
    cursor.close()
    conn.close()
    return datasql

def datenverarbeitung_aufgabe_drei(datasql):
    # Listen für Dateninitialisierung
    idliste = []            # Eine Liste aller eindeutigen IDs
    liste_abfrage = []      # Eine Liste für die Abfrageergebnisse
    ergebnis_aufgabe_drei = []           # Eine Liste für Ergebnisse der dritten Aufgabe (fehlerhafte IDs)

    #Daten sortiern
    datasql.sort(key=lambda datasql: datasql[5])  # Rohdaten nach Datum und Uhrzeit sortieren

    # Eine Liste mit allen eindeutigen Produkten erstellen
    for i in range(len(datasql)-1):
        if datasql[i][1] not in idliste:
            idliste.append(datasql[i][1])   #i => Zeile ; 1 => Spalte

    # Jedes Produkt einzeln verarbeiten
    for z in range(len(idliste)-1):
        for x in range(len(datasql) - 1):
            if idliste[z] in datasql[x]:
                liste_abfrage.append(datasql[x])  # Abfrageergebnisse für jedes Produkt hinzufügen
                y = len(liste_abfrage) - 1
        # Zeit des Produkts vom ersten bis zum letzten Datensatz abrufen
        time = liste_abfrage[y][5] - liste_abfrage[0][5]
        # Überprüfen, ob das Produkt länger als zwei Tage unterwegs ist
        if time > timedelta(days=2):
            ergebnis_aufgabe_drei.append(liste_abfrage[0][1])  # Ergebnisliste für Produkte, die die Transportdauer überschreiten
        # Abfrage Liste leeren       
        liste_abfrage.clear()
        time = 0
        
    ergebnis_aufgabe_drei = " ".join(ergebnis_aufgabe_drei) #Klammern entfernen
    print("Fehler ID", ergebnis_aufgabe_drei, " Transportdauer von 48 Stunden überschritten") #Ausgabe
    return ergebnis_aufgabe_drei

sql_datenbank_verbindung()
datenverarbeitung_aufgabe_drei(datasql)

