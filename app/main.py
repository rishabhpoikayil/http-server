import socket
import threading
import os
import sys

def handle_client(client_socket):
    # Reading the request sent by the client
    req = client_socket.recv(1024).decode()
    print(f"Request received:\n{req}")

    # Parsing HTTP request to get the request line
    http_request = req.split("\r\n")
    request_line = http_request[0]
    method, path, http_version = request_line.split()

    # Checking the request path and sending the appropriate response
    if method == "GET":
        if path == "/":
            response = f"HTTP/1.1 200 OK\r\n\r\n".encode()

        elif path.startswith("/echo/"):
            # Extracting response string to be sent back
            echo_string = path[len("/echo/"):]

            # Support for content-encoding header
            for line in http_request[1:]:
                if line.lower().startswith("accept-encoding:"):
                    encoding_type = line.split(":", 1)[1].strip()

            if echo_string.isalnum():
                if len(encoding_type) != 0 and encoding_type == "gzip":
                    response = f"HTTP/1.1 200 OK\r\nContent-Encoding: {encoding_type}\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_string)}\r\n\r\n{echo_string}".encode()
                else:
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_string)}\r\n\r\n{echo_string}".encode()

            # if echo_string.isalnum():
            #     response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_string)}\r\n\r\n{echo_string}".encode()

        elif path.startswith("/user-agent"):
            # Reading user agent header
            for line in http_request[1:]:
                if line.lower().startswith("user-agent:"):
                    user_agent_res = line.split(":", 1)[1].strip()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent_res)}\r\n\r\n{user_agent_res}".encode()

        elif path.startswith("/files/"):
            filename = path[len("/files/"):]
            file_path = os.path.join(FILES_DIRECTORY, filename)

            # Check if file exists -> if true, read its contents
            if os.path.isfile(file_path):
                with open(file_path, "r") as f:
                    content = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()
            else:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

        else:
            response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

    if method == "POST":
        if path.startswith("/files/"):
            filename = path[len("/files/"):]
            file_path = os.path.join(FILES_DIRECTORY, filename)

            # Get POST data and write into a new file
            post_data_index = req.find("\r\n\r\n") + 4
            post_data = req[post_data_index:]
            with open(file_path, "w") as f:
                f.write(post_data)

            response = f"HTTP/1.1 201 Created\r\n\r\n".encode()

    client_socket.sendall(response)
    client_socket.close()


def main():
    global FILES_DIRECTORY

    # Parsing command line arguments for dealing with files
    if len(sys.argv) > 2:
        if sys.argv[1] == "--directory":
            FILES_DIRECTORY = sys.argv[2]
    
    addr = ("localhost", 4221)
    server_socket = socket.create_server(addr, reuse_port=True)
    print("Server is listening on localhost:4221")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Starting new threads to handle multiple clients if needed
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
