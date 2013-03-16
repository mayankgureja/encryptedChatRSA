"""
encryptedChat.py
Mayank Gureja
03/14/2013
"""


import sys
import socket
import threading
import rsa as RSA
import datetime
import os


def Server(host, port):
    """
    Creates the server instance, sets up the server
    """

    port = int(port)

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)

        print "* Waiting for partner to join conversation... *\n"
        conn, client_addr = server.accept()

        # print "Client connected: ", client_addr[0]
        print "* Client attempting to connect... *\n"
    except Exception:
        pass

    # Wait to receive client's public key
    recvIsComplete = False
    key = ""
    while not recvIsComplete:
        key += conn.recv(1024)
        if key.strip("~") and key[0] == "~" and key[-1] == "~":
            recvIsComplete = True

    key = key.strip("~").split(',')
    publicTuple = (key[0], key[1])
    print "* Client\'s Public Key received *"

    # Send public key to client
    e, d, c = RSA.keygen()
    sendPublic = str(d) + ',' + str(c)
    conn.send("~" + sendPublic + "~")
    print "* Public Key sent *"

    privateTuple = (e, c)

    # Receving test string to make sure encryption is working properly
    recvIsComplete = False
    data = ""
    while not recvIsComplete:
        data += conn.recv(1024)
        if data.strip("~") and data[0] == "~" and data[-1] == "~":
            recvIsComplete = True
    data = decrypt(data.strip("~"), publicTuple)
    if data != "~Client:abcdefghijklmnopqrstuvwxyz~":
        # print "data: ", data
        print "\n* Encryption could not be verified! Please try to reconnect... *\n"
        conn.send("~ABORT~")
        connClose(conn)
        return

    # Sending test string to make sure encryption is working properly
    data = "~Server:abcdefghijklmnopqrstuvwxyz~"
    data = encrypt(data.strip(), privateTuple)
    conn.send("~" + data + "~")

    # # Receving test string to make sure encryption is working properly
    # recvIsComplete = False
    # data = ""
    # while not recvIsComplete:
    #     data += conn.recv(1024)
    #     if data.strip("~") and data[0] == "~" and data[-1] == "~":
    #         recvIsComplete = True
    # if data != "~ABORT~":
    #     print "\n* Encryption Verified! *"
    # else:
    #     print "\n* Encryption could not be verified! Please try to reconnect... *\n"
    #     connClose(conn)
    #     return

    print "\n* Connected to chat *\n*"
    print "1. Type your messages below and hit Enter to send"
    print "2. Type \'file()\' and hit Enter to send a file in the current directory"
    print "3. Type \'quit()\' and hit Enter to leave the conversation\n"

    ReadThread = Thread_Manager('read', conn, publicTuple, None)
    WriteThread = Thread_Manager('write', conn, None, privateTuple)

    ReadThread.start()
    WriteThread.start()

    # Wait until client disconnects
    ReadThread.join()
    print "\n* Your partner has left the conversation. Press any key to quit... *\n "

    # Stop the write thread
    WriteThread.stopWrite()
    WriteThread.join()

    # Shut down client connection
    try:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
    except:
        # Connection already closed
        pass

    # Shut down server
    connClose(server)


def Client(host, port):
    """
    Creates the client instance, sets up the client
    """

    port = int(port)

    print "\n* Connecting to server... *\n"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Send public key to server
    e, d, c = RSA.keygen()
    sendPublic = str(d) + "," + str(c)
    client.send("~" + sendPublic + "~")
    print "* Public Key sent *"

    # Wait to receive server's public key
    recvIsComplete = False
    key = ""
    while not recvIsComplete:
        key += client.recv(1024)
        if key.strip("~") and key[0] == "~" and key[-1] == "~":
            recvIsComplete = True

    key = key.strip("~").split(',')
    publicTuple = (key[0], key[1])
    print "* Server\'s Public Key received *"

    privateTuple = (e, c)

    # Sending test string to make sure encryption is working properly
    data = "~Client:abcdefghijklmnopqrstuvwxyz~"
    data = encrypt(data.strip(), privateTuple)
    client.send("~" + data + "~")

    # Receving test string to make sure encryption is working properly
    recvIsComplete = False
    data = ""
    while not recvIsComplete:
        data += client.recv(1024)
        if data.strip("~") and data[0] == "~" and data[-1] == "~":
            recvIsComplete = True

    if data != "~ABORT~":
        data = decrypt(data.strip("~"), publicTuple)
    if data != "~Server:abcdefghijklmnopqrstuvwxyz~":
        # print "data: ", data
        print "\n* Encryption could not be verified! Please try to reconnect... *\n"
        client.send("~ABORT~")
        connClose(client)
        return
    else:
        print "\n* Encryption Verified! *"

    print "\n* Connected to chat *\n*"
    print "1. Type your messages below and hit Enter to send"
    print "2. Type \'file()\' and hit Enter to send a file in the current directory"
    print "3. Type \'quit()\' and hit Enter to leave the conversation\n"

    ReadThread = Thread_Manager('read', client, publicTuple, None)
    WriteThread = Thread_Manager('write', client, None, privateTuple)

    ReadThread.start()
    WriteThread.start()

    ReadThread.join()
    print "\n* Your partner has left the conversation. Press any key to quit... *\n"

    # Stop the write thread
    WriteThread.stopWrite()
    WriteThread.join()

    # Shut down client connection
    connClose(client)


