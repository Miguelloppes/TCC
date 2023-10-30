from ultralytics import YOLO
import cv2
import numpy
import CL
import depth as depth
import threading
# start webcam
cap = cv2.VideoCapture(2)
cap.set(3, 640)
cap.set(4, 480)

distance_floor = 1000
port = '/dev/ttyACM0'
length = 1 
width = 1
# model
model = YOLO("yolo-weights/best.pt")

# object classes
classNames = ["box_top"]
def read_depth():
    while True:
        global depth_value
        depth_value = depth.depth_arduino_ultra(distance_floor, port)

depth_thread = threading.Thread(target=read_depth, daemon=True)
depth_thread.start()


while True:
    try:
        length_previous = length
        width_previous = width
        success, img = cap.read()
        print(success)
        H, W, _ = img.shape
        results = model(img)
        annotaded_frame = results[0].plot()
        #print(results[0].masks)
        for result in results:
            for j, mask in enumerate(result.masks.data):
                mask = mask.cpu().numpy()
                mask = (mask * 255).astype("uint8")
                mask = cv2.resize(mask, (W, H))

        length,width = CL.camera_find_points(mask,depth_value,distance_floor) #Calculo do comprimento e largura 
        if (length == 0 and width == 0):#Caso haja algum erro de identificação a caixa vai utilizar das medidas anteriores 
            CL.display(annotaded_frame,depth_value,length_previous,width_previous)
        else:
            CL.display(annotaded_frame,depth_value,length,width)
    except Exception as exc:
        print(exc)
    cv2.imshow("img.jpg", annotaded_frame)  

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()