import cv2

def main():
    # Create a VideoCapture object and set the video source to the PiCam
    cap = cv2.VideoCapture(0)
    
    # Check if the camera was opened successfully
    if not cap.isOpened():
        print("Failed to open the camera")
        return
    
    # Set the video frame width and height (adjust as needed)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Create a window to display the video
    cv2.namedWindow("PiCam Stream", cv2.WINDOW_NORMAL)
    
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        
        # If frame read is not successful, then break the loop
        if not ret:
            break
        
        # Flip the frame vertically
        flipped_frame = cv2.flip(frame, 0)
        
        # Display the flipped frame in the "PiCam Stream" window
        cv2.imshow("PiCam Stream", flipped_frame)
        
        # Check for keypress and exit if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
    
    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
