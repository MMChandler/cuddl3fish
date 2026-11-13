import socket
from threading import Thread
from listen import listen_for_client

# IP & port
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 49152

# string to split on to separate client name & message
separator_token = "<SEP>"

# Socket setup
client_sockets = set()
tcpsoc = socket.socket()
# resusable
tcpsoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsoc.bind((SERVER_HOST, SERVER_PORT))
# tcpsoc.bind(SERVER_HOST)
tcpsoc.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def close_client_sdockets():
    # close client sockets
    for cs in client_sockets:
        cs.close()

    # close server socket
    tcpsoc.close()


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = tcpsoc.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(
        target=listen_for_client,
        args=(
            client_sockets,
            client_socket,
        ),
    )
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
