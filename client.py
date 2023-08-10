import socket
import threading
import os
import base64

# Ubah ukuran buffer menjadi 20 MB (20 * 1024 * 1024 byte)
BUFFER_SIZE = 20 * 1024 * 1024

def receive_message(client_socket):
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
                    save_document(file_name, received_data)
                else:
                    print(f"File {file_name} corrupted during transmission.")

            elif data_str.startswith("image:"):
                data_str = data_str[len("image:"):]
                destination, image_name, image_data = data_str.split(":")
                save_image(image_name, image_data)

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
                    save_music(music_name, received_data)
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
                    save_video(video_name, received_data)
                else:
                    print(f"File {video_name} corrupted during transmission.")

            else:
                print(f"Pesan diterima: {data_str}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def send_message(client_socket):
    try:
        while True:
            print("1. Kirim pesan ke client tertentu")
            print("2. Kirim pesan ke beberapa client")
            print("3. Kirim pesan broadcast ke semua client")
            print("4. Kirim dokumen (docx/pdf) ke client tertentu")
            print("5. Kirim dokumen (docx/pdf) ke beberapa client")
            print("6. Kirim dokumen (docx/pdf) broadcast ke semua client")
            print("7. Kirim gambar (jpg/png) ke client tertentu")
            print("8. Kirim gambar (jpg/png) ke beberapa client")
            print("9. Kirim gambar (jpg/png) broadcast ke semua client")
            print("10. Kirim musik (mp3) ke client tertentu")
            print("11. Kirim musik (mp3) ke beberapa client")
            print("12. Kirim musik (mp3) broadcast ke semua client")
            print("13. Kirim video (mp4) ke client tertentu")
            print("14. Kirim video (mp4) ke beberapa client")
            print("15. Kirim video (mp4) broadcast ke semua client")
            choice = input("Pilih opsi: ")

            if choice in ["1", "2"]:
                destination = input("Masukkan alamat tujuan (nama client): ")
                message = input("Masukkan Kalimat/paragraf: ")
                data = f"{destination}:{message}"
                client_socket.sendall(data.encode())

            elif choice == "3":
                message = input("Masukkan Kalimat/paragraf: ")
                data = f"broadcast:{message}"
                client_socket.sendall(data.encode())

            elif choice in ["4", "5", "6"]:
                file_path = input("Masukkan path dokumen (docx/pdf) yang akan dikirim: ")
                with open(file_path, "rb") as file:
                    file_data = file.read()
                file_name = os.path.basename(file_path)

                if choice == "4":
                    destination = input("Masukkan alamat tujuan (nama client): ")
                    data = f"file:{destination}:{file_name}:{len(file_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(file_data)
                elif choice == "5":
                    destinations = input("Masukkan daftar alamat tujuan (pisahkan dengan koma): ")
                    data = f"file:{destinations}:{file_name}:{len(file_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(file_data)
                elif choice == "6":
                    data = f"file:broadcast:{file_name}:{len(file_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(file_data)

            elif choice in ["7", "8", "9"]:
                image_path = input("Masukkan path gambar (jpg/png) yang akan dikirim: ")
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                image_name = os.path.basename(image_path)
                image_data_encoded = base64.b64encode(image_data).decode()

                if choice == "7":
                    destination = input("Masukkan alamat tujuan (nama client): ")
                    data = f"image:{destination}:{image_name}:{image_data_encoded}"
                    client_socket.sendall(data.encode())
                elif choice == "8":
                    destinations = input("Masukkan daftar alamat tujuan (pisahkan dengan koma): ")
                    data = f"image:{destinations}:{image_name}:{image_data_encoded}"
                    client_socket.sendall(data.encode())
                elif choice == "9":
                    data = f"image:broadcast:{image_name}:{image_data_encoded}"
                    client_socket.sendall(data.encode())

            elif choice in ["10", "11", "12"]:
                music_path = input("Masukkan path musik (mp3) yang akan dikirim: ")
                with open(music_path, "rb") as music_file:
                    music_data = music_file.read()
                music_name = os.path.basename(music_path)

                if choice == "10":
                    destination = input("Masukkan alamat tujuan (nama client): ")
                    data = f"music:{destination}:{music_name}:{len(music_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(music_data)
                elif choice == "11":
                    destinations = input("Masukkan daftar alamat tujuan (pisahkan dengan koma): ")
                    data = f"music:{destinations}:{music_name}:{len(music_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(music_data)
                elif choice == "12":
                    data = f"music:broadcast:{music_name}:{len(music_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(music_data)

            elif choice in ["13", "14", "15"]:
                video_path = input("Masukkan path video (mp4) yang akan dikirim: ")
                with open(video_path, "rb") as video_file:
                    video_data = video_file.read()
                video_name = os.path.basename(video_path)

                if choice == "13":
                    destination = input("Masukkan alamat tujuan (nama client): ")
                    data = f"video:{destination}:{video_name}:{len(video_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(video_data)
                elif choice == "14":
                    destinations = input("Masukkan daftar alamat tujuan (pisahkan dengan koma): ")
                    data = f"video:{destinations}:{video_name}:{len(video_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(video_data)
                elif choice == "15":
                    data = f"video:broadcast:{video_name}:{len(video_data)}"
                    client_socket.sendall(data.encode())
                    client_socket.sendall(video_data)

            else:
                print("Opsi tidak valid. Silakan pilih lagi.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def save_document(file_name, data):
    folder_name = "terima"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "wb") as file:
        file.write(data)

    print(f"Dokumen {file_name} berhasil disimpan di sistem Anda.")

def save_image(image_name, data):
    folder_name = "terima_gambar"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    image_path = os.path.join(folder_name, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(base64.b64decode(data.encode()))

    print(f"Gambar {image_name} berhasil disimpan di sistem Anda.")

def save_music(music_name, data):
    folder_name = "terima_music"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    music_path = os.path.join(folder_name, music_name)
    with open(music_path, "wb") as music_file:
        music_file.write(data)

    print(f"Musik {music_name} berhasil disimpan di sistem Anda.")

def save_video(video_name, data):
    folder_name = "terima_video"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    video_path = os.path.join(folder_name, video_name)
    with open(video_path, "wb") as video_file:
        video_file.write(data)

    print(f"Video {video_name} berhasil disimpan di sistem Anda.")

if __name__ == "__main__":
    client_host = "10.217.16.128"
    client_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((client_host, client_port))

    client_name = input("Masukkan nama Anda: ")
    client_socket.sendall(client_name.encode())

    threading.Thread(target=receive_message, args=(client_socket,)).start()
    threading.Thread(target=send_message, args=(client_socket,)).start()
