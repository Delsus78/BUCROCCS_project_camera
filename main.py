import sys

from CameraControleur import CameraControleur


def main(camIndex, sendDataToUDPNeeded, interval):
    controleur = CameraControleur(camIndex, sendDataToUDPNeeded, interval)
    try:
        controleur.run()
    except KeyboardInterrupt:
        controleur.stop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        camIndex = int(sys.argv[1])
        sendDataToUDPNeeded = True
        interval = 60

        if len(sys.argv) > 2 and sys.argv[2] == '--no-udp':
            sendDataToUDPNeeded = False

        if len(sys.argv) > 3:
            interval = int(sys.argv[3])

        main(camIndex, sendDataToUDPNeeded, interval)
    else:
        print("Please provide the camera index")
        sys.exit(1)
