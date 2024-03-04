#-----------------------------------
#Version 1.2
#Aufgabe 2
#Kätemittelanlage 
#Stand 02.03.2024
#-----------------------------------
"""
Gruppe: 
Jan+1
"""
# Import von erforderlichen Bibliotheken from datetime import timedelta
datasql = []            # Eine leere Liste für Rohdaten aus der SQL-Datenbank
import pyodbc
from datetime import timedelta
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

def datenverarbeitung_aufgabe_zwei(datasql):
                # Listen für Dateninitialisierung
    idliste = []            # Eine Liste aller eindeutigen IDs
    liste_abfrage = []      # Eine Liste für die Abfrageergebnisse
    ergebnis_aufgabe_zwei = []           # Eine Liste für Ergebnisse der dritten Aufgabe (fehlerhafte IDs)

    # Datenverarbeitung

    # Eine Liste mit allen eindeutigen Produkten erstellen
    for i in range(len(datasql)-1):
        if datasql[i][1] not in idliste:
            idliste.append(datasql[i][1])   #i => Zeile ; 1 => Spalte

    # Jedes Produkt einzeln verarbeiten
    for z in range(len(idliste)-1):
        for x in range(len(datasql) - 1):
            if idliste[z] in datasql[x]:
                liste_abfrage.append(datasql[x])  # Abfrageergebnisse für jedes Produkt hinzufügen

        for w in range (len(liste_abfrage)-1):
            liste_abfrage.sort(key=lambda liste_abfrage: liste_abfrage[5])  #Sortierung der Einträge der IDs nach Zeit
            if liste_abfrage [w][1]== liste_abfrage [w+1][1]: #abfrage der beiden ids ob gleich 
                if liste_abfrage[w][4] == "'out'" and liste_abfrage[w+1][4] == "'in'": #Abfrage ob erste id auschecken ist
                    if liste_abfrage[w+1][5] - liste_abfrage[w][5]> timedelta(minutes=10): #Abfrage ob abstand über 10 Min ist
                        time = liste_abfrage[w+1][5] - liste_abfrage[w][5]          
                        print("Fehler ID",liste_abfrage[w][1],"Kühlkette unterbrochen, Zeitüberschreitung >10 Minuten, Dauer:",time)
                        ergebnis_aufgabe_zwei.append(liste_abfrage[0][1])  # Ergebnisliste für Produkte, die die Transportdauer überschreiten
        liste_abfrage.clear()
    return ergebnis_aufgabe_zwei
    
sql_datenbank_verbindung()
datenverarbeitung_aufgabe_zwei(datasql)