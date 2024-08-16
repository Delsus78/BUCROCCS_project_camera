import asyncio
import sys
import time

from CameraControleur import CameraControleur


async def main(camIndex):
    controleur = CameraControleur(camIndex)
    try:
        await controleur.run()
    except KeyboardInterrupt:
        controleur.stop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        asyncio.run(main(int(sys.argv[1])))
    else:
        print("Please provide the camera index")
        sys.exit(1)
