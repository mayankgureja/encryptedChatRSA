encryptedChatRSA
===================

A Chat Server/Client with built-in RSA encryption written in Python

How To Run
----------

python encryptedChat.py <hostname/IP> <port>
eg. python encryptedChat.py localhost 1337

Compatibility
-------------

Tested to work on Python 2.7 on Windows 8

Description
------------

This is a Chat Server/Client with built-in RSA encryption written in Python. This program uses p2p (peer-to-peer) and not full duplex connections.

This program is meant to serve the purposes of someone who might be in Anonymous/WikiLeaks or other parties who require secure communications. The program is able to securely transfer text chat messages as well as most types of text files (PDFs etc. cannot be shared because of their encoding).

encryptedChat.py contains the classes and methods that set up the chat server and client. There is no need to specify whether you are the server or not. If no server is running on the specified address, you will become the server and wait for the other party to connect. The server begins by creating a socket and listening for incoming connections. The client receives a port and connects to the server on using that port. As soon as the connection is established, the server and client exchange Public Keys. Then, the client sends a pre-determined test message to the server in order to make sure that the encryption algorith is functioning normally. This needed to be done because of a bug that is yet to be fully fixed.

Both the client and server spawn two threads each. One responsible for reading messages from stdin and sending to the conversation partner, and the other to accept messages from the partner and printing to stdout. In addition, when 'FILE' is typed, the user is allowed to type in the name of a file in the current directory and send it, encrypted, to the other side. The receiver spawns a new thread that allows the file to be decoded and saved in the current directory.

encryptedChat.py imports rsa.py and encrypts all outgoing traffic and decrypts all incoming traffic. When a message 'quit()' is received, the connection is closed. At this point, the server also shuts down.

rsa.py contains all the methods necessary to implement RSA encryption and cryptography to the program as described above. The library contains helper methods, methods for encryption, decryption and key cracking and some tester methods (these have been commented out). It should be noted that keeping performance in mind, and the need for a chat program to seem like real-time communication, the range of prime numbers used for encryption had to kept at a maximum of 100. Anything more than that takes some time to decrypt and that made the program noticeably slower. That behavior was found to be unacceptable and it was decided to reduce the size of the cryptographic keys. However, increasing this is a simple matter of increasing variable 'n' in the gen_prime() method. In the real world, AES encryption is used for these types of situations, as it is much faster than RSA.

Usage
-----

1. Type your messages and hit Enter to send
2. Type 'file()' and hit Enter to send a file in the current directory
3. Type 'quit()' and hit Enter to leave the conversation	

Screenshots
-----------

Screenshots of the application in action are available in the /screenshots folder.

Dependencies/Requirements
-------------------------

Everything is part of the standard Python libraries.