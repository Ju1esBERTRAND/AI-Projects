import cv2
import numpy as np
from ultralytics import YOLO
np.bool = np.bool_

model = YOLO("yolov8n.engine", task="detect")
cap = cv2.VideoCapture(0)
width = int(cap.get(3))
height = int(cap.get(4))


video_capture = cv2.VideoWriter('video_test.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, (width, height))


line_x = width // 2  
object_tracks = {}

in_count = 0
out_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    results = model.track(frame, classes=0, persist=True)
    current_objects = {}

    for result in results:
        res_plotted = results[ 0 ].plot()
        box = result.boxes.cpu()
        box_sz = box.xyxy.numpy()
        if box_sz.size !=0 :
            x = int(box_sz[0][0])
            y = int(box_sz[0][1])
            xim = int(box_sz[0][2])
            yim = int(box_sz[0][3])
            cv2.circle( res_plotted, (x, y), 4, (0, 0, 255), -1 )
            cv2.line(res_plotted,(x,y),(xim,yim),(255,0,0),2)
        for box in result.boxes:
            class_id = int(box.cls[0])
            if class_id == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2


                object_id = len(current_objects) + 1
                current_objects[object_id] = center_y

                cv2.rectangle(res_plotted, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(res_plotted, (center_x, center_y), 4, (0, 0, 255), -1)


                if object_id in object_tracks:
                    previous_x = object_tracks[object_id]
                    if previous_x < line_x and center_x >= line_x:
                        in_count += 1
                    elif previous_x > line_x and center_x <= line_x:
                        out_count += 1


                object_tracks[object_id] = center_x


    cv2.line(res_plotted, (line_x, 0), (line_x, height), (255, 0, 0), 2)


    cv2.putText(res_plotted, f"COUNT: {in_count - out_count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    video_capture.write(res_plotted)
    cv2.imshow("Object Counter", res_plotted)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
video_capture.release()
print("The video was successfully saved") 
cap.release()
cv2.destroyAllWindows()