def encrypt(data, private):
    """
    Encrypts incoming data with given private key
    """
    encrypted_data = ""
    for i in range(0, len(data)):
        encrypted_data += str(RSA.endecrypt(ord(data[i]), private[0], private[1])) + ","
    return encrypted_data


def decrypt(data, public):
    """
    Decrypts input integer list into sentences
    """

    words = data.split(",")
    decrypted_data = ""
    for i in range(0, len(words) - 1):
        decrypted_data += str(RSA.decode(RSA.endecrypt(words[i], public[0], public[1])))
    return decrypted_data


def connClose(conn):
    """
    Closes given connection
    """
    try:
        print "* Closing all sockets and exiting... *"
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
    except:
        # Connection already closed
        pass


class Thread_Manager(threading.Thread):
    """
    Creates threads for asynchronoues reading and writing
    """

    def __init__(self, action, conn, public, private):
        """
        Constructor for Thread_Manager class
        """

        threading.Thread.__init__(self)
        self.action = action.lower()
        self.conn = conn
        self.dowrite = True
        self.exitcode = 'quit()'

        if public is not None:
            self.setPublic(public)
        if private is not None:
            self.setPrivate(private)

    def run(self):
        """
        Invoked when new thread is executed
        """

        if self.action == 'read':
            self.read()
        elif self.action == "file":
            self.file()
        else:
            self.write()

    def setPublic(self, public):
        """
        Sets public key from other party for decryption
        """

        self.public = public

    def setPrivate(self, private):
        """
        Sets private key for encryption
        """

        self.private = private

    def stopWrite(self):
        """
        Terminates the write loop
        """

        self.dowrite = False

    def read(self):
        """
        Responsible for reading in data from the client and displaying stdout
        """

        global doRead
        recvIsComplete = False
        data = ""
        while not recvIsComplete and doRead:
            data += self.conn.recv(1024)
            if data.strip("~") and data[0] == "~" and data[-1] == "~":
                recvIsComplete = True

        data = decrypt(data.strip("~"), self.public)

        while doRead and data.strip() != self.exitcode and len(data) > 0:
            if data.strip().split(":")[0] == "#FILE":
                print "\n* Receiving file... *"
                self.saveFile(data.strip())
            else:
                print "<Message>", data.strip()

            recvIsComplete = False
            data = ""
            while not recvIsComplete and doRead:
                data += self.conn.recv(1024)
                if data.strip("~") and data[0] == "~" and data[-1] == "~":
                    recvIsComplete = True

            data = decrypt(data.strip("~"), self.public)

        self.stopWrite

    def saveFile(self, data):
        """
        Reads in file from the client and creates the file in the local directory
        """

        try:
            filename, extension = os.path.splitext(data.split(":")[1])
            filename = filename.replace(extension, "")
            newname = filename + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + extension
            newFile = open(newname, "wb")
            data = data.replace("#FILE:" + filename + extension + ":", "")
            newFile.write(data)
            print "* File \"%s\" received *" % (newname)
        except:
            print "* File NOT received *"

    def write(self):
        """
        Reads in data from stdin and sends to client
        """
        global doRead

        while self.dowrite:
            data = sys.stdin.readline()
            if data.strip() == self.exitcode:
                print "\n* Leaving conversation... (Waiting for partner's response) *\n"
                self.stopWrite
                doRead = False
            elif data.strip() == "file()":
                FileThread = Thread_Manager('file', self.conn, None, self.private)
                FileThread.start()
                FileThread.join()
                continue

            data = encrypt(data.strip(), self.private)
            self.conn.send("~" + data + "~")

    def file(self):
        """
        Reads and sends file data
        """
        try:
            filename = str(raw_input(
                "\nOnly files located in your current directory are accessible\nEnter filename including extension: "))
            f = open(filename, 'r')
            print "* Encrypting file... (Large files will take time) *"
            data = encrypt("#FILE:" + filename + ":" + f.read(), self.private)
            f.close()
            print "* Sending file \"%s\" ... *" % filename
            self.conn.send("~" + data + "~")
            print "* File sent *"
        except IOError:
            print "* File " + filename + " does not exist *"


"""
Main - Checks for correct input arguments and runs the appropriate methods
"""

TESTING = False

print ""
print "------------------------------------------------------"
print "                 ENCRYPTED CHAT v1.0                  "
print "------------------------------------------------------"

if TESTING:
    host = 'localhost'
    port = 1337
else:
    if (len(sys.argv) < 3):
        print "\nUsage: python encryptedChat.py <hostname/IP> <port>\n"
        raw_input("Press any key to quit")
        exit(0)
    host = sys.argv[1]
    port = sys.argv[2]

doRead = True
try:
    Client(host, port)
except Exception, e:
    if TESTING:
        print e
        pass
    print "* Server was not found. Creating server... *\n"
    try:
        Server(host, port)
    except Exception, e:
        if TESTING:
            print e
            pass
        print "* ERROR creating server *\n"

print "\n* Exiting... Goodbye! *"
