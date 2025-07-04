from datetime import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
from matplotlib.pyplot import clf
import numpy as np
from train import Train
from pymongo import MongoClient
from dotenv import load_dotenv
import pickle

load_dotenv(dotenv_path=".env.local")
MONGO_URI = os.getenv("MONGO_URI")

class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition")
        self.root.geometry("1270x700+0+0")
        self.root.resizable(False, False)  # Disable maximize (and resizing)

        # Title
        title_lbl = Label(self.root, text="FACE RECOGNITION", 
                          font=("times new roman", 35, "bold"), bg="black", fg="white")
        title_lbl.pack(side=TOP, fill=X)

        img_top = Image.open("images/face_detection.png")
        img_top = img_top.resize((600, 700), Image.LANCZOS)
        self.img_top = ImageTk.PhotoImage(img_top)
        img_lbl = Label(self.root, image=self.img_top)
        img_lbl.place(x=0, y=60, width=600, height=650)

        #buttons
        b1 = Button(self.root, text="Detect Face and mark attendance", command=self.face_recognition, cursor="hand2",
                    font=("times new roman", 20, "bold"), bg="blue", fg="white")
        b1.place(x=750, y=300, width=400, height=40)

        
    # ================ attendance ================
    def mark_attendance(self, id):
        with open("attendance.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            id_list = [line.split(",")[0] for line in myDataList]
            if str(id) not in id_list:
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                f.writelines(f"\n{id},{dt_string},Present")

    def face_recognition(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf, id_map, collection):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
            coord = []
            reverse_id_map = {v: k for k, v in id_map.items()}
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                if confidence > 77:
                    str_id = reverse_id_map.get(id)
                    student = collection.find_one({"studentID": str_id})
                    if student:
                        name = student.get("studentName", "Unknown")
                        cv2.putText(img, f"ID: {str_id}", (x, y - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                        cv2.putText(img, f"Name: {name}", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                        cv2.putText(img, f"Accuracy: {confidence}%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                        self.mark_attendance(str_id)
                    else:
                        cv2.putText(img, "Unknown face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                else:
                    cv2.putText(img, "Unknown face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            return coord

        def recognize(img, clf, faceFascade, id_map, collection):
            coord = draw_boundary(img, faceFascade, 1.1, 10, (255, 0, 0), "Face", clf, id_map, collection)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        # Load id_map and connect to MongoDB ONCE
        with open("id_map.pkl", "rb") as f:
            id_map = pickle.load(f)
        client = MongoClient(MONGO_URI)
        db = client["student_db"]
        collection = db["students"]

        video_capture = cv2.VideoCapture(0)
        while True:
            ret, img = video_capture.read()
            img = recognize(img, clf, faceCascade, id_map, collection)
            cv2.imshow("Face Recognition", img)
            key = cv2.waitKey(1)
            if key == 13 or key == 27 or cv2.getWindowProperty("Face Recognition", cv2.WND_PROP_VISIBLE) < 1:
                break

        video_capture.release()
        cv2.destroyAllWindows()
        client.close()
        messagebox.showinfo("Success", "Attendance updated successfully")

if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognition(root)
    root.mainloop()