import pyodbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Initialization
key = b'mysecretpassword'  # 16 Byte Passwort
iv = b'passwort-salzen!'  # 16 Byte Initialization Vektor
cipher = AES.new(key, AES.MODE_CBC, iv)  # Initialize encryption

# Decryption function
def decrypt_value(encrypted_data):
    return unpad(cipher.decrypt(encrypted_data),AES.block_size).decode()

# Connection details
server = 'sc-db-server.database.windows.net'
database = 'supplychain'
username = 'rse'
password = 'Pa$$w0rd'
datasql=[]
#0x46b0+col,0x01,0x9960+col,0x0a
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
select_query = 'SELECT company, transportstation,transportID, category,direction, datetime FROM v_coolchain_crypt'
cursor.execute(select_query)
print(select_query)
# For each row, decrypt and print the company
for row in cursor.fetchall():
    encrypted_company, encrypted_transportstation, transportID, encrypted_category, direction, datetime = row
    print(encrypted_company)
    print(encrypted_transportstation)
    decrypted_company = decrypt_value(encrypted_company) # Assuming the encrypted data is in the first column directly
    print(decrypted_company)
    decrypted_transportstation = decrypt_value(encrypted_transportstation) 
    decrypted_category = decrypt_value(encrypted_category)
    data =[decrypted_company, decrypted_transportstation,transportID, decrypted_category, datetime ]
    datasql.append(data)

print(f"{decrypted_company }")

# Close connection
cursor.close()
conn.close()