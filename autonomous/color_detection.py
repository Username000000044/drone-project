import cv2 as cv
import numpy as np
from config.load_config import load_config_file

color_ranges, color_order = load_config_file(
    "./config/color_ranges.json", 
    ["color_ranges", "initial_color_order"]
)

def detect_hoop_center(frame, color_range, target_color=None):
    """
    Detects a colored hoop using HSV filtering.
    Returns:
        - The processed frame (with drawings),
        - The centroid (always usable),
        - The full circle center (only if enough of the hoop is seen),
        - The detected color (if found).
    """
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Unpack the lower and upper HSV bounds for the desired color
    lower = np.array(color_range[0], dtype=np.uint8)  # Lower HSV bound
    upper = np.array(color_range[1], dtype=np.uint8)  # Upper HSV bound

    # Create a mask: white where color is in range, black elsewhere
    mask = cv.inRange(hsv, lower, upper)

    # Apply operations to clean noise in the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask, kernel, iterations=1)  # Shrinks white regions (removes noise)
    mask = cv.dilate(mask, kernel, iterations=2)  # Expands white regions (restores shape)

    # Found contours (shapes) in the masked image
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    contour_centroid = None
    circle_center = None
    detected_color = None  # To store color of the detected hoop

    frame_height, frame_width = frame.shape[:2]  # Get the frame dimensions

    for contour in contours:
        area = cv.contourArea(contour)

        # Skip tiny contours (likely noise)
        if area < 300:
            continue

        M = cv.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])  # X-cord of centroid
            cy = int(M['m01'] / M['m00'])  # Y-cord of centroid
            contour_centroid = (cx, cy)

            # Draw centroid on the frame as a red dot
            cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv.putText(frame, "Centroid", (cx + 10, cy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        else:
            continue  # Invalid moments

        # Check if a circle can safely fit
        if len(contour) >= 5:
            (x, y), radius = cv.minEnclosingCircle(contour)

            # Accept circle only if radius is reasonable and center is inside the frame
            if 20 < radius < 150 and 50 < x < frame_width - 50 and 50 < y < frame_height - 50:
                circle_center = (int(x), int(y))

                # Draw the fitted circle and its center
                cv.circle(frame, circle_center, int(radius), (0, 255, 0), 2)
                cv.circle(frame, circle_center, 5, (255, 0, 0), -1)
                cv.putText(frame, "Circle Center", (int(x) + 10, int(y)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                # Process only one valid contour (skip rest)
                break

        # Determine the color of the detected hoop (based on color range)
        if target_color:
            detected_color = target_color

    return frame, contour_centroid, circle_center, detected_color

def detect_hoops_in_frame(frame, color_order, color_ranges):
    """
    Detect all hoops in the frame by checking multiple colors.
    Updates the color order as hoops are passed.
    Returns a list of tuples containing the frame with hoops drawn, and the detected colors.
    """
    # Initialize a list to hold the results
    results = []

    # Loop through each color range and detect hoops
    for color_name, color_range in color_ranges.items():
        processed_frame, centroid, circle_center, detected_color = detect_hoop_center(frame, color_range, target_color=color_name)

        # If a hoop of the correct color is detected, add it to the results
        if detected_color:
            # If the color is the next color in the color order list
            if color_order and color_order[0] == detected_color:
                # Remove the detected color from the color order list
                color_order.pop(0)  # Remove the first item
                print(f"👓 Detected {detected_color}, moving to the next hoop!")

            results.append((processed_frame, detected_color, centroid, circle_center))

    return results, color_order
