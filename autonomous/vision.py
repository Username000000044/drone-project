# Start tello camera feed
# define threading queue to process frames
# Gets frames
# .put() Push them to threading queue max=10 or so
# .get() Get current frame in queue
# Detect circles which are the rings
# Detect color of circles
# if the ring the drone sees is the next ring, fly towards the center of the ring
# if no ring, move foward and rotate slowly until ring is spotted
# if no ring at all, land drone.

"""
  +-----------------------+
    |   Camera Thread       |
    |  - Gets frames        |
    |  - Push to queue      |
    +----------+------------+
               |
               v
    +------------------------+
    |  Detection Process     |
    |  - Pulls from queue    |
    |  - Runs detection      |
    |  - Returns results     |
    +------------------------+
"""

# threading.Queue for a thread reaidng frames from drone's camera
# multiprocessing.Queue for sending drone camera's frames from the main thread for the detection process.

from djitellopy import Tello, TelloException

import video_thread
import color_detection

import queue

import logging

# Set logging level to DEBUG to see all messages
# logging.basicConfig(level=logging.DEBUG)

tello = Tello()

try:
    tello.connect()
    print("✅ Tello sucessfully connected.")
except TelloException as e:
    print(f"❌ Tello was unable to connect!")
    exit()

def main():
    #start tello stream
    tello.streamon()

    # get frame from thread and put it into queue
    thread_frame = video_thread.VideoStream(tello)
    frame_queue = queue.Queue(maxsize=10)
    frame_queue.put(thread_frame)

    while True:
        frame = frame_queue.get()
        drawn_frame = color_detection.ColorDetection(frame)



        






if __name__ == "__main__":
    try:
        main()
        print(f"✅ Main function declared.")
    except Exception as e:
        print(f"❌ Error: {e}")

