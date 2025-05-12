import time
import cv2 as cv
from video_stream import TelloVideoStream # 📽️ Video stream manager
from color_detection import detect_hoops_in_frame
from config.load_config import load_config_file
from control import DroneController  # 🚁 Drone controller

def main():
    # Load configurations
    load_config_file

    color_ranges, color_order = load_config_file(
    "./config/color_ranges.json", 
    ["color_ranges", "initial_color_order"]
)
    video_settings, drone_settings = load_config_file(
    "./config/settings.json", 
    ["video_settings", "drone_settings"]
)

    if video_settings is None or drone_settings is None:
        print("❌ Unable to load settings. Exiting.")
        return

    # Initialize video stream
    stream = TelloVideoStream(width=video_settings["width"], height=video_settings["height"])
    stream.start()
    print(f"📻 Video stream started at {video_settings['width']}x{video_settings['height']}")

    # Initialize drone controller
    controller = DroneController(drone_settings)
    controller.takeoff()

    time.sleep(2)  # Let video stabilize

    frame_counter = 0
    frame_skip_interval = video_settings['frame_skip_interval']

    try:
        while stream.is_running():
            frame = stream.read()

            if frame is None:
                continue

            # Skip frames based on the frame skip interval
            if frame_counter % frame_skip_interval == 0:

                frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)  # (x, y)

                results, color_order = detect_hoops_in_frame(frame, color_order, color_ranges)

                for processed_frame, detected_color, centroid, circle_center in results:
                    if centroid:
                        print(f"🔵 Centroid of {detected_color} at {centroid}")
                    if circle_center:
                        print(f"🟡 Circle center of {detected_color} at {circle_center}")
                    
                    # 🧠 Control drone based on detection
                    controller.update(centroid, circle_center, frame_center)

                    # Show frame for debugging
                    cv.imshow("Drone View", processed_frame)

            frame_counter += 1  # Increment the frame counter

            key = cv.waitKey(1)
            if key == 27:  # ESC to quit
                break

    except Exception as e:
        print(f"❌ [Main] Error: {e}")
        controller.emergency_stop()

    finally:
        print("❎ Stopping...")
        controller.land()
        stream.stop()
        cv.destroyAllWindows()

if __name__ == "__main__":
    main()
