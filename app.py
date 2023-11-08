import cv2
from pyzbar.pyzbar import decode

# create a video capture object
cap = cv2.VideoCapture(0)

while True:
    # read the frame from the camera
    ret, frame = cap.read()

    # find the qr code in the frame
    decoded_data = decode(frame)

    # print the decoded data
    if decoded_data:
        for decoded in decoded_data:
            print(f"Decoded data: {decoded.data.decode('utf-8')}")
            print(f"Type: {decoded.type}")

    # display the frame
    cv2.imshow('frame', frame)

    # stop the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the video capture object
cap.release()

# close all the windows
cv2.destroyAllWindows()