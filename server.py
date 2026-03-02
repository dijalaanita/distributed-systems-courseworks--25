import os
import Pyro4
@Pyro4.expose


class FileServer(object):
    def get_content(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
        return content
    
# creating daemon and register the server object
daemon = Pyro4.Daemon()
name_server = Pyro4.locateNS()

uri = daemon.register(FileServer)
name_server.register("sixseven.fileserver", uri)

print("File Server is ready.")
daemon.requestLoop()