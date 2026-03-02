from Pyro4


class FileServer(filename):
    def __init__(self, filename):
        self.filename = filename

    def get_content(self):
        with open(self.filename, 'r') as file:
            content = file.read()
        return content