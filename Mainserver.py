import socket
import threading

HOST = '127.0.0.1'
TCP_PORT = 56890
UDP_PORT = 56891
ports = []
Status = []

def handle_client(client_socket, clients, nicknames):
    """
    Function to handle each client connection
    """
    global pm 
    pm =''
    try:
        # Send welcome message to the client
        welcome_txt = "Welcome to the chat server. Please sign up with a unique username."
        client_socket.sendall(welcome_txt.encode('utf-8'))

        # Receive the client's chosen username
        nickname = client_socket.recv(1024).decode('utf-8')
        
        # Check if the username is already taken
        while True:
            if nickname in nicknames:
                client_socket.sendall("That username is already taken. Please choose a different one.".encode("utf-8"))
                nickname = client_socket.recv(1024).decode('utf-8')
            else:
                client_socket.sendall("Proceed".encode("utf-8"))
                break

        # Confirm connection and store client information
        print(f"{nickname} has connected to the server.")
        clients[nickname] = client_socket
        nicknames.append(nickname)
        
        # Receive client's UDP port and status
        client_socket.sendall('now'.encode('utf-8'))
        client_port = client_socket.recv(1024).decode('utf-8')
        ports.append(client_port)
        a_s = client_socket.recv(1024).decode('utf-8')
        Status.append(a_s)
        print(f"{nickname}'s status is {a_s}.")

        # Handle 'away' status
        if a_s.lower() == "away":
            while True:
                try:
                    incoming = client_socket.recv(1024).decode('utf-8')
                    if incoming == "chs#avail":
                        ind = nicknames.index(nickname)
                        Status[ind] = "available"
                        break
                except Exception as e:
                    print(f"An error occurred: {e}")

        while True:
            # Receive commands from the client
            command = client_socket.recv(1024).decode('utf-8')

            if command == 'req':
                # Send lists of available and connected users to the client
                available_list = [nicknames[i] for i in range(len(nicknames)) if Status[i] == "available"]
                connected_list = [nicknames[i] for i in range(len(nicknames)) if Status[i] == "connected"]
                if len(available_list) != 0:
                    client_socket.sendall(str(available_list).encode('utf-8'))
                else:
                    client_socket.sendall("There is no user that is available.".encode('utf-8'))

                war = client_socket.recv(1024).decode('utf-8')
                if war == "send" and len(connected_list) != 0:
                    client_socket.sendall(str(connected_list).encode('utf-8'))
                elif war == "send" and len(connected_list) == 0:
                    client_socket.sendall("There is no connected user.".encode('utf-8'))

                if len(available_list)==1:
                    pm = client_socket.recv(1024).decode('utf-8')
                    if pm == "yes":
                        idx = nicknames.index(nickname)
                        Status[idx]="connected"

            elif command == 'dm':
                # Handle direct messaging requests
                recipient = client_socket.recv(1024).decode('utf-8')
                if recipient in clients:
                    pos = nicknames.index(recipient)
                    rec = clients[recipient]
                    if Status[pos] == 'available':
                        # Request chat permission from recipient
                        rec.sendall(f"/{nickname} is requesting to chat with you./".encode('utf-8'))
                        print("Request sent, waiting for approval.")
                        # Wait for the client to update permission
                        while True:
                            if pm == "yes":
                                print("Permission granted!")
                                client_socket.sendall("/Permission granted!/".encode('utf-8'))
                                goOn = client_socket.recv(1024).decode('utf-8')
                                sender_port = ports[pos]
                                if goOn =="go-on":
                                    client_socket.sendall(str(sender_port).encode('utf-8'))
                                    print("Address sent to start UDP chatting!")
                                    Status[pos] = "connected"
                                    break
                            elif pm == "no":
                                print("Permission not granted.")
                                pm = ""
                                client_socket.sendall("#Permission not granted.".encode('utf-8'))
                                continue  # Go back and wait for the next command

                    elif Status[pos] == "away":
                        client_socket.sendall("User is away.".encode('utf-8'))
                        break
                    elif Status[pos] == 'connected':
                        client_socket.sendall("/User is connected with another user, so responses might take time./".encode('utf-8'))
                        rec.sendall(f"/{nickname} is requesting to chat with you./".encode('utf-8'))
                        pm = rec.recv(1024).decode('utf-8')
                        if pm == "yes":
                            sender_port = ports[pos]
                            client_socket.sendall(str(sender_port).encode('utf-8'))

                else:
                    print(f"Recipient '{recipient}' not found.")

            elif command == '!q':
                # Handle client disconnection
                nicknames.remove(nickname)
                del clients[nickname]
                print(f"{nickname} left.")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


def main():
    # Setup TCP server
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_tcp.bind((HOST, TCP_PORT))
    server_tcp.listen()

    print("Server is listening for TCP connections...")

    clients = {}
    nicknames = []
    global pm 
    while True:
        try:
            # Accept incoming client connections
            client_socket, address = server_tcp.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, clients, nicknames))
            client_thread.start()
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    server_tcp.close()


if __name__ == "__main__":
    main()
