#!/usr/bin/env python3
"""
Handles Tello commands and displays video stream and state.
"""

import socket
import socketserver
import multiprocessing
import cv2

HOST = "192.168.10.1"
PORT = 8889
VIDEO_PORT = 11111
STATE_HOST = "0.0.0.0"
STATE_PORT = 8890

class TelloStateHandler(socketserver.BaseRequestHandler):
    """
    Creates a local UDP server that receives state information from the 
    Tello.
    Based on: https://docs.python.org/3/library/socketserver.html#socketserver-udpserver-example
    """

    def handle(self):
        #TODO: This should be stored in a variable instead of output
        data = self.request[0]
        print(f"{self.client_address} wrote: {data}")

class ForkingUDPServer(socketserver.ForkingMixIn, socketserver.UDPServer):
    """
    Forking server for handling state asynchronously
    """

def read_response(sock):
    """
    Handles command responses from the Tello drone.
    """
    print("Started response handler")
    while True:
        data, sender = sock.recvfrom(1024)
        data = data.decode(encoding="utf-8")
        print(f"{sender}: {data}")

def video_stream():
    """
    Handles incoming video packets from the drone
    """
    print("Started video stream handler")
    source = f"udp://{HOST}:{VIDEO_PORT}"
    capture = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
    if not capture.isOpened():
        capture.open(source)

    while True:
        retval, frame = capture.read()
        if retval:
            cv2.imshow("frame", frame)
        cv2.waitKey(1)

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
    stream_process = 0
    state_process = 0
    sock.sendto("command".encode(encoding="utf-8"), (HOST, PORT))
    print("Tello control activated. Awaiting command...")
    while True:
        try:
            command = input("")
            if command == "land":
                break
            if command == "streamon":
                stream_process = multiprocessing.Process(target=video_stream)
                stream_process.start()
            if command == "streamoff":
                stream_process.terminate()
            if command == "stateon":
                server = ForkingUDPServer((STATE_HOST, STATE_PORT), TelloStateHandler)
                with server:
                    state_process = multiprocessing.Process(server.serve_forever())
                    state_process.start()
            if command == "stateoff":
                state_process.terminate()

            sock.sendto(command.encode(encoding="utf-8"), (HOST, PORT))
            print(f"Sent: {command}")

        except KeyboardInterrupt:
            sock.close()
            print("Landing...")
            command = "land"
    response_process.terminate()
    if stream_process:
        stream_process.terminate()
    if state_process:
        state_process.terminate()
    print("Autonomous landing sequence engaged...\nGoodbye.")

main()
