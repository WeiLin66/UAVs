import cv2 
import threading

cap = cv2.VideoCapture("rtsp://221.120.82.20:8554/test")
ret,frame = cap.read()

# Image frame sent to the Flask object
global video_frame
video_frame = None

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock 
thread_lock = threading.Lock()


while ret:
    ret,frame = cap.read()
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
