import socket


def send_tcp_data(ip, port, data):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    s.connect((ip, port))

    # Send data
    s.sendall(data.encode())

    # Close the connection
    s.close()


# Use the function
send_tcp_data("127.0.0.1", 7000, "Hello, Server!")
