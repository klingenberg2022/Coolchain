#
#V1.2
#
##
import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import pyodbc
from datetime import timedelta
transportstation_crypt_data = []
datasql= []
ergebnis_aufgabe_zweipunkt= []
# Initialization
key = b'mysecretpassword'  # 16 Byte Passwort
iv = b'passwort-salzen!'  # 16 Byte Initialization Vektor

cipher = AES.new(key, AES.MODE_CBC, iv)  # Initialize encryption


# Decryption function
def decrypt_value(encrypted_data): 
        return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode() 

def sql_verbindung_transportstation_crypt():
    
        # Connection details
    server = 'sc-db-server.database.windows.net'
    database = 'supplychain'
    username = 'rse'
    password = 'Pa$$w0rd'
    
    # Connection string
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )

    # Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Read records
    select_query = 'SELECT transportstationID, transportstation, category, plz FROM transportstation_crypt'
    cursor.execute(select_query)
    print(select_query)
    # For each row, decrypt and print the company
    for row in cursor.fetchall():
        transportstationID, encrypted_transportstation, encrypted_category, encrypted_plz = row
        decrypted_transportstation = decrypt_value(encrypted_transportstation)  # Assuming the encrypted data is in the first column directly
        decrypted_category = decrypt_value(encrypted_category)
        decrypted_plz = decrypt_value(encrypted_plz)
        data =[transportstationID, decrypted_transportstation, decrypted_category,decrypted_plz ]
        transportstation_crypt_data.append(data)

    print(f"Company: {transportstation_crypt_data}")

    # Close connection
    cursor.close()
    conn.close()
    return transportstation_crypt_data



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
    cursor.execute('SELECT * FROM v_coolchain ORDER BY transportstation, transportid, datetime')
    # Ergebnisse verarbeiten
    for row in cursor:
        datasql.append(row)                 # Rohdaten in eine Liste für Offline-Auswertung übertragen
# Überprüfen der Richtungsreihenfolge, der TransportID und der Transportstation
        
    cursor.close()
    conn.close()# Verbindung schließen     
    return datasql
def datenverarbeitung_aufgabe_zwei(datasql):
                # Listen für Dateninitialisierung
    idliste = []            # Eine Liste aller eindeutigen IDs
    liste_abfrage = []      # Eine Liste für die Abfrageergebnisse
    ergebnis_aufgabe_zwei = []           # Eine Liste für Ergebnisse der dritten Aufgabe (fehlerhafte IDs)

    # Datenverarbeitung

    # Eine Liste mit allen eindeutigen Produkten erstellen
    for i in range(len(datasql)-1):
        if datasql[i][2] not in idliste:
            idliste.append(datasql[i][2])   #i => Zeile ; 1 => Spalte

    # Jedes Produkt einzeln verarbeiten
    for z in range(len(idliste)-1):
        for x in range(len(datasql) - 1):
            if idliste[z] in datasql[x]:
                liste_abfrage.append(datasql[x])  # Abfrageergebnisse für jedes Produkt hinzufügen

        for w in range (len(liste_abfrage)-1):
            liste_abfrage.sort(key=lambda liste_abfrage: liste_abfrage[5])  #Sortierung der Einträge der IDs nach Zeit
            if liste_abfrage [w][2]== liste_abfrage [w+1][2]: #abfrage der beiden ids ob gleich 
                if liste_abfrage[w][4] == "'out'" and liste_abfrage[w+1][4] == "'in'": #Abfrage ob erste id auschecken ist
                    if liste_abfrage[w+1][5] - liste_abfrage[w][5]> timedelta(minutes=10): #Abfrage ob abstand über 10 Min ist
                        time = liste_abfrage[w+1][5] - liste_abfrage[w][5] 
                        print("Fehler ID",liste_abfrage[w][2], "Transportstation ",liste_abfrage [w][1], "Kühlkette unterbrochen, Zeitüberschreitung >10 Minuten, Dauer:",time)
                        ergebnis_aufgabe_zwei.append(liste_abfrage[0][2] )  # Ergebnisliste für Produkte, die die Transportdauer überschreiten
                        ergebnis_aufgabe_zweipunkt.extend([liste_abfrage[0][2],liste_abfrage[0][1]])
    
        liste_abfrage.clear()
        return ergebnis_aufgabe_zwei, ergebnis_aufgabe_zweipunkt
    print(ergebnis_aufgabe_zwei)


#sql_verbindung_transportstation_crypt()
sql_datenbank_verbindung()
datenverarbeitung_aufgabe_zwei(datasql)
print(ergebnis_aufgabe_zweipunkt)
for r in range(len(ergebnis_aufgabe_zweipunkt)):
    if ergebnis_aufgabe_zweipunkt[r] in transportstation_crypt_data:
        print()

for r in range(len(ergebnis_aufgabe_zweipunkt)-1):
    if ergebnis_aufgabe_zweipunkt[r] in transportstation_crypt_data:
        print()