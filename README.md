# udp-tcp-chatbox
The Terminal Chat Application provides a simple yet effective way for users to communicate with each other via text messages within a terminal environment. Designed to be lightweight and easy to use, this application facilitates real-time conversations between users on the same network.
Features
Username Selection: Users can choose a username to identify themselves in the chat.
Availability Status: Users can set their availability status as "available" or "away".
Direct Messaging: Users can send direct messages to other users who are available.
UDP Chatting: Direct messages are sent using UDP sockets for faster and more efficient communication.
Dynamic Peer List: Users can see a list of available peers and choose whom to message.
Simulated Typing Indicator: The application simulates a typing indicator to show when the other user is typing.
Exit Command: Users can type "Exit" to leave the chat.
Requirements
Python 3.x
How to Use
Clone or download the repository to your local machine.
Open a terminal window and navigate to the directory containing the application files.
Run the server.py file to start the server: python server.py
In another terminal window, run the client.py file to connect to the server and start the chat application: python client.py
Follow the on-screen instructions to choose a username, set your availability status, and interact with other users.
Commands
req: Request a list of available peers.
dm: Send a direct message to a specific user.
!q: Quit the chat application.
Notes
Make sure the server is running before starting the client application.
You can customize the host and port settings in the server.py and client.py files if needed.

Tshemollo
