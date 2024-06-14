import socket

def main():
    addr = ("localhost", 4221)
    server_socket = socket.create_server(addr, reuse_port=True)
    print("Server is listening on localhost:4221")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Reading the request sent by the client
        req = client_socket.recv(1024).decode()
        print(f"Request received:\n{req}")

        # Parsing HTTP request to get the request line
        http_request = req.split("\r\n")
        print(f"http_request:\n{http_request}")
        request_line = http_request[0]
        method, path, http_version = request_line.split()

        # Checking the request path and sending the appropriate response
        if path == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"

        elif path.startswith("/echo/"):
            # Extracting response string to be sent back
            echo_string = path[len(b"/echo/"):]
            if echo_string.isalnum():
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_string)}\r\n\r\n{echo_string}".encode()

        elif path.startswith("/user-agent"):
            # Reading user agent header
            for line in http_request[1:]:
                if line.startswith("User-Agent:"):
                    user_agent_res = line.split(":", 1)[1].strip()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent_res)}\r\n\r\n{user_agent_res}".encode()

        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    main()
