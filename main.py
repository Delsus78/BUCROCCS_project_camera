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
        main(camIndex)
    else:
        print("Please provide the camera index")
        sys.exit(1)
