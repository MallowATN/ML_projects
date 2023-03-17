import cv2
import numpy as np

# Load YOLOv3 model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Input image
img = cv2.imread("image.jpg")

# Get dimensions of the input image
height, width, channels = img.shape

# Create a 4D blob from the input image
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 16), (0, 0, 0), True, crop=False)

# Set the input to the model
net.setInput(blob)

# Run forward pass through the model
output_layers = net.forward(["yolo_82", "yolo_94", "yolo_106"])

# Initialize lists to store the bounding boxes and confidences
bboxes = []
confidences = []

# Loop through the output layers
for output in output_layers:
    # Loop through the detections
    for detection in output:
        # Get the class probabilities
        scores = detection[5:]
        # Get the class with the highest probability
        class_id = np.argmax(scores)
        # Get the confidence of the detection
        confidence = scores[class_id]
        # Only consider detections with a high confidence
        if confidence > 0.5:
            # Get the bounding box coordinates
            x, y, w, h = detection[0:4] * np.array([width, height, width, height])
            # Append to the lists
            bboxes.append([x, y, w, h])
            confidences.append(float(confidence))

# Non-maximum suppression
indices = cv2.dnn.NMSBoxes(bboxes, confidences, 0.5, 0.4)

# Draw the bounding boxes on the input image
for i in indices:
    i = i[0]
    x, y, w, h = bboxes[i]
    cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 2)

# Show the output image
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
