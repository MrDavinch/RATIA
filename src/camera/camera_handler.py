# Lógica para conexión, selección y captura

import cv2

class CameraHandler:
    def __init__(self, index=0):
        self.index = index
        self.last_frame = None
        self.cap = None
        self.connected = False   

    def connect(self):
        self.cap = cv2.VideoCapture(self.index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.connected = self.cap.isOpened()
        return self.connected

    def read_frame(self):
        if self.connected and self.cap:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release(self):
        if self.cap:
            self.cap.release()
        self.cap = None
        self.connected = False
