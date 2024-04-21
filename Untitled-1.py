from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Initialisierung
key = b'mysecretpassword'  # 16 Byte Passwort
iv = b'passwort-salzen!'  # 16 Byte Initialization Vektor
cipher = AES.new(key, AES.MODE_CBC, iv)  # Verschlüsselung initialisieren

# Entschlüsselung
ciphertext = b'\x99\x89\xdc:\xb4\xeb\xd2\xee.\x11\xa5\xb9\x19\x8fLy'
plaintext = unpad(cipher.decrypt(ciphertext), 16)  # Text entschlüsseln

# Ausgabe
print('--------------------------------------------------------------------------')
print("Entschlüsselter Text als Bytewert: ", plaintext)
print("Entschlüsselter Text als String: ", plaintext.decode())
print('--------------------------------------------------------------------------')

"""from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
# Initialisierung
key = b'mysecretpassword' # 16 Byte Passwort
iv = b'passwort-salzen!' # 16 Byte Initialization Vektor
cipher = AES.new(key, AES.MODE_CBC, iv) # Verschlüsselung initialisieren
# Entschlüsselung
ciphertext = b'\xe0\xdc*\x84l\x87;p\xd22\xd9\x94\xabH6\xcd\xf0&\xeduO\x19\x17$+K*wke\x81\xdf\0x96'
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size) # Text entschlüsseln
# Ausgabe
print ('--------------------------------------------------------------------------')
print ("Entschlüsselter Text als Bytewert: ", plaintext)
print ("Entschlüsselter Text als String: ", plaintext.decode())
print ('--------------------------------------------------------------------------')"""