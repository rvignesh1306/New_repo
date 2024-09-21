import cv2

# Load the pre-trained MobileNet SSD model
model_weights = '/Users/janaki/Desktop/MobileNetSSD_deploy.caffemodel'
model_cfg = '/Users/janaki/Desktop/MobileNetSSD_deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(model_cfg, model_weights)

# Set the desired confidence threshold
confidence_threshold = 0.5

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

# Define the output video codec and frame rate
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 7.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare the frame for object detection by resizing and normalizing
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # Set the input to the network and perform a forward pass
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections by confidence threshold
        if confidence > confidence_threshold:
            class_id = int(detections[0, 0, i, 1])

            # Get the bounding box coordinates
            box = detections[0, 0, i, 3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the bounding box and label on the frame
            label = f"Object: {confidence:.2f}"
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the frame with detected objects into the output video
    out.write(frame)

# Release the video capture and output video
cap.release()
out.release()
