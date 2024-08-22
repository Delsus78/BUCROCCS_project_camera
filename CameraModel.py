import base64
import json

import cv2


class CameraModel:
    def __init__(self, vidIndex):
        self.cap = cv2.VideoCapture(vidIndex)

    def start(self):
        cv2.namedWindow("preview")

        if self.cap.isOpened():  # try to get the first frame
            rval, frame = self.cap.read()
        else:
            print("Error: Camera not found")
            rval = False

        if rval:
            cv2.imshow("preview", frame)

    def camera_loop(self):
        rval, frame = self.cap.read()

        cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            self.cap.release()
            cv2.destroyWindow("preview")

    def save_image(self, image_name, image):
        cv2.imwrite(image_name, image)

    def stop(self):
        self.cap.release()
        cv2.destroyWindow("preview")

    def getActualFrame(self):
        rval, frame = self.cap.read()
        if rval:
            return frame
        return None

    def getActualFrameAsJson(self):
        frame = self.getActualFrame()

        if frame is not None:
            # Resize the image to reduce size if necessary
            max_height, max_width = 480, 640  # example values, adjust as needed
            frame = cv2.resize(frame, (max_width, max_height), interpolation=cv2.INTER_AREA)

            # Compress the image by adjusting the quality to ensure it fits within 1024 bytes
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]  # Adjust quality as needed
            _, buffer = cv2.imencode('.jpg', frame, encode_param)

            # Check buffer size and adjust if necessary
            while len(buffer) > 1024:
                encode_param[1] -= 5  # Reduce quality
                _, buffer = cv2.imencode('.jpg', frame, encode_param)
                if encode_param[1] <= 10:  # Prevent infinite loop by setting a minimum quality
                    break

            # Convert to Base64
            encoded_image = base64.b64encode(buffer).decode('utf-8')

            # Return the JSON object
            return json.dumps({"image": encoded_image})
        return None
