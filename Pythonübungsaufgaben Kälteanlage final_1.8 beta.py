#-----------------------------------
#Version 1.8 beta
#Aufgabe Kühlkette 
#Stand 06.05.2024
#-----------------------------------
"""
Gruppe: 
Burak
Tim
Marcel
Malte
Jan
Fathi
"""
import pyodbc
from datetime import timedelta

from Crypto.Cipher import AES 
from Crypto.Util.Padding import unpad 

# Initialisierung 
key = b'mysecretpassword'                
iv  = b'passwort-salzen!'   

datasql= []

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

    # SQL-Statement ausführen mit ORDER BY für transportid und datetime
    cursor.execute('SELECT * FROM coolchain ORDER BY transportid, datetime')
    # Ergebnisse verarbeiten
    for row in cursor:
        datasql.append(row)                 # Rohdaten in eine Liste für Offline-Auswertung übertragen
# Überprüfen der Richtungsreihenfolge, der TransportID und der Transportstation
        
    cursor.close()
    conn.close()# Verbindung schließen     
    return datasql

def datenverarbeitung_aufgabe_eins(datasql):
    idliste =[]
    transportid =[]
    datetime =[]
    direction =[]
    transportstation =[]
    ergebnis_aufgabe_eins = []
    prev_transportid = None
    prev_direction = None
    prev_transportstation = None
    correct_output = {}  # Dictionary, um die bereits überprüften TransportIDs zu verfolgen
    fehlerhafte_transport_id = set()  # Set für fehlerhafte TransportIDs
    for i in range(len(datasql)):
            transportstation.append(datasql[i][3])
            transportid.append(datasql[i][2])
            direction.append(datasql[i][4])
            datetime.append(datasql[i][5])
            
            if datasql[i][2] not in idliste:
                idliste.append(datasql[i][2])
    

    for x in range(len(datasql)- 1):
                # Überprüfen, ob die TransportID korrekt ist
                if transportid[x] != prev_transportid:
                    # Wenn vorherige TransportID überprüft wurde, überprüfe den Status und gib die entsprechende Ausgabe aus
                    prev_transportid = transportid[x]
                    if prev_transportid is None:
                    
                        if prev_transportid not in fehlerhafte_transport_id:
                            print(f"Fehler ID {prev_transportid} Fehlerhaft")
                            fehlerhafte_transport_id.add(prev_transportid)
                    
                    prev_direction = None  # Zurücksetzen der vorherigen Richtung bei neuer TransportID
                    prev_transportstation = None  # Zurücksetzen der vorherigen Transportstation bei neuer TransportID
                    correct_output[transportid[x]] = True  # Setze den Wert für die aktuelle TransportID auf True

                if transportid[x] in fehlerhafte_transport_id:
                    continue  # Überspringe die Überprüfung für eine TransportID, wenn sie bereits als fehlerhaft markiert ist

                # Überprüfen, ob es einen Wechsel zwischen "in" und "out" gibt
                if prev_direction is not None and prev_direction == direction[x]:
                    print(f"Fehler ID {transportid[x]} Fehlerhafte Richtung um {datetime[x]}: zwei aufeinanderfolgende '{direction[x]}'")
                    correct_output[transportid[x]] = False  # Setze den Wert für die aktuelle TransportID auf False
                    fehlerhafte_transport_id.add(transportid[x])  # Markiere die TransportID als fehlerhaft
                    ergebnis_aufgabe_eins.append(transportid[x])

                # Überprüfen, ob "out" vor "in" auftritt
                if prev_direction == 'out' and direction[x] == 'in':
                    print(f"Fehler ID {transportid[x]} Fehlerhafte Richtung um {datetime[x]}: 'out' vor 'in'")
                    correct_output[transportid[x]] = False  # Setze den Wert für die aktuelle TransportID auf False
                    fehlerhafte_transport_id.add(transportid[x])  # Markiere die TransportID als fehlerhaft
                    ergebnis_aufgabe_eins.append(transportid[x])

                # Überprüfen, ob die Richtungsänderung an derselben Transportstation erfolgt
                if prev_direction == 'in' and direction[x] == 'out' and prev_transportstation != transportstation[x]:
                    print(f"Fehler ID {transportid[x]} Fehlerhafte Richtung um {datetime[x]}: 'in' zu 'out' an unterschiedlichen Transportstationen")
                    ergebnis_aufgabe_eins.append(transportid[x])

                prev_direction = direction[x]
                prev_transportstation = transportstation[x]
                
                # Überprüfen und Ausgeben des Status für die letzte TransportID
                if prev_transportid is None:                
                    if prev_transportid not in fehlerhafte_transport_id:
                        print(f"Fehler ID {prev_transportid} Fehlerhaft")
                        fehlerhafte_transport_id.add(prev_transportid)
                        ergebnis_aufgabe_eins.append(fehlerhafte_transport_id)

    return ergebnis_aufgabe_eins
                       
