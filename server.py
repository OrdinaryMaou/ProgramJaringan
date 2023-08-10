import socket
import threading
import os
import base64

# Ubah ukuran buffer menjadi 20 MB (20 * 1024 * 1024 byte)
BUFFER_SIZE = 20 * 1024 * 1024

def save_image(client_name, image_name, data):
    folder_name = os.path.join("terima", client_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    image_path = os.path.join(folder_name, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(base64.b64decode(data.encode()))

def save_document(client_name, file_name, data):
    folder_name = os.path.join("terima", client_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "wb") as file:
        file.write(data)

def save_music(client_name, music_name, data):
    folder_name = os.path.join("terimaS", client_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    music_path = os.path.join(folder_name, music_name)
    with open(music_path, "wb") as music_file:
        music_file.write(data)

def save_video(client_name, video_name, data):
    folder_name = os.path.join("terima", client_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    video_path = os.path.join(folder_name, video_name)
    with open(video_path, "wb") as video_file:
        video_file.write(data)

def handle_client(client_socket, client_address, clients):
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            data_str = data.decode()
            if data_str.startswith("file:"):
                data_str = data_str[len("file:"):]
                destination, file_name, file_size = data_str.split(":")
                file_size = int(file_size)
                received_data = b""

                while len(received_data) < file_size:
                    data = client_socket.recv(min(BUFFER_SIZE, file_size - len(received_data)))
                    if not data:
                        break
                    received_data += data

                if len(received_data) == file_size:
                    save_document(destination, file_name, received_data)
                else:
                    print(f"File {file_name} corrupted during transmission.")

            elif data_str.startswith("image:"):
                data_str = data_str[len("image:"):]
                destination, image_name, image_data = data_str.split(":")
                save_image(destination, image_name, image_data)

            elif data_str.startswith("music:"):
                data_str = data_str[len("music:"):]
                destination, music_name, music_size = data_str.split(":")
                music_size = int(music_size)
                received_data = b""

                while len(received_data) < music_size:
                    data = client_socket.recv(min(BUFFER_SIZE, music_size - len(received_data)))
                    if not data:
                        break
                    received_data += data

                if len(received_data) == music_size:
                    save_music(destination, music_name, received_data)
                else:
                    print(f"File {music_name} corrupted during transmission.")

            elif data_str.startswith("video:"):
                data_str = data_str[len("video:"):]
                destination, video_name, video_size = data_str.split(":")
                video_size = int(video_size)
                received_data = b""

                while len(received_data) < video_size:
                    data = client_socket.recv(min(BUFFER_SIZE, video_size - len(received_data)))
                    if not data:
                        break
                    received_data += data

                if len(received_data) == video_size:
                    save_video(destination, video_name, received_data)
                else:
                    print(f"File {video_name} corrupted during transmission.")

            else:
                destination, message = data_str.split(":", 1)
                destinations = destination.split(",")
                if destination == "broadcast":
                    send_broadcast_message(message, clients, client_socket)
                else:
                    send_message_to_clients(destinations, message, clients, client_socket)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def send_image(destination, image_name, image_data, clients):
    data = f"image:{destination}:{image_name}:{image_data}"
    clients[destination].sendall(data.encode())

def send_broadcast_message(message, clients, sender_socket):
    for dest_socket in clients.values():
        if dest_socket != sender_socket:
            dest_socket.sendall(message.encode())

def send_message_to_clients(destinations, message, clients, sender_socket):
    for dest in destinations:
        if dest in clients:
            dest_socket = clients[dest]
            dest_socket.sendall(message.encode())
        else:
            response = f"Client dengan alamat '{dest}' tidak ditemukan."
            sender_socket.sendall(response.encode())

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print(f"Server berjalan di {host}:{port}")

    clients = {}

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Terhubung ke {client_address[0]}:{client_address[1]}")
            client_name = client_socket.recv(1024).decode()
            clients[client_name] = client_socket
            threading.Thread(target=handle_client, args=(client_socket, client_address, clients)).start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    server_host = "10.217.16.128"
    server_port = 12345

    start_server(server_host, server_port)
