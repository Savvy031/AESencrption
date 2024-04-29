from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from pathlib import Path
import App

class Encryption:

    def encrypt(self, path: str, pw: str):
        """Encrypt various files using AES.
        
        path(string):
            The input string with the file location.
            
        pw(string):
            The secret key to use in the symmetric cipher."""
        
        # Save the name of the file to encrypt
        file = Path(path).name
        
        # Create some random data for key derivation. Does not need to be kept secret, 
        # but it should be random and chosen for each derivation
        salt = get_random_bytes(16)

        # Create the key that we encrypt with
        # dkLen: The cumulative length of the keys to produce
        key = PBKDF2(pw, salt, dkLen=32)

        # Open the input and output files
        input_file = open(path, 'rb').read()# 'r' read, 'b' binary
        output_file = open(f'output/{file}.encrypted', 'wb') # 'w' write, 'b' binary

        # Create an AES object and give the key
        # We chose the EAX mode because it does not require padding like e.g. CBC
        cipher = AES.new(key, AES.MODE_EAX) 

        # We write the nonce, tag and salt to the ciphertext 
        # Encrypt and digest to get the ciphered data and tag
        ciphertext, tag = cipher.encrypt_and_digest(input_file) 
        # The nonce will be required for decryption. Fix size of 16 bytes. Does not need to be kept secret
        output_file.write(cipher.nonce) 
        # The tag will be required for decryption. Fix size of 16 bytes
        output_file.write(tag)
        # The salt will be required for decryption. Fix size of 16 bytes 
        output_file.write(salt) 
        # Write ciphhertext to file
        output_file.write(ciphertext)
        # Close the output file
        output_file.close()



    def decrypt(self, path: str, pw: str):
        """Decrypt various files using AES.
        
        path(string):
            The input string with the file location.
            
        pw(string):
            The secret key to use in the symmetric cipher."""
        
        try:
            # Save the name of the encrypted file
            file = Path(path).stem
            # Open encrypted file and read nonce, tag, salt and ciphertext
            file_in = open(path, "rb") # 'r' read, 'b' binary
            nonce = file_in.read(16) # 16 bytes long
            tag = file_in.read(16) # 16 bytes long
            salt = file_in.read(16) # 16 bytes long
            ciphertext = file_in.read() # Read the rest of the data out as ciphertext
            file_in.close()

            # Create key using user's input and salt we save to derive the same key
            key = PBKDF2(pw, salt, dkLen=32)

            # Open the output file
            output_file = open(f'output/{file}', 'wb') # 'w' write, 'b' binary

            # Create an AES object and give the key
            cipher = AES.new(key, AES.MODE_EAX, nonce)
            # Decrypt ciphertext and verify with the tag
            data = cipher.decrypt_and_verify(ciphertext, tag) 
            # Write the decrypted data to file
            output_file.write(data)
            # Close the output file
            output_file.close()

            App.App.labelChange(self, "Decryption with AES successful")

        except (ValueError):
            App.App.labelChange(self, "Incorrect password")