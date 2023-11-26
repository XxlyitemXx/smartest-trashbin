from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
from discord import SyncWebhook
import serial

port = 'CMSIS-DAP'
baudrate = 9800
ser = serial.Serial(port, baudrate)
def microbitstersenter(data):
    message = "data"
    encoded_message = message.encode('utf-8')
    ser.write(encoded_message)
WEBHOOK_URL = "https://discord.com/api/webhooks/1172538727185252414/Si8JY0Ki9JSuyCMQBYrNSWAeHqu3uwkY-aGnYaB48R7uDIdH3cHhaPePM-xRycSXyNpD"
hook = SyncWebhook.from_url(WEBHOOK_URL)
recycle = 0
biowaste = 0
dangerous = 0

currentname = "unknown"
encodingsP = "encodings.pickle"
cascade = "haarcascade_frontalface_default.xml"
print("[INFO] loading encodings + object detector by github.com/XxlyitemXx...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)
print("[INFO] starting object detection system...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)

    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

            if currentname != name:
                currentname = name
                print(currentname)
            names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (255, 0, 0), 2)

        if name == "recycle":
            microbitstersenter("recycle")
            print("recycle")
            recycle += 1
            hook.send("recycle : " + str(recycle))
        elif name == "biowaste":
            microbitstersenter("biowaste")
            print("biowaste")
            biowaste += 1
            hook.send("biowaste : " + str(biowaste))
        elif name == "dangerous":
            microbitstersenter("dangerous")
            print("dangerous")
            dangerous += 1
            hook.send("dangerous : " + str(dangerous))
        elif name == "back":
            microbitstersenter("back")
            print("back")

    cv2.imshow("object detector...", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
