import socket, threading

# user/peer config
user_port = int(input("Enter your port to bind on: "))
peer_ip, peer_port = input("Enter peer's ip: "), int(input("Peer's port: "))
peer_sock_addr = peer_ip, peer_port

# user socket
user_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
user_sock.bind(('', user_port))

# fonction listening
def listening():
    print(f"Listening on port {user_port}\n")
    while True:
        in_data = user_sock.recv(1024)
        print(f"Peer says: {in_data.decode()}")
# start a thread to listening function
threading.Thread(target=listening, daemon=True).start()

# sending data
while True:
    try:
        out_data = input("\n")
        user_sock.sendto(out_data.encode(), peer_sock_addr)
    except KeyboardInterrupt:
        print("\nClosing conversation...")
        user_sock.close()
        exit()
