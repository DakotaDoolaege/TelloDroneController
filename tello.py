"""
Sends commands to the Tello
"""

import socket
import multiprocessing

HOST = "192.168.10.1"
PORT = 8889

def read_response(sock):
    """
    Handles command responses from the Tello drone.
    """
    while True:
        data, sender = sock.recvfrom(1024)
        data = data.decode(encoding="utf-8")
        print(f"Response: {data}")

def main():
    """
    Main entry point for Tello Drone Autopilot
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 9000))

    response_process = multiprocessing.Process(target=read_response,
                                               args=(sock,))
    response_process.start()

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
    response_process.terminate()
    print("Thanks for flying TelloAir, Goodbye.")


main()

