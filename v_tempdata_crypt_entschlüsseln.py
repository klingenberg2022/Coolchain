#v_tempdata_crypt_entschlüsseln
import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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
