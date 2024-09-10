import asyncio
from datetime import datetime
import time

from CameraModel import CameraModel
from UdpClient import UdpClient

server_ip = "udpserver.bu.ac.th"
server_port = 5005


class CameraControleur:
    def __init__(self, vidIndex, sendDataToUDPNeeded, interval=60):
        self.camera = CameraModel(vidIndex)
        self.udp_client = UdpClient(server_ip, server_port)
        self.loop = asyncio.get_event_loop()
        self.running = True
        self.last_executed_interval = None
        self.sendDataToUDPNeeded = sendDataToUDPNeeded
        self.interval = interval

    def get_image(self):
        return self.camera.getActualFrame()

    def get_image_as_json(self):
        return self.camera.getActualFrameAsJson()

    async def start_camera(self):
        self.camera.start()

    async def main_loop(self):
        while self.running:
            self.camera.camera_loop()

            if self.sendDataToUDPNeeded:
                await self.send_image_to_server_periodically()
            
            self.save_image_in_folder(self.interval)

            if self.sendDataToUDPNeeded:
                await asyncio.sleep(3)

    async def send_image_to_server_periodically(self):
        print("Sending image to server ...")
        image = self.get_image_as_json()
        if image is not None:
            await self.udp_client.send_data_only("SET", "farm2000_camera", json_data=image)
        else:
            print("No image retrieved from camera, Skipping ...")

    def save_image_in_folder(self, interval):
        image = self.get_image()

        current_time = datetime.now()
        # get the current interval, i.e. the current hour and minute
        current_interval = current_time.strftime('%H:%M')

        if current_interval != self.last_executed_interval:
            if current_time.minute % interval == 0:
                image_name = f"image_{time.strftime('%Y%m%d-%H%M%S')}.jpg"
                today_date = time.strftime('%Y%m%d')
                image_path = f"images\\{today_date}"
                self.camera.save_image(image_path, image_name, image)

                self.last_executed_interval = current_time.strftime('%H:%M')

    def run(self):
        self.loop.run_until_complete(self.main_loop())

    def stop(self):
        self.running = False
        self.camera.stop()
