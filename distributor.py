#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 12:58:52 2023

@author: karl-henrikhorve
"""

import docker
import socket
import threading
import time

LISTEN_PORT = 2222
DOCKER_IMAGE = "ctf_test4"

socket_lock = threading.Lock()
client = docker.from_env()

def handle_connection(client_socket):
    # Launch a new Docker container
    container = client.containers.run(
        DOCKER_IMAGE, detach=True, tty=True, ports={"22/tcp": None}
    )

    # Wait for the container to start
    time.sleep(5)

    # Get the container's IP address
    container.reload()
    container_ip = container.attrs["NetworkSettings"]["IPAddress"]

    # Forward the connection to the container
    try:
        with socket.create_connection((container_ip, 22)) as container_socket:
            forward_threads = [
                threading.Thread(target=forward, args=(client_socket, container_socket)),
                threading.Thread(target=forward, args=(container_socket, client_socket)),
            ]

            for t in forward_threads:
                t.start()

            for t in forward_threads:
                t.join()
    finally:
        # Stop and remove the container
        container.stop()
        container.remove()

        # Close the client socket
        close_socket(client_socket)


def close_socket(sock):
    with socket_lock:
        if not sock._closed:
            sock.close()


def forward(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if len(data) == 0:
                break
            dst.sendall(data)
    finally:
        close_socket(src)
        close_socket(dst)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", LISTEN_PORT))
        server_socket.listen(5)

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            threading.Thread(target=handle_connection, args=(client_socket,)).start()


if __name__ == "__main__":
    main()
