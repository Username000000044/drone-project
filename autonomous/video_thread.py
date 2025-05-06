import threading

class VideoStream:
    def __init__(self, tello):
        self.tello = tello

        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

        self.running = True
    
    def get_frame(self):
        return self.frame
    
    def update(self):
        while self.running:
            self.frame = self.tello.get_frame_read().frame

    def stop(self):
        self.running = False
        self.thread.join()