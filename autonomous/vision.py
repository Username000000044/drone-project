"""
Main Thread (vision.py)
 ├── Tello control logic
 ├── VideoStream (Thread) → Grabs frames
 ├── HoopDetectorProcess (Process) → Analyzes frames
 └── Queue ↔ Used to pass frames & results between them

threading.Queue for a thread reaidng frames from drone's camera
multiprocessing.Queue for sending drone camera's frames from the main thread for the detection process.

"""

from djitellopy import Tello
from video_thread import VideoStream
from hoop_detection import HoopDetection
from color_config import color_ranges, hoops_sequence
 
import multiprocessing
import cv2 as cv

def main():
    tello = Tello()

    # Connect drone
    tello.connect()
    print("✅ Tello sucessfully connected.")

    # Start tello stream
    tello.streamon()
    print("📹 Camera sucessfully activated.")

    video_stream = VideoStream(tello)

    # Queues
    frame_queue = multiprocessing.Queue(maxsize=5)
    product_queue = multiprocessing.Queue()

    # Start multiprocessing hoop detector
    detector = HoopDetection(
        frame_queue=frame_queue,
        product_queue=product_queue,
        color_ranges=color_ranges,
        sequence=hoops_sequence
    )
    detector.start()

    try:
        while True:
            frame = video_stream.get_frame()

            if not frame_queue.full():
                frame_queue.put(frame)

            if not product_queue.empty():
                center, radius = product_queue.get()
                if center and radius:
                    print(f"🎯 Hoop center: {center}, Radius: {radius}")
                    
                    # Center and Outline hoop identification circles.
                    cv.circle(frame, center, 2, (0, 0, 255), 2)
                    cv.circle(frame, center, radius, (255, 0, 0), 2)
                    
                else:
                    print(f"🔍 No hoop detected.")

                cv.imshow("Drone Feed", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("🛑 Exiting...")

    finally:
        # Shuts down queues and detector
        """ ====== hoop_detector.py ======
            while True:
                frame = self.frame_queue.get()
                if frame is None:
                    break
        """
        frame_queue.put(None)
        detector.join()
        tello.streamoff()
        cv.destroyAllWindows()
    
if __name__ == "__main__":
    multiprocessing.set_start_method('spawn') # For window support
    main()