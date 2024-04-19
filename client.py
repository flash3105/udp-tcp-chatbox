import socket
import threading
import random
import time

HOST = '127.0.0.1'
TCP_PORT = 56890
UDP_PORT = 56891

# Function to receive UDP messages
def receive_udp(client_udp):
    while True:
        try:
            message, addr = client_udp.recvfrom(1024)
            print(message.decode('utf-8'))
            print("other user was typing...", end="", flush=True)
            time.sleep(1)  # Simulating typing indicator delay
            print("\r" + " " * 30 + "\r", end="", flush=True)  # Clear typing indicator
        except OSError as e:
            print(f"Error receiving UDP message: {e}")
            break

# Main function
def main():
    global nickname
    global sport
    
    client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_tcp.connect((HOST, TCP_PORT))
    print("Connected to the server!")

    welcome_message = client_tcp.recv(1024)
    print(welcome_message.decode('utf-8')) 
    nickname = input("Please input your username: ")
    

    while True:
        client_tcp.sendall(nickname.encode('utf-8'))
        msg = client_tcp.recv(1024).decode('utf-8')
        if msg !="Proceed":
            print(msg)
            nickname = input("Please input a new username:")
        else:
            break

    
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sport = random.randint(8000, 9000)
    que = client_tcp.recv(1024).decode('utf-8')
    if que == 'now':
        client_udp.bind(('127.0.0.1', sport)) 
        client_tcp.sendall(str(sport).encode('utf-8'))
        
    udp_thread = threading.Thread(target=receive_udp, args=(client_udp,))
    udp_thread.start()
    
    a_s = input("Please input your availability status(available/away):")
    client_tcp.sendall(a_s.encode('utf-8'))

    if a_s == "away":
        print("Given that you are away, you will not receive texts/files from any user. Also, you can't chat with anyone.")
        print("Use the command 'chs#avail' to change your status.")
        while True:
            try:
                incoming = input()
                if incoming == 'chs#avail':
                    client_tcp.sendall(incoming.encode('utf-8'))
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
    
    print("Enter a command 'req' to see a list of available peers:")
    command = input()
    if command == "req":
        client_tcp.sendall(command.encode('utf-8'))
        txt1 = client_tcp.recv(1024).decode('utf-8')
        print("Available peers to chat with are:")
        print(txt1)
        client_tcp.sendall("send".encode('utf-8'))
        txt2 = client_tcp.recv(1024).decode("utf-8")
        print("Available but connected peers are:")
        print(txt2)

    if len(eval(txt1)) == 1:
        print("Since there is no one available, wait for people to log in.")
        pm = client_tcp.recv(1024).decode('utf-8')
                    
        if pm.startswith("/"):
            print(pm)
            des = input("Do you accept? yes or no? ")
            client_tcp.send(des.encode('utf-8'))
            if des.lower() == "yes":
                print("You are now chatting with your peer via UDP chat.") 
    else:
        print("Enter a command ('dm' to send a direct message, '!q' to quit)")

    while True:
        try:   
            command = input()
            client_tcp.sendall(command.encode('utf-8'))
                   
            if command == 'dm':
                recipient = input("Enter the recipient's nickname: ")
                client_tcp.sendall(recipient.encode('utf-8'))
                
                con = client_tcp.recv(1024).decode('utf-8')
                print(con)
                # Receive the port number of the recipient from the server
                if con.startswith("/Per"):
                    client_tcp.sendall("go-on".encode('utf-8'))
                    recipient_port = int(client_tcp.recv(1024).decode('utf-8'))
                    print("You are now chatting with your peer via UDP chat.")
                    permission = input("Please note you are now proceeding to a chatroom. Enter 'okay' to proceed: ")
                    if permission.lower() == "okay":
                        client_tcp.sendall("okay".encode('utf-8'))
                        print("Chat session initiated.")
                    
                # Start sending messages via UDP
                #elif con.startswith("#P"):
                     
                   
                   #  break
                while True:
                        message = input("")
                        if message == "Exit":
                            client_udp.sendto(f"{nickname} has left the chat, connect with other peers".encode('utf-8'), (HOST, recipient_port))
                            client_tcp.sendall(message.encode('utf-8'))
                            break
                        else:
                            print("Sending...", end="", flush=True)
                            client_udp.sendto(f"{nickname}: {message}".encode(), (HOST, recipient_port))
                            time.sleep(2)  # Simulating sending indicator delay
                            print("\r" + " " * 20 + "\r", end="", flush=True)  # Clear sending indicator
            
            elif command == '!q':
                client_tcp.sendall(command.encode('utf-8'))
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
        

if __name__ == "__main__":
    main()
