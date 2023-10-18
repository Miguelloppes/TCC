from ultralytics import YOLO
import cv2
import numpy
import CL

# start webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
img = cv2.imread("4.jpg")
length = 1 
width = 1
# model
model = YOLO("yolo-weights/best.pt")

# object classes
classNames = ["box_top"]



# while True:
length_previous = length
width_previous = width
#success, img = cap.read()
#print(success)
H, W, _ = img.shape
results = model(img)
annotaded_frame = results[0].plot()
#print(results[0].masks)
for result in results:
    for j, mask in enumerate(result.masks.data):

        mask = (mask.numpy() * 255).astype("uint8")

        mask = cv2.resize(mask, (W, H))
length,width = CL.camera_find_points(mask,7.5,1000) #Calculo do comprimento e largura 
if (length == 0 and width == 0):#Caso haja algum erro de identificação a caixa vai utilizar das medidas anteriores 
    CL.display(annotaded_frame,7.5,length_previous,width_previous)
else:
    CL.display(annotaded_frame,7.5,length,width)
cv2.imwrite("img.jpg", annotaded_frame)  
#cv2.imwrite("mask", mask)
    # if cv2.waitKey(1) == ord('q'):
    #     break

# cap.release()
cv2.destroyAllWindows()