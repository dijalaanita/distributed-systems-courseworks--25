import os
import Pyro4
@Pyro4.expose


class FileServer1(object):
    def get_content1(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content1 = file.read()
        return content1
    
# creating daemon and register the server object
daemon = Pyro4.Daemon()
name_server = Pyro4.locateNS()

uri = daemon.register(FileServer1)
name_server.register("sixtyseven.fileserver1", uri)

print("File Server 1 is ready.")
daemon.requestLoop()