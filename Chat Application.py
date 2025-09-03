import socket
import threading

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    # Remove client if sending fails
                    clients.remove(client)

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print(f"Client {addr} disconnected")
                break
            print(f"Received from {addr}: {message.decode('utf-8')}")
            broadcast(message, client_socket)
        except ConnectionResetError:
            print(f"Connection reset by {addr}")
            break
        except Exception as e:
            print(f"Error with {addr}: {e}")
            break
    with clients_lock:
        clients.remove(client_socket)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen()
    print("Server listening on port 5555")

    while True:
        client_socket, addr = server.accept()
        with clients_lock:
            clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    main()
