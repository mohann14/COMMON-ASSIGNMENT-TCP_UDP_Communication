
import socket
import time

SERVER = input("Enter Server IP Address: ")
PORT = 9100

client_id = input("Enter Client ID: ")

print("\n1. TCP Communication")
print("2. UDP Communication")

choice = input("Select Protocol: ")

if choice == "1":
    protocol = "TCP"
elif choice == "2":
    protocol = "UDP"
else:
    print("Invalid selection")
    raise SystemExit

if protocol == "TCP":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, PORT))
else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

print("\nConnected using", protocol)

sequence = 1

while True:
    message = input("\nEnter Message (exit to quit): ")

    if message.lower() == "exit":
        break

    data = f"{client_id}|{sequence}|{message}"

    start = time.perf_counter()

    try:
        if protocol == "TCP":
            sock.sendall((data + "\n").encode())
            response = sock.makefile("r").readline().strip()
        else:
            sock.sendto(data.encode(), (SERVER, PORT))
            response, address = sock.recvfrom(4096)
            response = response.decode()

        end = time.perf_counter()

        print("Server Response:", response)
        print("Acknowledgment: Received")
        print("Transmission Time:",
              round((end - start) * 1000, 3), "ms")

    except socket.timeout:
        print("Acknowledgment: Not received (Timeout)")

    except OSError as error:
        print("Communication Error:", error)
        break

    sequence += 1

sock.close()
print("\nClient communication ended.")
