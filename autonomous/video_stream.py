# Use: Setting up video stream using ffmpeg and djitellopy to capture video frames.

import subprocess
import threading
import numpy as np
import cv2 as cv
import time

class TelloVideoStream:
    def __init__(self, width=960, height=720):
        self.width = width
        self.height = height
        self.frame_size = self.width * self.height * 3 # In bytes o width * height gives number of pixels, * 3 is for each of the red, green and blue channels. # 921,600 bytes (or 0.92 MB)
        self.frame = None
        self.lock = threading.Lock() # #nsures thread-safe access to the frame
        self.running = False
        self.proc = None # Holds the ffmpeg subprocess

    def start(self):
        """
        Starts the video stream using ffmpeg in a subprocess.
        A background thread is also started to read the frames continously
        """
        try: # creates and starts a new process, running the specified command (ffmpeg in this case), and allows interaction with its input/output streams (stdin, stdout, stderr).
            self.proc = subprocess.Popen(
                [
                    'ffmpeg',
                    '-i',
                    'udp://0.0.0.0:11111',  # Input stream (UDP port)
                    '-f',
                    'rawvideo',  # Output format is raw video
                    '-pix_fmt',
                    'bgr24',  # Pixel format is BGR (Blue, Green, Red)
                    '-loglevel',
                    'quiet', '-'
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except FileNotFoundError:
            raise RuntimeError("❌ FFmpeg not found. Is it installed and added to PATH?")
        
        self.running = True # Marks stream as running

        # Start thread to continuouly fetch frames
        thread = threading.Thread(target=self._update_frame, daemon=True)
        thread.start()

    def _update_frame(self):
        """
        Continously reads frames from the ffmpeg subpress and stores them
        """
        while self.running:
            try:
                # Read a raw frame of the specified size from subprocess
                raw_frame = self.proc.stdout.read(self.frame_size)
                if not raw_frame:
                    continue # skip if no data is recieved

                # convert raw byte data into numpy array and reshape into an image (height x width x channels)
                frame = np.frombuffer(raw_frame, np.uint8).reshape((self.height, self.width, 3))

                # Acquire the lock before updatin the frame to ensure thread safety
                with self.lock:
                    self.frame = frame
            
            except Exception as e:
                print(f"❌ [VideoStream] Error: {e}")
                break  # Break if an error occurs (e.g., subprocess terminates)
    
    def read(self):
        """
        Returns nthe most recent frame.
        Makes a copy of the frame to avoid data corruption due to threading.
        """
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
        
    def stop(self):
        """
        Stop the video stream gracefully by terminating the ffmpeg subprocess.
        """
        self.running = False
        if self.proc:
            self.proc.terminate() # terminate the subprocess
            self.proc.wait() # Wait for the process to exit cleanly
    
    def is_running(self):
        """
        Returns the status boolean of the video stream (whether it's still running).
        """
        return self.running