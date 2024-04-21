import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Initialization
key = b'mysecretpassword'  # 16 Byte Passwort
iv = b'passwort-salzen!'  # 16 Byte Initialisierungsvektor
cipher = AES.new(key, AES.MODE_CBC, iv)  # Verschlüsselung initialisieren

# Entschlüsselungsfunktion
def decrypt_value(encrypted_data):
    
    return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()

# Verbindungsdaten
server = 'sc-db-server.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'
datasql = []

# Verbindungszeichenfolge
conn_str = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

# Mit der Datenbank verbinden
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Datensätze lesen
select_query = 'SELECT company, transportstation, transportID, category, direction, datetime FROM v_coolchain_crypt'
cursor.execute(select_query)
print(select_query)

# Für jeden Datensatz entschlüsseln und die Firma ausgeben
for row in cursor.fetchall():
    encrypted_company, encrypted_transportstation, encrypted_transportID, decrypted_category, decrypted_direction, decrypted_datetime = row
    decrypted_company = decrypt_value(encrypted_company)  # Angenommen, die verschlüsselten Daten befinden sich direkt in der ersten Spalte
    decrypted_transportstation = decrypt_value(encrypted_transportstation)
    decrypted_transportID = decrypt_value(encrypted_transportID)
    data =[decrypted_company,decrypted_transportstation,decrypted_transportID]
    datasql.append(data)
    break
print(f"Firma: {datasql}")

# Verbindung schließen
cursor.close()
conn.close()
