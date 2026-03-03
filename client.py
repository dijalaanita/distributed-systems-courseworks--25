import Pyro4
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
try:
    with open("client_private_key.pem", "rb") as f:
        priv_key = serialization.load_pem_private_key(f.read(), password=None)
except FileNotFoundError:
    print("Private key file not found. Please ensure client_private_key.pem is in the same directory.")
    exit()

file_server = Pyro4.Proxy("PYRONAME:sixseven.fileserver")
test_file = "test_file.txt".strip()

sig_bytes = priv_key.sign(
    test_file.encode(),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256())

sig = sig_bytes.hex()

print(f"Signature generated for {test_file}")
print(f"Fetching content of {test_file} from the server...")

try:
    content = file_server.get_content(test_file, sig)
    print(f"Content of {test_file}:\n{content}")

except Exception as e:
    print(f"An error occurred: {e}")