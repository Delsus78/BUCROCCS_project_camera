import asyncio

from CameraModel import CameraModel
from UdpClient import UdpClient

server_ip = "udpserver.bu.ac.th"
server_port = 5005


class CameraControleur:
    def __init__(self, vidIndex):
        self.camera = CameraModel(vidIndex)
        self.udp_client = UdpClient(server_ip, server_port)
        self.running = True

    def get_image(self):
        # Retrieve the image as a JSON string
        return self.camera.getStringVersionOfActualFrame()

    async def start_camera(self):
        self.camera.start()

    async def send_image_to_server_periodically(self):
        while self.running:
            image = self.get_image()
            if image is not None:
                print(image)
                await self.udp_client.retrieve_data("SET", "camera", json_data=image)
            else:
                print("No image retrieved from camera, Skipping ...")

            # sleep for 3 seconds
            await asyncio.sleep(3)

    async def run(self):
        camera_task = asyncio.create_task(self.start_camera())
        image_sender_task = asyncio.create_task(self.send_image_to_server_periodically())

        await asyncio.gather(camera_task, image_sender_task)

    def stop(self):
        self.running = False
        self.camera.stop()