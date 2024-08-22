import json
import socket
import asyncio


class UdpClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.loop = asyncio.get_event_loop()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)  # Make the socket non-blocking
        self.lock = asyncio.Lock()  # Create a lock

    async def send_data_only(self, command, id_str, json_data=None):
        async with self.lock:

            # sending
            message = f"{command},{id_str}"
            if json_data:
                message += f",{json.dumps(json_data)}"

            self.sock.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))
            #print(f"Data sended to {self.server_ip}:{self.server_port} with message : {message}")

    def close(self):
        self.sock.close()