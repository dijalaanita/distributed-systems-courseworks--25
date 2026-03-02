from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub_key = priv_key.public_key()

with open("client_private_key.pem", "wb") as f:
    f.write(priv_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("client_public_key.pem", "wb") as f:
    f.write(pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("key generated and saved to private_key.pem and public_key.pem")