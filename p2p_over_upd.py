import socket, threading

# user/peer config
user_port = input("Enter your port to bind on: ")
while int(user_port) > 65535:
    user_port = input("error! port must be 0-65535. Retry: ")

peer_ip, peer_port = input("Enter peer's ip: "), input("Peer's port: ")
while int(peer_port) > 65535:
    peer_port = input("error! port must be 0-65535. Retry: ")

# user/peer sockets
user_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
user_sock.bind(('', int(user_port)))
peer_sock_addr = (peer_ip, int(peer_port))

# fonction listening
def listening():
    print(f"Listening on port {user_port}")
    while True:
        in_data = user_sock.recv(1024) # limit 1024B, changeable
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
