import Pyro4

file_server = Pyro4.Proxy("PYRONAME: sixseven.fileserver")
test_file = "test_file.txt"
print(f"Fetching content of {test_file} from the server...")

try:
    content = file_server.get_content(test_file)
    print(f"Content of {test_file}:\n{content}")

except Exception as e:
    print(f"An error occurred: {e}")