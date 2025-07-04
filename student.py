from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import cv2


load_dotenv(dotenv_path=".env.local")
MONGO_URI = os.getenv("MONGO_URI")

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1270x700+0+0")
        self.root.resizable(False, False)  # Disable maximize (and resizing)

        # ========== Variables declaration ==============
        self.studentID = StringVar()
        self.studentName = StringVar()
        self.studentEmail = StringVar()
        self.studentPhone = StringVar()
        self.gender = StringVar()  
        self.unit = StringVar()
        self.term = StringVar()
        self.course = StringVar()  
    
        # Title
        title_lbl = Label(self.root, text="MANAGE STUDENT DETAILS", 
                          font=("times new roman", 35, "bold"), bg="black", fg="white")
        title_lbl.pack(side=TOP, fill=X)

        # Background color
        background_color = "#FFFFFF"
        self.root.configure(bg=background_color)

        # Custom style for ttk.Entry
        style = ttk.Style()
        style.configure("Custom.TEntry",
                        foreground="#333333",
                        fieldbackground="#F0F0F0",
                        bordercolor="#4A90E2",
                        borderwidth=2,
                        relief="flat")

        # left side frame
        self.left_frame = LabelFrame(self.root, text="ADD/UPDATE STUDENT DETAILS",
                                     font=("times new roman", 15, "bold"), bg="#FFFFFF")   
        self.left_frame.place(x=5, y=65, width=650, height=550) 

        # Current Course inside left frame
        self.current_course_frame = LabelFrame(self.left_frame, text="Current Course Details",
                                     font=("times new roman", 12, "bold"), bg="#FFFFFF")   
        self.current_course_frame.place(x=5, y=15, width=635, height=120, bordermode="inside")

        unit_label = Label(self.current_course_frame, text="Unit", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF")
        unit_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        unit_combo = ttk.Combobox(self.current_course_frame, textvariable=self.unit, font=("times new roman", 12, "bold"), state="readonly")
        unit_combo["values"] = ("Select Unit", "ICT Foundation", "Promote cybersecurity",
                                 "Match ICT needs", "IP/Ethics/Privacy")
        unit_combo.current(0)
        unit_combo.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        term_label = Label(self.current_course_frame, text="Term", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF")
        term_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        term_combo = ttk.Combobox(self.current_course_frame, textvariable=self.term, font=("times new roman", 12, "bold"), state="readonly")
        term_combo["values"] = ("Select Term", "Term 1", "Term 2", "Term 3", "Term 4", "Term 5")
        term_combo.current(0)
        term_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        Course_label = Label(self.current_course_frame, text="Course", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF")
        Course_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        Course_combo = ttk.Combobox(self.current_course_frame, textvariable=self.course, font=("times new roman", 12, "bold"), state="readonly")
        Course_combo["values"] = ("Select Course", "Diploma of IT", "Advanced Diploma of IT", "Diploma of Civil", "Advanced Diploma of Civil", "Project management")
        Course_combo.current(0)
        Course_combo.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Class student details inside left frame
        self.class_student_frame = LabelFrame(self.left_frame, text="Class Student Information",
                                     font=("times new roman", 12, "bold"), bg="#FFFFFF")   
        self.class_student_frame.place(x=5, y=150, width=635, height=370, bordermode="inside")

        self.studentID_label = Label(self.class_student_frame, text="Student ID", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF")  
        self.studentID_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)   

        self.studentID_entry = ttk.Entry(self.class_student_frame, textvariable=self.studentID, font=("times new roman", 12, "bold"), width=50, style="Custom.TEntry")
        self.studentID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        self.studentName_label = Label(self.class_student_frame, text="Student Name", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF")  
        self.studentName_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)   

        self.studentName_entry = ttk.Entry(self.class_student_frame, textvariable=self.studentName, font=("times new roman", 12, "bold"), width=50, style="Custom.TEntry")
        self.studentName_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        self.studentEmail_label = Label(self.class_student_frame, text="Student Email", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF") 
        self.studentEmail_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        self.studentEmail_entry = ttk.Entry(self.class_student_frame, textvariable=self.studentEmail, font=("times new roman", 12, "bold"), width=50, style="Custom.TEntry")
        self.studentEmail_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        self.studentPhone_label = Label(self.class_student_frame, text="Student Phone", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF") 
        self.studentPhone_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        self.studentPhone_entry = ttk.Entry(self.class_student_frame, textvariable=self.studentPhone, font=("times new roman", 12, "bold"), width=50, style="Custom.TEntry")
        self.studentPhone_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        self.gender_label = Label(self.class_student_frame, text="Student Gender", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF") 
        self.gender_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        self.gender_combo = ttk.Combobox(self.class_student_frame, textvariable=self.gender, font=("times new roman", 12, "bold"), state="readonly")
        self.gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        self.gender_combo.current(0)
        self.gender_combo.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # # Radio buttons 
        # self.var_photo_taken = StringVar()
        # self.photo_taken_radio = ttk.Radiobutton(self.class_student_frame, variable=self.var_photo_taken, text="Take photo sample", value="Yes")
        # self.photo_taken_radio.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        # self.no_photo_radio = ttk.Radiobutton(self.class_student_frame, variable=self.var_photo_taken, text="No photo sample", value="No")
        # self.no_photo_radio.grid(row=5, column=1, padx=5, pady=5, sticky=W)

        # Buttons frame
        self.button_frame = Frame(self.class_student_frame, bg="#FFFFFF", relief=RIDGE, bd=2)
        self.button_frame.place(x=0, y=220, height=100, width=630)

        self.save_button = Button(self.button_frame, command=self.add_student, cursor="hand2", text="Save", font=("times new roman", 12, "bold"), bg="#4CAF50", fg="white", width=10)
        self.save_button.grid(row=0, column=0, padx=10, pady=5)

        self.update_button = Button(self.button_frame, command=self.update_student, cursor="hand2", text="Update", font=("times new roman", 12, "bold"), bg="#2196F3", fg="white", width=10)
        self.update_button.grid(row=0, column=1, padx=10, pady=5)

        self.reset_button = Button(self.button_frame, command=self.reset_fields, cursor="hand2", text="Reset", font=("times new roman", 12, "bold"), bg="#a7c71b", fg="white", width=10)
        self.reset_button.grid(row=0, column=2, padx=10, pady=5)

        self.delete_button = Button(self.button_frame, command=self.delete_student, cursor="hand2", text="Delete", font=("times new roman", 12, "bold"), bg="#f44336", fg="white", width=10)
        self.delete_button.grid(row=0, column=3, padx=10, pady=5)

        self.take_photo_button = Button(self.button_frame, command=self.generate_dataset, cursor="hand2", text="Take Photo Sample", font=("times new roman", 12, "bold"), bg="#0F6B8F", fg="white", width=25)
        self.take_photo_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.update_photo_button = Button(self.button_frame, command=self.generate_dataset, text="Update Photo Sample", cursor="hand2", font=("times new roman", 12, "bold"), bg="#0F6B8F", fg="white", width=25)
        self.update_photo_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="w")

        # Right side frame
        self.right_frame = LabelFrame(self.root, text="SEARCH STUDENT DETAILS",
                                      font=("times new roman", 15, "bold"), bg="#FFFFFF")   
        self.right_frame.place(x=670, y=65, width=595, height=550)

        # -------------- Search systemt in right side frame -------------------
        self.search_frame = LabelFrame(self.right_frame, text="Search System",
                                       font=("times new roman", 12, "bold"), bg="#FFFFFF")  
        self.search_frame.place(x=5, y=15, width=580, height=100)

        search_label = Label(self.search_frame, text="Search By",
                             font=("times new roman", 12, "bold"), bg="#627FDF")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.search_combo = ttk.Combobox(self.search_frame, font=("times new roman", 12, "bold"), state="readonly")
        self.search_combo["values"] = ("Select Option", "studentID", "studentName", "unit")
        self.search_combo.current(0)
        self.search_combo.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        self.search_entry = Entry(self.search_frame, font=("times new roman", 12, "bold"), bg="#FFFFFF")
        self.search_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        self.search_button = Button(self.search_frame, command=self.search_student, text="Search", font=("times new roman", 12, "bold"), bg="#4CAF50", fg="white")
        self.search_button.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        self.show_all_button = Button(self.search_frame, command=self.show_all_students, text="Show All", font=("times new roman", 12, "bold"), bg="#2196F3", fg="white")
        self.show_all_button.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Table frame for displaying student details
        self.table_frame = Frame(self.right_frame, bg="#FFFFFF", bd=2, relief=RIDGE)
        self.table_frame.place(x=5, y=125, width=580, height=390)
        self.scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.student_table = ttk.Treeview(self.table_frame, columns=(
            "studentID", "studentName", "studentEmail", "studentPhone",
            "unit", "term", "course", "gender"
        ), xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set, show="headings")
        self.scroll_x.config(command=self.student_table.xview)
        self.scroll_y.config(command=self.student_table.yview)
        
        self.student_table.heading("studentID", text="Student ID")
        self.student_table.heading("studentName", text="Student Name")
        self.student_table.heading("studentEmail", text="Student Email")
        self.student_table.heading("studentPhone", text="Student Phone")
        self.student_table.heading("unit", text="Unit")
        self.student_table.heading("term", text="Term")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("gender", text="Gender")
        #Set table heading widths
        self.student_table.column("studentID", width=80)
        self.student_table.column("studentName", width=150)
        self.student_table.column("studentEmail", width=200)
        self.student_table.column("studentPhone", width=100)
        self.student_table.column("unit", width=150)
        self.student_table.column("term", width=150)
        self.student_table.column("course", width=150)
        self.student_table.column("gender", width=80)
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)

        
        # ================== Buttons Functions declaration ==================
        
    def add_student(self):
        # Function to add student details
        # Function to add student details
        if (
            self.studentID.get() == "" 
            or self.studentName.get() == "" 
            or self.studentEmail.get() == "" 
            or self.studentPhone.get() == "" 
            or self.unit.get() == "" or self.term.get() == "" 
            or self.course.get() == ""
            or self.gender.get() == ""
        ):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                # Connect to MongoDB
                client = MongoClient(MONGO_URI)
                db = client["student_db"]
                collection = db["students"]

                # Check if studentID already exists
                existing_student = collection.find_one({"studentID": self.studentID.get()})
                if existing_student:
                    messagebox.showerror("Error", "Student ID already exists. Please enter correct ID.", parent=self.root)
                    client.close()
                    return

                # Prepare the student data
                student_data = {
                    "studentID": self.studentID.get(),
                    "studentName": self.studentName.get(),
                    "studentEmail": self.studentEmail.get(),
                    "studentPhone": self.studentPhone.get(),
                    "unit": self.unit.get(),
                    "term": self.term.get(),
                    "course": self.course.get(),
                    "gender": self.gender.get()
                }

                # Insert the data
                collection.insert_one(student_data)
                client.close()
                messagebox.showinfo("Success", "Student details added successfully", parent=self.root)
            except Exception as err:
                messagebox.showerror("Error", f"Failed to add student details: {err}", parent=self.root)

    def delete_student(self):
        # Function to delete student details
        if self.studentID.get() == "":
            messagebox.showerror("Error", "Please enter Student ID to delete", parent=self.root)
        else:
            try:
                # Connect to MongoDB
                client = MongoClient(MONGO_URI)
                db = client["student_db"]
                collection = db["students"]

                # Delete the student data
                result = collection.delete_one({"studentID": self.studentID.get()})
                client.close()
                
                if result.deleted_count > 0:
                    messagebox.showinfo("Success", "Student details deleted successfully", parent=self.root)
                else:
                    messagebox.showerror("Error", "Student ID not found", parent=self.root)
            except Exception as err:
                messagebox.showerror("Error", f"Failed to delete student details: {err}", parent=self.root)

    def get_cursor(self, event=""):
        # Function to get the selected row from the table
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        row = content["values"]
        
        # Set the values in the entry fields
        self.studentID.set(row[0])
        self.studentName.set(row[1])
        self.studentEmail.set(row[2])
        self.studentPhone.set(row[3])
        self.unit.set(row[4])
        self.term.set(row[5])
        self.course.set(row[6])
        self.gender.set(row[7])
        self.studentID_entry.focus()

    def update_student(self):
        # Function to update student details
        if (
            self.studentID.get() == "" 
            or self.studentName.get() == "" 
            or self.studentEmail.get() == "" 
            or self.studentPhone.get() == "" 
            or self.unit.get() == "" or self.term.get() == "" 
            or self.course.get() == ""
            or self.gender.get() == ""
        ):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                # Connect to MongoDB
                client = MongoClient(MONGO_URI)
                db = client["student_db"]
                collection = db["students"]

                # Update the student data
                updated_data = {
                    "studentName": self.studentName.get(),
                    "studentEmail": self.studentEmail.get(),
                    "studentPhone": self.studentPhone.get(),
                    "unit": self.unit.get(),
                    "term": self.term.get(),
                    "course": self.course.get(),
                    "gender": self.gender.get()
                }

                result = collection.update_one({"studentID": self.studentID.get()}, {"$set": updated_data})
                client.close()

                if result.modified_count > 0:
                    messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)
                else:
                    messagebox.showerror("Error", "Student ID not found", parent=self.root)
            except Exception as err:
                messagebox.showerror("Error", f"Failed to update student details: {err}", parent=self.root)

    def reset_fields(self):
        # Function to reset all fields
        self.studentID.set("")
        self.studentName.set("")
        self.studentEmail.set("")
        self.studentPhone.set("")
        self.unit.set("Select Unit")
        self.term.set("Select Term")
        self.course.set("Select Course")
        self.gender.set("Select Gender")
        self.var_photo_taken.set("")
        self.studentID_entry.focus()

    def show_all_students(self):
        # Function to show all students in the table
        try:
            # Connect to MongoDB
            client = MongoClient(MONGO_URI, ssl = True)
            db = client["student_db"]
            collection = db["students"]

            # Fetch all student data
            students = collection.find()
            self.student_table.delete(*self.student_table.get_children())
            for student in students:
                self.student_table.insert(
                    "", "end", values=(student["studentID"], student["studentName"], 
                                       student["studentEmail"], student["studentPhone"],
                                       student["unit"], student["term"], student["course"], student["gender"]))
            client.close()
        except Exception as err:
            messagebox.showerror("Error", f"Failed to fetch student details: {err}", parent=self.root)

    def search_student(self):
        # Function to search for a student by ID, Name, or Unit
        search_by = self.search_combo.get()
        search_value = self.search_entry.get()

        if search_by == "Select Option" or search_value == "":
            messagebox.showerror("Error", "Please select a valid search option and enter a value", parent=self.root)
            return

        try:
            # Connect to MongoDB
            client = MongoClient(MONGO_URI)
            db = client["student_db"]
            collection = db["students"]

            query = {search_by: search_value}
            student = collection.find_one(query)

            if student:
                self.student_table.delete(*self.student_table.get_children())
                self.student_table.insert("", "end", values=(student["studentID"], student["studentName"], student["studentEmail"], student["studentPhone"]))
            else:
                messagebox.showinfo("Info", "No student found with the given criteria", parent=self.root)
            client.close()
        except Exception as err:
            messagebox.showerror("Error", f"Failed to search for student: {err}", parent=self.root)


    # =============== Generate data set ot take photo sample =================
    def generate_dataset(self):
        if self.studentID.get() == "" or self.studentName.get() == "":
            messagebox.showerror("Error", "Please enter Student ID and Name to take photo sample", parent=self.root)
            return
        else:
            try:
        # ============= Load predidefined data on face frontal from opencv ====================
                face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  
                def face_cropped(img):
                    # Function to detect and crop the face from the image
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in faces:
                        cropped_face = img[y:y+h, x:x+w]
                        return cropped_face

                cap = cv2.VideoCapture(0)  # Initialize the camera
                img_id = 0  # Initialize image ID for saving
                student_id = self.studentID.get()  # Get the student ID for file naming
                while True:
                    ret, my_frame = cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id += 1

                        face = cv2.resize(face_cropped(my_frame), (450, 450))
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        file_name_path = "data/user." + str(student_id) + "." + str(img_id) + ".jpg"
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)   
                        cv2.imshow("Cropped Face", face)
                    if cv2.waitKey(1)==13 or int(img_id) == 100 :
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result", "Generating dataset completed successfully", parent=self.root)
            except Exception as err:
                messagebox.showerror("Error", f"Failed to generate dataset: {err}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
