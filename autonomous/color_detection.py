from multiprocessing import Process, Queue, set_start_method
set_start_method('spawn')
import cv2 as cv

colorRanges = {
    "red": { "lower": [], "upper": []},
}

class ColorDetection():
    def __init__(self, frame):
        self.frame = frame

        self.multi_queue = Queue()

        self.multi_process = Process(target=self.find_hoops, daemon=True)
        self.multi_process.start()
    
    def find_hoops(self):
        self.img = cv.imread(self.frame, flags=cv.IMREAD_COLOR)

        # hoop detection logic with colors
        #!https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/