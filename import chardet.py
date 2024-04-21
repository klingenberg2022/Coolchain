
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Initialisierung
key = b'mysecretpassword'  # 16 Byte Passwort
iv = b'passwort-salzen!'  # 16 Byte Initialisierungsvektor
cipher = AES.new(key, AES.MODE_CBC, iv)  # Verschlüsselung initialisieren

# Verschlüsselter Text
ciphertext = b'T\x7f\rv\x96\x86n]+]P¥ì?8-ldesheim'  
# Verschlüsselter Text

# Entschlüsselung
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)  # Text entschlüsseln

# Ausgabe
print("Entschlüsselter Text als String: ", plaintext.decode())
