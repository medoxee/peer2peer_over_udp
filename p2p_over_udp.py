import socket
from threading import Thread
from os import system
import time

is_connected = False # is client connected to peer?
client_username = input("Enter your username: ").upper()

# broadcasting socket
broadcast_port = 10001
brd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
brd_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # what is that?
brd_sock.bind(('', broadcast_port))
broadcast_addr = ("255.255.255.255", broadcast_port) # 1st arg is the broadcast ip addr

# client socket configuration
client_sock_addr = ('', 10000)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket recveing data
client_sock.bind(client_sock_addr)

# broadcast discovery msg
def brd_discovery_msg(client_username, broadcast_addr):
    discovery_msg = client_username
    print("broadcasting discovery message...")
    while not is_connected:
        brd_sock.sendto(discovery_msg.encode(), broadcast_addr)
        time.sleep(3)

# capture discovety msg
def f_discovery_msg_capture(is_connected):
    while not is_connected:
        data, src_addr = brd_sock.recvfrom(1024) # limit 1024B, changeable
        decoded_data = data.decode()
        if decoded_data != client_username: # ignore localhost brd_packets
            print(f"Online profiles: {decoded_data}")
            cmd = input("Select one peer or refresh[R]: ").upper()
            if cmd == 'R':
                system("clear")
                continue
            is_connected = True
            system("clear")
            break
    return src_addr[0], cmd # return ip of peer and ignore port 10001

# listening function
def f_data_capture(peer_username):
    print(f"Listening on {client_sock_addr} ...\n")
    while True:
        # receiving text messages after connection
        data = client_sock.recv(1024) # limit 1024B, changeable
        decoded_data = data.decode()
        print(f"\r{peer_username}: {decoded_data}\nme: ", end="", flush=True)

t1 = Thread(target=brd_discovery_msg, args=(client_username,broadcast_addr,), daemon=True)
t1.start()
peer_ip, peer_username= f_discovery_msg_capture(is_connected)
t2 = Thread(target=f_data_capture, args=(peer_username,), daemon=True)
t2.start()

while True:
    # transmitting text messages after connection
    try:
        data_out = input("me: ").strip()
        client_sock.sendto(data_out.encode(), (peer_ip, 10000))
    except KeyboardInterrupt:
        print("\nClosing conversation...")
        client_sock.close()
        exit()
