import sys

from CameraControleur import CameraControleur


def main(camIndex):
    controleur = CameraControleur(camIndex)
    try:
        controleur.run()
    except KeyboardInterrupt:
        controleur.stop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        camIndex = int(sys.argv[1])
        sendDataToUDPNeeded = true

        if len(sys.argv) > 2 and sys.argv[2] == '--no-udp'
            sendDataToUDPNeeded = false

        main(camIndex, sendDataToUDPNeeded)
    else:
        print("Please provide the camera index")
        sys.exit(1)
