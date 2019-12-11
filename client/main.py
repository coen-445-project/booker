import sys, socket, sqlite3

def main():
    # get server ip address (localhost for now)
    ip_server = socket.gethostbyname(socket.gethostname())
    # open local journal file
    sql_file = sqlite3.connect("server_db.db")

    # ****** UDP Settings ******

    # port number to listen on
    port_bind = 6942
    # port number to send on
    port_send = 6969
    # initialize UDP socket on IPv4
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind to chosen port
    sock.bind((socket.gethostname(), port_bind))
    # set socket to be non-blocking
    sock.setblocking(0)

    print("Main Menu")
    print("q: quit")
    print("s: send message")
    while True:
        inp = input()
        if inp == "s":
            sock.sendto(b'test msg', (ip_server, port_send))
        elif inp == "q":
            exit()



if __name__ == "__main__":
    main()