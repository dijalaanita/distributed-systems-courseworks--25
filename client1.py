import Pyro4

file_server1 = Pyro4.Proxy("PYRONAME:sixtyseven.fileserver1")
test_file1 = "test_file.txt"
print(f"Fetching content of {test_file1} from the server...")

try:
    content1 = file_server1.get_content1(test_file1)
    print(f"Content of {test_file1}:\n{content1}")

except Exception as e:
    print(f"An error occurred: {e}")