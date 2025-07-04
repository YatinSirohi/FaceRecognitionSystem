from tkinter import *
from student import Student
from train import Train
from face_recognition import FaceRecognition
from attendance import Attendance
import os

class face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1270x700+0+0")
        self.root.resizable(False, False)  # Disable maximize (and resizing)

        # Title
        title_lbl = Label(self.root, text="FACE RECOGNITION ATTENDANCE SYSTEM", 
                          font=("times new roman", 35, "bold"), bg="black", fg="white")
        title_lbl.pack(side=TOP, fill=X)

        # Background color
        background_color = "#FFFFFF"
        self.root.configure(bg=background_color)

        # student button
        b1 = Button(self.root, text="Student Details", command=self.student_details, cursor="hand2",
                   font=("times new roman", 20, "bold"), bg="blue", fg="white")
        b1.place(x=50, y=100, width=200, height=50)

        b2 = Button(self.root, text="Attendance", command=self.attendance,  cursor="hand2", 
                   font=("times new roman", 20, "bold"), bg="blue", fg="white")
        b2.place(x=300, y=100, width=200, height=50)

        b3 = Button(self.root, text="Train Model", command=self.train_model, cursor="hand2",
                   font=("times new roman", 20, "bold"), bg="blue", fg="white")
        b3.place(x=550, y=100, width=200, height=50)

        b4 = Button(self.root, text="Photos", command=self.photos,  cursor="hand2",
                   font=("times new roman", 20, "bold"), bg="blue", fg="white")
        b4.place(x=800, y=100, width=200, height=50)

        b5 = Button(self.root, command=self.face_detector, text="Face Detector", cursor="hand2",
                   font=("times new roman", 20, "bold"), bg="blue", fg="white")
        b5  .place(x=50, y=200, width=200, height=50)

        b5 = Button(self.root, text="Exit", command=self.exit,  cursor="hand2",
                   font=("times new roman", 20, "bold"), bg="blue", fg="white")
        b5  .place(x=300, y=200, width=200, height=50)

    # Function to open student details window
    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def attendance(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def train_model(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def photos(self):
        os.startfile("data")

    def face_detector(self):
        self.new_window = Toplevel(self.root)
        self.app = FaceRecognition(self.new_window)

    def exit(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = face_Recognition_System(root)
    root.mainloop()

