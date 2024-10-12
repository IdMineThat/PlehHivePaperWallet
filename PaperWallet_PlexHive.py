import hashlib
import base58
import ecdsa

def password_to_private_key():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    return private_key

def private_key_to_public_key(private_key):
    public_key = private_key.verifying_key
    public_key_bytes = public_key.to_string('compressed')
    return public_key_bytes

def public_key_to_address(public_key):
    hashed_public_key = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).digest()
    hashed_public_key_with_version = theVersionByte + hashed_public_key
    checksum = hashlib.sha256(hashlib.sha256(hashed_public_key_with_version).digest()).digest()[:4]
    address_data = hashed_public_key_with_version + checksum
    coin_address = base58.b58encode(address_data).decode('utf-8')
    return coin_address

def private_key_to_wifc(private_key):
    private_key_bytes = private_key.to_string()
    compression_flag = b'\x01'
    wifc_data = theWifcVersionByte + private_key_bytes + compression_flag
    checksum = hashlib.sha256(hashlib.sha256(wifc_data).digest()).digest()[:4]
    wifc_key = base58.b58encode(wifc_data + checksum).decode('utf-8')
    return wifc_key

coinData=\
    [
        ["PlexHive","1C","32","PLHV",0]#in decimal:28,50
    ]

theVersionByte = bytes.fromhex(coinData[0][1])
theWifcVersionByte = bytes.fromhex(coinData[0][2])
coin_address = public_key_to_address(public_key)
wifc_key = private_key_to_wifc(private_key)
private_key = password_to_private_key()
public_key = private_key_to_public_key(private_key)

print(coinData[0][0], "Address:", coin_address)
print(coinData[0][0], "WIFC Key:", wifc_key)
print("Private Key (hex):", private_key.to_string().hex())

f = open("PlexHiveAddress.csv", "a")
f.write(coinData[o][0] + ',' + coin_address + ',' + wifc_key + ',' + private_key.to_string().hex() + '\n')
f.close()
