"""
Sends commands to the Tello
"""

import socket
import threading

HOST = "192.168.10.1"
PORT = 8889

flying = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 9000))

def read_response():
    """
    Handles command responses from the Tello drone.
    """
    while flying:
        data, sender = sock.recvfrom(1024)
        data = data.decode(encoding="utf-8")
        print(f"Response: {data}")

response_thread = threading.Thread(target=read_response)
response_thread.start()

command = ""
sock.sendto("command".encode(encoding="utf-8"), (HOST, PORT))
while True:
    try:
        command = input("")
        sock.sendto(command.encode(encoding="utf-8"), (HOST, PORT))
        print(f"Sent: {command}")
        if command == "land":
            break
    except KeyboardInterrupt:
        sock.close()
        print("Landing...")
        command = "land"
flying = False
response_thread.join()
print("Thanks for flying TelloAir, Goodbye.")

