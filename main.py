import cv2
import time

def track_object(video_source):
    # Create a video capture object
    cap = cv2.VideoCapture(video_source)

    time.sleep(0.5)

    # Read the first frame
    success, frame = cap.read()

    # Flip the frame horizontally (mirror it)
    frame = cv2.flip(frame, 1)

    if not success:
        print("Failed to read video")
        return

    # Let user select the bounding box
    bbox = cv2.selectROI("Frame", frame, False)
    cv2.destroyWindow("Frame")

    # Initialize CSRT tracker
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, bbox)

    # Initialize FPS calculation
    fps = 0
    frame_count = 0
    start_time = time.time()

    while True:
        # Read a new frame
        success, frame = cap.read()

        # Flip the frame horizontally (mirror it)
        frame = cv2.flip(frame, 1)

        if not success:
            break

        # Update the tracker
        success, bbox = tracker.update(frame)

        # Draw the bounding box
        if success:
            (x, y, w, h) = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Tracking failure", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Calculate and display FPS
        frame_count += 1
        end_time = time.time()
        fps = frame_count / (end_time - start_time)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Tracking", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# For a video file
#track_object("/Users/zheka/Downloads/MOT17-11-raw.webm")

# For a webcam or video stream
track_object(0)  # 0 is typically the ID for the default webcam
