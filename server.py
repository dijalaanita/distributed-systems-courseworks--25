import os
import Pyro4
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
@Pyro4.expose


class FileServer(object):
    def __init__(self):
        with open("client_public_key.pem", "rb") as f:
            self.client_public_key = serialization.load_pem_public_key(f.read())
            
    def get_content(self, filename, signature):
        try:
            self.client_public_key.verify(
                signature,
                content.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("Signature is valid. Content is being sent.")
        except Exception:
            raise ValueError("Invalid signature")
        
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
                return content
        return "File not found."
    
# creating daemon and register the server object
daemon = Pyro4.Daemon()
name_server = Pyro4.locateNS()

uri = daemon.register(FileServer)
name_server.register("sixseven.fileserver", uri)

print("File Server is ready.")
daemon.requestLoop()