def datenverarbeitung_aufgabe_zwei(datasql):
                # Listen für Dateninitialisierung
    idliste = []            # Eine Liste aller eindeutigen IDs
    liste_abfrage = []      # Eine Liste für die Abfrageergebnisse
    ergebnis_aufgabe_zwei = []           # Eine Liste für Ergebnisse der dritten Aufgabe (fehlerhafte IDs)

    # Datenverarbeitung

    # Eine Liste mit allen eindeutigen Produkten erstellen
    for i in range(len(datasql)):
        if datasql[i][2] not in idliste:
            idliste.append(datasql[i][2])   #i => Zeile ; 1 => Spalte
    

    # Jedes Produkt einzeln verarbeiten
    for z in range(len(idliste)):
        for x in range(len(datasql)):
            if idliste[z] in datasql[x]:
                liste_abfrage.append(datasql[x])  # Abfrageergebnisse für jedes Produkt hinzufügen

        for w in range (len(liste_abfrage)-1):
            liste_abfrage.sort(key=lambda liste_abfrage: liste_abfrage[5])  #Sortierung der Einträge der IDs nach Zeit
            if liste_abfrage [w][1]== liste_abfrage [w+1][1]: #abfrage der beiden ids ob gleich 
                if liste_abfrage[w][4] == "'out'" and liste_abfrage[w+1][4] == "'in'": #Abfrage ob erste id auschecken ist
                    if liste_abfrage[w+1][5] - liste_abfrage[w][5]> timedelta(minutes=10): #Abfrage ob abstand über 10 Min ist
                        time = liste_abfrage[w+1][5] - liste_abfrage[w][5] 
                        print("Fehler ID",liste_abfrage[w][2],"Kühlkette unterbrochen, Zeitüberschreitung >10 Minuten, Dauer:",time)
                        ergebnis_aufgabe_zwei.append(liste_abfrage[0][2])  # Ergebnisliste für Produkte, die die Transportdauer überschreiten
        liste_abfrage.clear()
    return ergebnis_aufgabe_zwei
 
def datenverarbeitung_aufgabe_drei(datasql):
    # Listen für Dateninitialisierung
    idliste = []            # Eine Liste aller eindeutigen IDs
    liste_abfrage = []      # Eine Liste für die Abfrageergebnisse
    ergebnis_aufgabe_drei = []           # Eine Liste für Ergebnisse der dritten Aufgabe (fehlerhafte IDs)

    #Daten sortiern
    datasql.sort(key=lambda datasql: datasql[5])  # Rohdaten nach Datum und Uhrzeit sortieren

    # Eine Liste mit allen eindeutigen Produkten erstellen
    for i in range(len(datasql)):
        if datasql[i][2] not in idliste:
            idliste.append(datasql[i][2])   #i => Zeile ; 1 => Spalte

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
            ergebnis_aufgabe_drei.append(liste_abfrage[0][2])  # Ergebnisliste für Produkte, die die Transportdauer überschreiten
        # Abfrage Liste leeren       
        liste_abfrage.clear()
        time = 0
        
    ergebnis_aufgabe_drei = " ".join(ergebnis_aufgabe_drei) #Klammern entfernen
    print("Fehler ID", ergebnis_aufgabe_drei, " Transportdauer von 48 Stunden überschritten") #Ausgabe
    return ergebnis_aufgabe_drei

def datenverarbeitung_korrekt_ergebnisse(datasql, ergebnis_aufgabe_eins, ergebnis_aufgabe_zwei, ergebnis_aufgabe_drei):
    korrekte_ids = []
    idliste = []

    for i in range(len(datasql)):
        if datasql[i][2] not in idliste:
            idliste.append(datasql[i][2])

    for j in range(len(idliste)):
        if idliste[j] not in ergebnis_aufgabe_eins and idliste[j] not in ergebnis_aufgabe_zwei and idliste[j] not in ergebnis_aufgabe_drei:
            korrekte_ids.append(idliste[j])
    
    for g in range(len(korrekte_ids)):              #Ausgabe aller richtigen Ergebnisse
        print(f"Korrekte ID {korrekte_ids[g]}")
         
    return korrekte_ids, ergebnis_aufgabe_eins, ergebnis_aufgabe_zwei, ergebnis_aufgabe_drei

sql_datenbank_verbindung()
ergebnis_aufgabe_eins = datenverarbeitung_aufgabe_eins(datasql)
ergebnis_aufgabe_zwei = datenverarbeitung_aufgabe_zwei(datasql)
ergebnis_aufgabe_drei = datenverarbeitung_aufgabe_drei(datasql)
datenverarbeitung_korrekt_ergebnisse(datasql, ergebnis_aufgabe_eins, ergebnis_aufgabe_zwei, ergebnis_aufgabe_drei)
