from pupil_labs.realtime_api.simple import discover_one_device
import cv2
import numpy as np

# Discover the device
device = discover_one_device()

# Create a named window
cv2.namedWindow("Scene Video", cv2.WINDOW_NORMAL)

try:
    while True:
        # Receive scene video frame and gaze data
        scene_sample, gaze_sample = device.receive_matched_scene_video_frame_and_gaze()
        
        # Convert the scene image from BGR to RGB
        scene_image_rgb = cv2.cvtColor(scene_sample.bgr_pixels, cv2.COLOR_BGR2RGB)
        
        # Convert the image to a format suitable for display
        scene_image_bgr = cv2.cvtColor(scene_image_rgb, cv2.COLOR_RGB2BGR)

        # Draw gaze data on the image
        if gaze_sample.x is not None and gaze_sample.y is not None:
            gaze_x = int(gaze_sample.x)
            gaze_y = int(gaze_sample.y)
            
            # Draw a circle at the gaze coordinates
            cv2.circle(scene_image_bgr, (gaze_x, gaze_y), 10, (0, 0, 255), 2)  # Red circle

        # Display the image
        
        cv2.imshow("Scene Video", scene_image_bgr)
        cv2.resizeWindow("Scene Video", 640, 480)
        
        # Exit on keypress (e.g., 'q' or 'Esc')
        if cv2.waitKey(1) & 0xFF in [27, ord('q')]:  # 27 is the ESC key, 'q' is for quit
            break

finally:
    # Release resources
    cv2.destroyAllWindows()
