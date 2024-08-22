import asyncio
from datetime import datetime
import time

from CameraModel import CameraModel
from UdpClient import UdpClient

server_ip = "udpserver.bu.ac.th"
server_port = 5005


class CameraControleur:
    def __init__(self, vidIndex):
        self.camera = CameraModel(vidIndex)
        self.udp_client = UdpClient(server_ip, server_port)
        self.loop = asyncio.get_event_loop()
        self.running = True
        self.last_executed_hour = None

    def get_image(self):
        return self.camera.getActualFrame()

    def get_image_as_json(self):
        return self.camera.getActualFrameAsJson()

    async def start_camera(self):
        self.camera.start()

    async def main_loop(self):
        while self.running:
            self.camera.camera_loop()

            await self.send_image_to_server_periodically()
            self.save_image_in_folder()

            await asyncio.sleep(3)

    async def send_image_to_server_periodically(self):
        print("Sending image to server ...")
        image = self.get_image_as_json()
        if image is not None:
            await self.udp_client.send_data_only("SET", "farm2000_camera", json_data=image)
        else:
            print("No image retrieved from camera, Skipping ...")

    def save_image_in_folder(self):
        image = self.get_image()

        current_time = datetime.now()
        current_hour = current_time.hour

        if current_hour != self.last_executed_hour:
            if current_time.minute == 0:
                image_name = f"image_{time.strftime('%Y%m%d-%H%M%S')}.jpg"
                self.camera.save_image(image_name, image)
                print(f"Image saved as {image_name}")

                self.last_executed_hour = current_hour

    def run(self):
        self.loop.run_until_complete(self.main_loop())

    def stop(self):
        self.running = False
        self.camera.stop()
