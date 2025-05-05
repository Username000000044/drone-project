"""
*   THREADING LOGIC:
*   One thread reads the frames
*   One thread processes the most recent frame
"""

from video_stream import VideoStream
from flight_controls import TelloController
import threading
import numpy as np
import cv2 as cv
import queue

streamToggle = True # True = webcam, False = drone
processed_frame = None # frame to display for frame_processor    

# Detects rings and displays them to window
def detect_rings(frame):
    # Copy frame to not edit the original
    img = frame.copy()

    # Convert BGR to grayscale as circle detection does not need color
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Apply blur
    # gray = preprocessed image
    # ksize=(9, 9) means a 8x8 pixel window is used to calc blur
    # sigmaX=0 lets OpenCV calculate the standard deviation automatically.
    gray_blurred = cv.GaussianBlur(
        gray,
        ksize=(9, 9),
        sigmaX=0,
    )

    # Detects circles in the image
    # gray_blurred = preprocessed image
    # cv.HOUGH_GRADIENT: The detection method.
    # dp=1.2: The inverse ratio of resolution. 1.2 means the accumulator has ~80% the resolution of the image. Makes drawing circles faster, but the accuracy is less.
    # minDist=80: Minimum distance between circle centers (prevents multiple detections of same ring).
    # param1=80: First parameter for the internal Canny edge detector.
    # param2=30: Threshold for center detection; lower = more circles, more false positives.
    # minRadius and maxRadius: Filters out circles too small or large.
    detected_circles = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        dp=1,
        minDist=80,
        param1=80,
        param2=30,
        minRadius=30,
        maxRadius=200,
    )

    # If circles are detected
    if detected_circles is not None:
        
        # rounds the detected circle corrdinates sand contects them to 16-bit unsigned integers for drawing
        detected_circles = np.uint16(np.around(detected_circles))

        # Sorts detected circles by radius (c[2]) in decending order to find the largest one.
        circles_sorted = sorted(
            detected_circles[0, :], 
            key=lambda c: -c[2]  # Sort by radius in descending order
            )

        # Selects the largest circle, and unpacks:
        # a, b = x and y center coordinates
        # r = radius
        most_prominent_circle = circles_sorted[0]
        a, b, r = most_prominent_circle[0], most_prominent_circle[1], most_prominent_circle[2]

        # Green outer circle
        cv.circle(img, (a, b), r, (0, 255, 0), 2)

        # Red center circle
        cv.circle(img, (a, b), 1, (0, 0, 255), 3)

        # Return drawn-on image with center x,y points
        return img, (a, b)

    # If no circle detected, return original image and no x,y cords
    return img, None

# Frame processing thread
# processes frames from the frame_queue
def frame_processor(frame_queue, tello_controller):
    global processed_frame

    # Center of frame of img 1280x720 resolution
    frame_center = (1280 // 2, 720 // 2) 
    # continuously checking for new frames

    # Keeps running the loop forever to continusly process frames.
    while True:

        # Checks if queue is not empty
        if not frame_queue.empty():
            print("✅ Frame found in queue...")
            # Process the latest frame
            frame = frame_queue.get()

            # calls detect_rings() function
            #process_image = frame with drawn circles
            # ring_center = x,y center of detected ring, or None if no ring is found
            processed_img, ring_center = detect_rings(frame)

            #Stores the processed frame with drawing so it can be displayed later.
            processed_frame = processed_img
            
            # If a ring was detected.
            if ring_center is not None and tello_controller:

                # Calcs how far the ring is form the center of the frame
                x_offset = ring_center[0] - frame_center[0] # x_offset > 0 ring is to the right -> move right
                y_offset = ring_center[1] - frame_center[1] # y_offset > 0 ring is below center -> move down.
                
                # Calls move_towards in TelloController object to adjust drone pos.
                tello_controller.move_towards(x_offset, y_offset)

# Main frame proccessing logic
def main():

     # Determine source based on streamToggle
    if streamToggle:
        print("🧪 Using webcam for testing.")
        stream = VideoStream(source=0, is_tello=False).start()
    else:
        print("🚁 Using Tello drone camera.")
        stream = VideoStream(source=0, is_tello=True).start()

    print("✅ Video stream started. Press 'd' to quit.")

    # Creates a thread safe queue with max size of 10 to fold frames
    # maxsize prevents queue from growing too large
    frame_queue = queue.Queue(maxsize=10)

    # Only create drone controller if using drone
    tello_controller = TelloController() if not streamToggle else None
    if tello_controller:
        tello_controller.takeoff()

    #Starts frame processing thread. Will run frame_processor() and processes them in queue
    processor_thread = threading.Thread(target=frame_processor, args=(frame_queue, tello_controller), daemon=True)

    # Starts the frame processing thread
    processor_thread.start()

    # Continuosly fetches the latest frame
    while True:
        
        # ret is a boolean for success
        # frame is the image itself
        ret, frame = stream.read()

        # Skips processing if frame wasn't read correctly.
        if not ret:
            print("⚠️ Frame not read properly.")
            continue
    
        # If the queue is not full
        if not frame_queue.full():
            # Adds frame into queue
            frame_queue.put(frame)

        # If the processed_frame exists
        if processed_frame is not None:
            print("🔃 Displaying frame...")
            # Displays the proceessed frame with circles in window.
            cv.imshow("Detected Circle", processed_frame)

        # in the current frame, wait 1ms for key press
        # exits if 'd' pressed
        if cv.waitKey(1) & 0xFF == ord('d'):
            break

    # Lands drone, stops the video steam and closes OpenCV windows.
    if tello_controller:
        tello_controller.land()
    stream.stop()
    cv.destroyAllWindows()

    print("🔚 Stream stopped.")

# Runs main() function only if this script is run directly
# Catches and prints any errors that occur during execution.
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")