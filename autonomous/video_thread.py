import threading
import time

class VideoStream:
    def __init__(self, tello):
        self.tello = tello

        self.frame = None
        self.is_running = True

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start() 
        
    
    def get_frame(self):
        return self.frame
    
    def update(self):
        while self.is_running:
            try:
                self.frame = self.tello.get_frame_read().frame
            except Exception as e:
                print(f"⚠️ Error getting frame: {e}")

                # Without would rapidly hit the exception over and over.
                # Causing consume 100% CPU, causing instability.
                time.sleep(0.1)

    def stop(self):
        self.is_running = False
        self.thread.join()