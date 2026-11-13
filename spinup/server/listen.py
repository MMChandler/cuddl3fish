class ListeningException(Exception):
    pass


# string to split on to separate client name & message
separator_token = "<SEP>"
global socket


def listen_for_client(client_sockets, client_soc):
    global socket
    socket = client_soc
    while True:
        try:
            msg = client_soc.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(client_soc)
        else:
            # if we received a message, replace the <SEP>
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")

        # Iterate over connected sockets, send messages
        for client_socket in client_sockets:
            client_socket.send(msg.encode())
