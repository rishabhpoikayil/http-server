import socket

def main():
    addr = ("localhost", 4221)
    server_socket = socket.create_server(addr, reuse_port=True)
    print("Server is listening on localhost:4221")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Reading the request sent by the client
        req = client_socket.recv(1024)
        print(f"Request received:\n{req}")

        # Parsing HTTP request to get the request line
        request_line = req.split(b"\r\n")[0]
        method, path, version = request_line.split()
        print(f"path"{path})

        # Checking the request path and sending the appropriate response
        if path == '/':
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    main()
