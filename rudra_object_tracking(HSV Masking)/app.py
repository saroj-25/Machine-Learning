from flask import Flask, render_template, Response
import cv2
from detection.color_tracker import ColorTracker

app=Flask(__name__)
tracker=ColorTracker()
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(5,15)

def gen_frames():
 while True:
    ret,frame=cap.read()
    if not ret:
        continue
    frame,centers,color_name=tracker.track(frame)
    cv2.putText(frame,f"Detected: {color_name}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    ret,buffer=cv2.imencode('.jpg',frame)
    frame=buffer.tobytes()
    yield(b'--frame\r\n'
          b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')

@app.route('/')
def index():
 return render_template('index.html')

@app.route('/video')
def video():
 return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
 print("Press 'c' to capture frame jpg, 'e' to exit")
 while True:
    ret,frame=cap.read()
    if not ret:
        continue
    frame,centers,color_name=tracker.track(frame)
    cv2.putText(frame,f"Detected: {color_name}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow("Color Tracker",frame)
    key=cv2.waitKey(50) & 0xFF
    if key==ord('c'):
        tracker.save_frame(frame,color_name)
    elif key==ord('e'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
app.run(debug=False)
