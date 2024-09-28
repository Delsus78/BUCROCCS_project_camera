---

# Camera Control and UDP Client

This project provides a system for controlling a camera, capturing images, and optionally sending them to a server via UDP. It includes multiple Python modules responsible for various tasks such as camera control, UDP communication, and image processing.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- asyncio

### Python Libraries

You need to install the following Python libraries:

```bash
pip install opencv-python
```

## Overview

This system captures images from a camera, displays them in a window, and saves them periodically. It can also send the captured images to a UDP server if configured to do so.

### Main Components

1. **main.py**
   - Entry point for the application. It initializes the `CameraControleur` with parameters like camera index, interval, and whether to send data via UDP.
   - Accepts command-line arguments for customization:
     - First argument: Camera index (e.g., `0` for the first camera).
     - Second argument (optional): `--no-udp` disables sending data to a UDP server.
     - Third argument (optional): Interval in minutes for saving images.

2. **CameraControleur.py**
   - Manages the main control loop for the camera, saving images periodically and optionally sending them to a UDP server.
   - Key responsibilities:
     - Starting and stopping the camera.
     - Handling the main loop for capturing and processing images.
     - Sending images to the server if enabled.
     - Saving images in the local folder at defined intervals.

3. **CameraModel.py**
   - Responsible for interacting with the camera using OpenCV (`cv2`).
   - Provides methods for capturing images, flipping them, and saving them to the file system.
   - Includes a method to convert the image to a Base64 string for easy transmission over UDP.

4. **UdpClient.py**
   - Handles communication with the UDP server.
   - Sends serialized image data to the server in a non-blocking, asynchronous manner.
   - Reinitializes the socket in case of errors during transmission.

## How to Run

### Basic Usage

1. Make sure your camera is connected and properly set up.
2. Run the application using the following command:

```bash
python main.py <camera_index> [--no-udp] [interval]
```

- `<camera_index>`: Index of the camera to use (e.g., `0` for the default camera).
- `--no-udp`: Optional flag to disable UDP transmission of images.
- `[interval]`: Optional argument to specify the time interval in minutes for saving images (default: 60 minutes).

### Example

```bash
python main.py 0 --no-udp 30
```

This command will run the camera with index `0`, disable UDP transmission, and save images every 30 minutes.

## Folder Structure

Images are saved in a folder named `images` under a subdirectory based on the current date and camera index. Each image is named with a timestamp (e.g., `image_20240928-123000.jpg`).

## UDP Communication

If UDP transmission is enabled (i.e., if `--no-udp` is not used), images will be converted to a Base64-encoded string and sent to a server at the specified IP and port. The server settings are hardcoded in the `CameraControleur` file as follows:

- Server IP: `udpserver.bu.ac.th`
- Server Port: `5005`

## Extending the System

- You can modify the `UdpClient` class to change the server IP or port.
- Adjust the image quality or size in `CameraModel` to optimize performance.
- The `interval` parameter in the `main.py` file can be adjusted to fit your needs for how often images are saved.

## Error Handling

- The system will attempt to reconnect and reinitialize the UDP socket if any errors occur during transmission.
- If no camera is found or there's an issue capturing images, an error message is displayed in the console.

---
