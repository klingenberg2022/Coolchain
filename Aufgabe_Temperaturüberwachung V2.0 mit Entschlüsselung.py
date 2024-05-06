
#v_tempdata_crypt_entschlüsseln
import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
# Initialisierung 
key = b'mysecretpassword'                
iv  = b'passwort-salzen!'       

cipher = AES.new(key, AES.MODE_CBC, iv) 

datasql = []



# Initialization
key = b'mysecretpassword'  # 16 Byte Passwort
iv = b'passwort-salzen!'  # 16 Byte Initialization Vektor
cipher = AES.new(key, AES.MODE_CBC, iv)  # Initialize encryption

# Decryption function
def decrypt_value(encrypted_data):
    return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()

# Connection details
server = 'sc-db-server.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'
datasql=[]

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
select_query = 'SELECT transportstationID, transportstation, category, datetime, temperature FROM v_tempdata_crypt'
cursor.execute(select_query)
print(select_query)
# For each row, decrypt and print the company
for row in cursor.fetchall():
    transportstationID, encrypted_transportstation, encrypted_category, encrypted_datetime, encrypted_temperatur = row
    decrypted_transportstation = decrypt_value(encrypted_transportstation)  # Assuming the encrypted data is in the first column directly
    decrypted_category = decrypt_value(encrypted_category)
    decrypted_datetime = decrypt_value(encrypted_datetime)
    decrypted_temperatur =decrypt_value(encrypted_temperatur)
    data =[transportstationID, decrypted_transportstation, decrypted_category,decrypted_datetime,decrypted_temperatur]
    datasql.append(data)

print(f"Company: {datasql}")

# Close connection
cursor.close()
conn.close()













def temperaturueberwachung_kuehlstation():
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
    cursor.execute('SELECT transportstationID, temperature, datetime FROM tempdata')

    # Liste für Transport IDs mit richtigen Temperaturen und eine für abweichende Temperaturen erstellen
    richtige_ids = set()
    abweichende_daten = {}

    # Ergebnisse verarbeiten
    for row in cursor:
        transportstationID, temperature, datetime = row
        # Transport IDs mit Temperaturen im richtigen Bereich zu den richtigen IDs hinzufügen
        if 2 <= temperature <= 4:
            richtige_ids.add(transportstationID)
        # Transport IDs mit abweichenden Temperaturen und den zugehörigen Daten speichern
        else:
            abweichende_daten.setdefault(transportstationID, []).append((temperature, datetime))

    # Verbindung schließen
    cursor.close()
    conn.close()

    # Rückgabe der richtigen Transport IDs und der abweichenden Daten
    return richtige_ids, abweichende_daten

# Funktion aufrufen, um die Transport IDs mit den Temperaturen und Daten zu erhalten
richtige_ids, abweichende_daten = temperaturueberwachung_kuehlstation()

# Richtige IDs ausgeben
print("Richtige Transport IDs:")
for transport_id in richtige_ids:
    print("Transport ID:", transport_id)

# Abweichende Daten ausgeben
print("\nAbweichende Transport IDs:")
for transport_id, data in abweichende_daten.items():
    print("Transport ID:", transport_id, "Abweichende Daten:")
    for temperature, datetime in data:
        print("  Temperatur:", temperature, "°C, Datum/Uhrzeit:", datetime)

