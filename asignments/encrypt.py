from cryptography.fernet import Fernet
# a simple encryption function
def encrypt(data):
    
    # reading the key
    file = open('key.key', 'rb')
    key = file.read() # The key will be type bytes
    file.close()

    # encoding data
    data = data.encode()

    # encrypting the data
    f = Fernet(key)
    encryptedData = f.encrypt(data)

    # returning the encrypted value 
    return encryptedData.decode()

def encryptfile(myfile):
    # getting file data
    with open(myfile.path,'r') as f:
        data = f.read()

    # returning the encrypted value
    return encrypt(data)


# function to decrypt the data
def decrypt(data):
    # reading the key
    file = open('key.key', 'rb')
    key = file.read() # The key will be type bytes
    file.close()

    # encoding data
    data = data.encode()

    # encrypting the data
    f = Fernet(key)
    decryptedData = f.decrypt(data)

    return decryptedData