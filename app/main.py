import socket


def main():
    print("logs")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept() # wait for client


if __name__ == "__main__":
    main()
