import cv2
import numpy as np
import mediapipe as mp


# Load Yolo
# Download weight file(yolov3_training_2000.weights) from this link :- https://drive.google.com/file/d/10uJEsUpQI3EmD98iwrwzbD4e19Ps-LHZ/view?usp=sharing
net = cv2.dnn.readNet("yolov4-obj_best.weights", "yolov4-obj.cfg")
classes = ["Weapon"]
# with open("coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

handsAI = mp.solutions.hands.Hands(static_image_mode=False,
                                                    max_num_hands=1,
                                                    min_tracking_confidence=0.5,
                                                    min_detection_confidence=0.5)

# Loading image
# img = cv2.imread("room_ser.jpg")
# img = cv2.resize(img, None, fx=0.4, fy=0.4)

# Enter file name for example "ak47.mp4" or press "Enter" to start webcam
#def value():
#    val = input("Enter file name or press enter to start webcam : \n")
#    if val == "":
#        val = 0
#    return val


# for video capture
cap = cv2.VideoCapture(0)



thres = 0.5 # Threshold to detect object
nms_threshold = 0.2 #(0.1 to 1) 1 means no suppress , 0.1 means high suppress 
#cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,280) #width 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,120) #height 
cap.set(cv2.CAP_PROP_BRIGHTNESS,150) #brightness 

classNames = []
with open('coco.names','r') as f:
    classNames = f.read().splitlines()

font = cv2.FONT_HERSHEY_PLAIN
#font = cv2.FONT_HERSHEY_COMPLEX
Colors = np.random.uniform(0, 255, size=(len(classNames), 3))

weightsPath = "frozen_inference_graph.pb"
configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
net2 = cv2.dnn_DetectionModel(weightsPath,configPath)
net2.setInputSize(320,320)
net2.setInputScale(1.0/ 127.5)
net2.setInputMean((127.5, 127.5, 127.5))
net2.setInputSwapRB(True)





# val = cv2.VideoCapture()
while True:
    _, img = cap.read()
    height, width, channels = img.shape
    # width = 512
    # height = 512

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net2.forward(output_layers)
    hand = handsAI.process(img)
    

    # Showing information on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.6:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    if indexes == 0: print("weapon detected in frame")



    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
    results = handsAI.process(img)
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    mp_drawing = mp.solutions.drawing_utils
    annotated_image = img.copy()
    mp_drawing_styles = mp.solutions.drawing_styles

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
            img,
            hand_landmarks,
            mp.solutions.hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
            #_update_info_direction_fingers(hand.multi_hand_landmarks[0].landmark[9], hand.multi_hand_landmarks[0].landmark[5])
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # frame = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    cv2.imshow("Image", img)
    #key = cv2.waitKey(1)
    #if key == 27:
    #    break




    success,img = cap.read()
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1,-1)[0])
    confs = list(map(float,confs))
    #print(type(confs[0]))
    #print(confs)

    indices = cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)
    if len(classIds) != 0:
        for i in indices:
            #i = i[0]
            box = bbox[i]
            confidence = str(round(confs[i],2))
            #color = Colors[classIds[i][0]-1]
            x,y,w,h = box[0],box[1],box[2],box[3]
            cv2.rectangle(img, (x,y), (x+w,y+h), color=(0,255,0), thickness=2)
            cv2.putText(img, classNames[classIds[i]-1]+" "+confidence,(x+10,y+20),
                        font,1,(0,255,0),2)



cap.release()
cv2.destroyAllWindows()
