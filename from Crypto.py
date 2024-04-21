from Crypto.Cipher import AES
import base64

# Funktion zur Ermittlung des Verschlüsselungsvektors und des Verschlüsselungscodes
def find_aes_parameters(plaintext, ciphertext):
    # Dekodieren des Base64-codierten verschlüsselten Texts
    ciphertext = base64.b64decode(ciphertext)
    
    # Iteration über mögliche Schlüssellängen (128, 192 oder 256 Bit)
    for key_length in (16, 24, 32):
        # Iteration über mögliche Verschlüsselungsmodi
        for mode in (AES.MODE_CBC, AES.MODE_ECB, AES.MODE_OFB, AES.MODE_CFB, AES.MODE_CTR):
            # Verwendung des unverschlüsselten Texts und des Verschlüsselungsmodus, um eine AES-Verschlüsselung zu initialisieren
            cipher = AES.new(plaintext[:key_length], mode)
            # Entschlüsselung des verschlüsselten Texts mit demselben Verschlüsselungsmodus
            decrypted_text = cipher.decrypt(ciphertext)
            # Überprüfung, ob der entschlüsselte Text mit dem ursprünglichen Text übereinstimmt
            if decrypted_text == plaintext:
                return key_length, mode

# Beispieltexte
plaintext = b'Food Solution Hildesheim'
ciphertext = b'\u46b1\u996a\u8783\u31cb\ud1ed\u09a2\u6068\u41ea\u7162\u6111\ubac1\u4573\u5a73\ua658\u7af8\u651e'

# Ermittlung des Verschlüsselungsvektors und des Verschlüsselungscodes
key_length, mode = find_aes_parameters(plaintext, ciphertext)
print("Key Length:", key_length)
print("Mode:", mode)
