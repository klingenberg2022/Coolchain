#-----------------------------------
#Version 1.2
#Kätemittelanlage 
#Aufgabe 1
#Stand 02.03.2024
#-----------------------------------
"""
Gruppe: 
Marcel+1
"""
import pyodbc
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

    # SQL-Abfrage ausführen
    #cursor.execute('SELECT * FROM coolchain')
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
    prev_transportid = None
    prev_direction = None
    prev_transportstation = None
    correct_output = {}  # Dictionary, um die bereits überprüften TransportIDs zu verfolgen
    fehlerhafte_transport_id = set()  # Set für fehlerhafte TransportIDs

    for i in range(len(datasql)-1):
            transportid.append(datasql[i][1])
            direction.append(datasql[i][4])
            datetime.append(datasql[i][5])
            transportstation.append(datasql[i][2])
            if datasql[i][1] not in idliste:
                idliste.append(datasql[i][1])

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

                # Überprüfen, ob "out" vor "in" auftritt
                if prev_direction == 'out' and direction[x] == 'in':
                    print(f"Fehler ID {transportid[x]} Fehlerhafte Richtung um {datetime[x]}: 'out' vor 'in'")
                    correct_output[transportid[x]] = False  # Setze den Wert für die aktuelle TransportID auf False
                    fehlerhafte_transport_id.add(transportid[x])  # Markiere die TransportID als fehlerhaft

                # Überprüfen, ob die Richtungsänderung an derselben Transportstation erfolgt
                if prev_direction == 'in' and direction[x] == 'out' and prev_transportstation != transportstation[x]:
                    print(f"Fehler ID {transportid[x]} Fehlerhafte Richtung um {datetime[x]}: 'in' zu 'out' an unterschiedlichen Transportstationen")

                prev_direction = direction[x]
                prev_transportstation = transportstation[x]
                
                # Überprüfen und Ausgeben des Status für die letzte TransportID
                if prev_transportid is None:                
                    if prev_transportid not in fehlerhafte_transport_id:
                        print(f"Fehler ID {prev_transportid} Fehlerhaft")
                        fehlerhafte_transport_id.add(prev_transportid)

sql_datenbank_verbindung()
datenverarbeitung_aufgabe_eins(datasql)
