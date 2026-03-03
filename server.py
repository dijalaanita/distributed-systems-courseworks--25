import os
import Pyro4
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
@Pyro4.expose


class FileServer(object):
    def __init__(self):
        try:
            with open("client_public_key.pem", "rb") as f:
                self.client_public_key = serialization.load_pem_public_key(f.read())
                print("Public key loaded successfully.")
        except FileNotFoundError:
            print("Public key file not found. Please ensure client_public_key.pem is in the same directory.")
        except Exception as e:
            print(f"An error occurred while loading the public key: {e}")

            
    def get_content(self, content, signature):
        # clean_content = content.strip()
        # print(f"Received request for content: '{clean_content}' with signature: {signature.hex()}")
        try:
            sig = bytes.fromhex(signature)
            self.client_public_key.verify(
                sig,
                content.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())
            print("Signature is valid. Content is being sent.")
        except Exception:
            raise ValueError("Invalid signature")
        
        if os.path.exists(content):
            with open(content, 'r') as file:
                return file.read()
        return "File not found."
    
# creating daemon and register the server object
daemon = Pyro4.Daemon()
name_server = Pyro4.locateNS()

uri = daemon.register(FileServer)
name_server.register("sixseven.fileserver", uri)

print("File Server is ready.")
daemon.requestLoop()