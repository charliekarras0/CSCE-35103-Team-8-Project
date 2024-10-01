import socket
import threading
import struct 

class UDP:
    def __init__(self):
        self.socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.broadcast_port = 7500
        self.broadcast_address = ('<broadcast>', self.broadcast_port)

        self.socket_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_receive.bind(("", 7501))

        self.listen_udp()

    def transmit_equipment_id(self, equipment_id):
        print(f"Transmitting Equipments: {equipment_id}")
        message = struct.pack('!I', equipment_id)
        self.socket_broadcast.sendto(message, self.broadcast_address)

    def receive_data(self):
        while True:
            data, address = self.socket_receive.recvfrom(2048)
            equipment_id_transmitting, hit = struct.unpack('!II', data)
            print(f"Received data from {address}: Transmitting ID: {equipment_id_transmitting}, Hit ID: {hit}")

    def listen_udp(self):
        listen_thread = threading.Thread(target=self.receive_data)
        listen_thread.daemon = True
        listen_thread.start()


