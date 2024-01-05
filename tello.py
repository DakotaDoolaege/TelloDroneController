#!/usr/bin/env python3
"""
Sends commands to the Tello
"""

import socket
import multiprocessing
import cv2

HOST = "192.168.10.1"
PORT = 8889
VIDEO_PORT = 11111

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
    sock.sendto("command".encode(encoding="utf-8"), (HOST, PORT))
    print("Tello control activated. Awaiting your command")
    while True:
        try:
            command = input("")
            sock.sendto(command.encode(encoding="utf-8"), (HOST, PORT))
            print(f"Sent: {command}")
            if command == "land":
                break
            if command == "streamon":
                stream_process = multiprocessing.Process(target=video_stream)
                stream_process.start()
            if command == "streamoff":
                stream_process.terminate()

        except KeyboardInterrupt:
            sock.close()
            print("Landing...")
            command = "land"
    response_process.terminate()
    stream_process.terminate()
    print("Autonomous landing sequence engaged, Goodbye.")


main()
