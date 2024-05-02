#---------------------------------------------
#Projekt: Temperaturueberwachung Kühlstation
#Version 2.0  
#Autor: Tim 
#---------------------------------------------
import pyodbc
tempdatasql = []

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
    print("korrekte Transport IDs:", richtige_ids)

    # Abweichende Daten ausgeben
    print("\nAbweichende Transport IDs" ,abweichende_daten)

    for a in range (len(tempdatasql)):
        if tempdatasql[a][0] in abweichende_daten:
            if not 2 <= tempdatasql[a][4] <= 4:
                print("Transport ID:",tempdatasql[a][0], "Abweichende Temperatur:", tempdatasql[a][4], "°C, Datum/Uhrzeit:", tempdatasql[a][3])

sql_verbindung_v_tempdata()
temperaturueberwachung_kuehlstation(tempdatasql)