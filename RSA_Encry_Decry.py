def rsa_encryption(data, public_key):
    return pow(data, public_key[0], public_key[1])


def rsa_decryption(data, private_key):
    return pow(data, private_key[0], private_key[1])

