from threading import Lock

from .tcp_server import TcpServer
from .udp_server import UdpServer


class Server:
    def __init__(self, address, tcp_port, udp_port):
        self.address = address
        self.tcp_port = tcp_port
        self.udp_port = udp_port

    def start(self):
        lock = Lock()

        udp_server = UdpServer(self.address, self.udp_port, lock, self)
        tcp_server = TcpServer(self.address, self.tcp_port, lock, self)

        udp_server.start()
        tcp_server.start()

        is_running = True

        print("Game Server")
        print("------------------------")
        print("list - lists connected users")
        # print("")
        print("------------------------")

        while is_running:
            cmd = input("> ")
            if cmd == "list":
                print("Yo yo")
            elif cmd == "quit":
                print("Shutting down server...")
                udp_server.is_listening = False
                tcp_server.is_listening = False
                is_running = False

        udp_server.join()
        tcp_server.join()
