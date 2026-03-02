import Pyro4
@Pyro4.expose

class FileClient:
    def __init__(self, server_uri):
        self.server = Pyro4.Proxy("PYRONAME: server")

    def fetch_content(self):
        return self.server.get_content()