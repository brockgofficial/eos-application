from Crypto.Cipher import AES
import secrets
import pickle
global fileSecret


# This function creates a 16 character string consisting of only numbers that will be used as the IV Value. #
# The IV value is an input used to provide an initial state which will result in a random encrypted output. #

def RandomIV():
	secretsGenerator = secrets.SystemRandom()
	random_iv = 0

	while True:
		random_iv = str(secretsGenerator.randint(0000000000000000,9999999999999999))
		NumberOfCharacters = (random_iv.count("") - 1)
		if (NumberOfCharacters == 16):
			return random_iv

# This function creates a 16 character string consiting of alphanumeric characters that will be used as the key value. #
# The key value is what is actually used to encrypt and decrypt the data.			

def RandomKey():
	KeyRandom = secrets.token_hex(8)
	return KeyRandom

# This function will take an input, generate a random key and IV value and then encrypt the information that was provided, returning the result. #

def do_encrypt(msg):
    global fileSecret
    global Key
    fileSecret = str(RandomIV())
    Key = str(RandomKey())

    try:
        KeyFile = open("PassIV","r")
    except IOError as err:
        print(err)
    KeyFileLines = KeyFile.read().splitlines()
    KeyForEncryptionOfKey = (KeyFileLines[0])
    IVForEncryptionOfIV = (KeyFileLines[1])
    KeyFile.close()

    KeyObj = AES.new(KeyForEncryptionOfKey, AES.MODE_CFB, IVForEncryptionOfIV)
    Keyphrase = Key + "," + fileSecret
    cipherkeys = KeyObj.encrypt(Keyphrase)

    msg = bytes(msg,'UTF-8')
    MessageObj = AES.new(Key, AES.MODE_CFB, fileSecret)
    ciphertext = MessageObj.encrypt(msg)
    return cipherkeys, ciphertext
    

# This function will take an input, use the encrypted data and decrypt it using the IV and the key. #

def do_decrypt_key(Message):
    KeyFiles = open("PassIV","r")
    KeyFileLines = KeyFiles.read().splitlines()
    KeyForDecryptionOfKey = (KeyFileLines[0])
    IVForDecryptionOfIV = (KeyFileLines[1])
    testKeyObj = AES.new(KeyForDecryptionOfKey, AES.MODE_CFB, IVForDecryptionOfIV)
    decryptedKey = testKeyObj.decrypt(Message)
    return decryptedKey


def do_decrypt(Message,Key,IV):
    testKeyObj = AES.new(Key, AES.MODE_CFB,IV)
    decryptedMessage = testKeyObj.decrypt(Message)
    return decryptedMessage

def decryption(message):
	keydecode = do_decrypt_key(message[0])
	keydecode = keydecode.decode()
	keydecode = keydecode.split(',')
	decryptedmessage = do_decrypt(message[1],keydecode[0],keydecode[1])
	print(decryptedmessage.decode())
	return decryptedmessage

def serialize(Message):
	Message = do_encrypt(Message)
	header_length = (f'{len(str(Message))}')
	encryptedtest = pickle.dumps([header_length,Message])
	return encryptedtest

	
