import socket


def start_server(ip, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    s.bind((ip, port))

    # Listen for incoming connections
    s.listen(1)
    print(f"Server started. Listening on {ip}:{port}")

    while True:
        # Accept a connection
        client_socket, addr = s.accept()
        print(f"Accepted connection from {addr}")

        # Receive data
        data = client_socket.recv(1024)
        print(f"Received data: {data.decode()}")

        # Close the connection
        client_socket.close()


# Start the server
start_server("127.0.0.1", 7000)
