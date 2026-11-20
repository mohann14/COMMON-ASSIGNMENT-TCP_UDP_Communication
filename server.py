
import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 9100

def log_message(message):
    with open("server_log.txt", "a") as file:
        file.write(message + "\n")

def handle_tcp(client, address):
    print("TCP Client connected:", address)

    try:
        with client:
            file = client.makefile("r")
            for line in file:
                data = line.strip()

                if not data:
                    continue

                print("TCP Received:", data)
                log_message("TCP: " + data)

                parts = data.split("|", 2)
                if len(parts) == 3:
                    response = f"ACK|{parts[0]}|{parts[1]}\n"
                    client.sendall(response.encode())

    except OSError as error:
        print("TCP Error:", error)

    print("TCP Client disconnected:", address)

def start_udp():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((HOST, PORT))

    print("UDP Server listening on port", PORT)

    while True:
        data, address = udp.recvfrom(4096)
        message = data.decode(errors="replace")

        print("UDP Received:", message)
        log_message("UDP: " + message)

        parts = message.split("|", 2)
        if len(parts) == 3:
            response = f"ACK|{parts[0]}|{parts[1]}"
            udp.sendto(response.encode(), address)

def start_tcp():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind((HOST, PORT))
    tcp.listen()

    print("TCP Server listening on port", PORT)

    while True:
        client, address = tcp.accept()
        thread = threading.Thread(
            target=handle_tcp,
            args=(client, address),
            daemon=True
        )
        thread.start()

if __name__ == "__main__":
    threading.Thread(target=start_tcp, daemon=True).start()
    start_udp()
