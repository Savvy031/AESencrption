from hashlib import sha256
from Crypto.Random import get_random_bytes
from pathlib import Path
import hashlib, App, os


class Encryption:
    
    def encrypt(self, path: str, pw: str):
        """Encrypt various files using own algorithm.
        
        path(string):
            The input string with the file location.
            
        pw(string):
            The secret key to use in the symmetric cipher."""
        
        # Save the name of the file to encrypt
        file = Path(path).name

        # Produce the salted password hash
        # Create some random data that is used to hash the data. Does not need to be kept secret, 
        # but it should be random and chosen for each derivation
        salt = get_random_bytes(16) 
        # Convert the entered password to bytes
        pwrd = bytes(pw, 'utf-8')
        # Add salt to pwrd to ensure that users with identical passwords obtain different hashes
        key = salt + pwrd
        # Create an instance of the sha256 class
        h = sha256() 
        # Update the hash object with salted key
        h.update(key) 
        # Get a hexadecimal representation of the hash value. The digest/hash has 32 bytes
        hash = h.hexdigest()
        
        # Save the the hash to a file. 
        file_out = open(f"output/{file}_hash.bin", "w") # no need to write it binary
        # Write hash to file
        file_out.write(hash)
        # Close the output file
        file_out.close()

        # Open the input and output files
        input_file = open(path, 'rb').read()
        output_file = open(f'output/{file}.encrypted', 'wb')

        # We write the salt to the ciphertext
        # Encrypt with XOR to get the ciphered data
        cipher = xorOperation(input_file, pwrd)
        # The salt will be required for decryption. Fix size of 16 bytes
        output_file.write(salt)
        # Write ciphhertext to file
        output_file.write(cipher)
        # Close the output file
        output_file.close()

        # delete original file
        os.remove(path) 
    


    def decrypt(self, path: str, pw: str):
        """Decrypt various files using own algorithm.
        
        path(string):
            The input string with the file location.
            
        pw(string):
            The secret key to use in the symmetric cipher."""

        # Save the name of the encrypted file       
        file = Path(path).stem

        # Open the input file and read in hash
        file_in = open(f"output/{file}_hash.bin", "r") # no need to read it binary
        hash_from_file = file_in.read()
        file_in.close()

        # Open encrypted file and read in salt and ciphertext
        file_in = open(path, "rb")
        salt = file_in.read(16)
        ciphertext = file_in.read() 
        file_in.close()

        # Convert the entered password to bytes
        pwrd = bytes(pw, 'utf-8')
        # Add identical salt as for encryption to the password the user entered
        key = salt + pwrd
        # Create identical hash as for encryption due to identical key
        hash = hashlib.sha256(key).hexdigest()
        
        if (not hash == hash_from_file):
            App.App.labelChange(self, 'Hashes are not identical')
        else:
            # Open the output file
            output_file = open(f'output/{file}', 'wb')
            plain = xorOperation(ciphertext, pwrd)
            output_file.write(plain)
            output_file.close()
            App.App.labelChange(self, "Decryption with successful")


def xorOperation(file, key):
    '''Use XOR operation on file and key.
    
    For further details have a look at our documentation.
    
    file(bytes):
        The input file that has to be encrypted.
        
    key(bytes):
        The secret key to use in the XOR operation. '''
    
    list = []  
    for i in range(len(file)):
        list.append(file[i] ^ key[i % len(key)])
    return bytes(list)

