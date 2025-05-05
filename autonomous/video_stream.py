import threading
import cv2 as cv
from djitellopy import Tello

class VideoStream:
    def __init__(self, source=0, is_tello=False):
        """
        Initialize the video stream.
        source: 0 for webcam, string for video file, or Tello() for drone camera
        is_tello: Boolean flag to specify whether to use the Tello drone or webcam
        """
        self.is_tello = is_tello

        if self.is_tello:
            # Initialize the Tello drone
            self.capture = Tello()
            self.capture.connect()
            self.capture.streamon()
            self.frame_reader = self.capture.get_frame_read()  # Frame reader for Tello
            self.ret, self.frame = False, None  # Initializing the frame values
        else:
            # Initialize the webcam or file capture
            self.capture = cv.VideoCapture(source)
            ret, frame = self.capture.read()
            self.ret, self.frame = ret, frame

        self.stopped = False
        self.lock = threading.Lock()

    def start(self):
        """Start the video stream in a separate thread."""
        threading.Thread(target=self.update, daemon=True).start()
        return self
    
    def update(self):
        """Continuously read frames from the camera (Tello or webcam)."""
        while not self.stopped:
            if self.is_tello:
                # For Tello, get the latest frame using the frame reader
                self.frame = self.frame_reader.frame
                self.ret = self.frame is not None
            else:
                # For webcam, capture the frame
                ret, frame = self.capture.read()
                if not ret:
                    self.stop()  # If failed to capture, stop the stream
                    return
                with self.lock:
                    self.ret = ret
                    self.frame = frame

    def read(self):
        """Return the latest frame."""
        with self.lock:
            return self.ret, self.frame.copy()

    def stop(self):
        """Stop the video stream and release resources."""
        self.stopped = True
        if self.is_tello:
            self.capture.streamoff()  # Stop the Tello stream
        else:
            self.capture.release()  # Release the webcam
