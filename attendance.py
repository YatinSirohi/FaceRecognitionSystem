from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import csv
from tkinter import filedialog
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")
MONGO_URI = os.getenv("MONGO_URI")

mydata = []
class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.title("Take Attendance")
        self.root.geometry("1270x700+0+0")
        self.root.resizable(False, False)  # Disable maximize (and resizing)

        #c============================== variables ==========================
        self.student_id = StringVar()
        self.attendance_date = StringVar()
        self.attendance_status = StringVar()

        # Title
        title_lbl = Label(self.root, text="ATTENDANCE SYSTEM", 
                          font=("times new roman", 35, "bold"), bg="black", fg="white")
        title_lbl.pack(side=TOP, fill=X)

        # Left Side Frame
        self.left_frame = LabelFrame(self.root, text="STUDENT ATTENDANCE DETAILS",
                                     font=("times new roman", 15, "bold"), bg="#FFFFFF")   
        self.left_frame.place(x=5, y=65, width=650, height=600) 

        # label and entry
        self.lbl_student_id = Label(self.left_frame, text="Student ID:", font=("times new roman", 15, "bold"), bg="#FFFFFF")
        self.lbl_student_id.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.entry_student_id = Entry(self.left_frame, font=("times new roman", 15), bg="#FFFFFF", textvariable=self.student_id, state='readonly')
        self.entry_student_id.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        self.lbl_attendance_date = Label(self.left_frame, text="Attendance Date:", font=("times new roman", 15, "bold"), bg="#FFFFFF")
        self.lbl_attendance_date.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.entry_attendance_date = Entry(self.left_frame, font=("times new roman", 15), bg="#FFFFFF", textvariable=self.attendance_date)
        self.entry_attendance_date.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        self.lbl_attendance_status = Label(self.left_frame, text="Attendance Status:", font=("times new roman", 15, "bold"), bg="#FFFFFF")
        self.lbl_attendance_status.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.entry_attendance_status = ttk.Combobox(self.left_frame, textvariable=self.attendance_status, font=("times new roman", 15), state='readonly', width=17)
        self.entry_attendance_status['values'] = ("Present", "Absent")
        self.entry_attendance_status.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        # Buttons
        self.button_frame = Frame(self.left_frame, bg="#FFFFFF", relief=RIDGE, bd=2)
        self.button_frame.place(x=0, y=220, height=80, width=630)

        self.save_button = Button(self.button_frame, command=self.import_csv, cursor="hand2", text="Import CSV", font=("times new roman", 12, "bold"), bg="#4CAF50", fg="white", width=10)
        self.save_button.grid(row=0, column=0, padx=10, pady=20)

        self.update_button = Button(self.button_frame, command=self.export_csv, cursor="hand2", text="Export CSV", font=("times new roman", 12, "bold"), bg="#2196F3", fg="white", width=10)
        self.update_button.grid(row=0, column=1, padx=10, pady=5)

        self.reset_button = Button(self.button_frame, command=self.reset, cursor="hand2", text="Reset", font=("times new roman", 12, "bold"), bg="#a7c71b", fg="white", width=10)
        self.reset_button.grid(row=0, column=2, padx=10, pady=5)

        self.update_button = Button(self.button_frame, command=self.update, cursor="hand2", text="Update", font=("times new roman", 12, "bold"), bg="#f44336", fg="white", width=10)
        self.update_button.grid(row=0, column=3, padx=10, pady=5)


        # Right side frame
        self.right_frame = LabelFrame(self.root, text="ATTENDANCE DETAILS",
                                      font=("times new roman", 15, "bold"), bg="#FFFFFF")   
        self.right_frame.place(x=670, y=65, width=595, height=600)

        self.table_frame = Frame(self.right_frame, bg="#FFFFFF", bd=2, relief=RIDGE)
        self.table_frame.place(x=5, y=10, width=580, height=550)
        self.scroll_x = Scrollbar(self.table_frame, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.table_frame, orient=VERTICAL)
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.AttendanceReportTable = ttk.Treeview(self.table_frame, columns=(
            "studentID", "date", "attendance",
        ), xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set, show="headings")
        self.scroll_x.config(command=self.AttendanceReportTable.xview)
        self.scroll_y.config(command=self.AttendanceReportTable.yview)
        
        self.AttendanceReportTable.heading("studentID", text="Student ID")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("attendance", text="Attendance")
        #Set table heading widths
        self.AttendanceReportTable.column("studentID", width=80)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)
        self.AttendanceReportTable['show'] = 'headings'
        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease-1>", self.get_cursor)

    # ========================== Functions =========================
    def fetch_data(self, rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("", END, values=i)

    # import CSV function
    def import_csv(self):
        global mydata
        mydata.clear()  # Clear existing data
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")), parent=self.root)
        if file_path:
            with open(file_path) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for i in reader:
                    mydata.append(i)
                self.fetch_data(mydata)
            messagebox.showinfo("Success", "Data imported successfully", parent=self.root)
        else:
            messagebox.showerror("Error", "No file selected", parent=self.root)

    # export CSV function
    def export_csv(self):
        try:
            if len(mydata) < 1:
                messagebox.showerror("Error", "No data to export", parent=self.root)
                return
            file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), defaultextension=".csv", initialfile="Exported_attendance.csv", title="CSV File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")), parent=self.root)
            if file_path:
                with open(file_path, mode='w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for row in mydata:
                        writer.writerow(row)
                messagebox.showinfo("Success", f"Data exported successfully to {file_path}", parent=self.root)
            else:
                messagebox.showerror("Error", "No file selected", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)

    def get_cursor(self, event):
        cursor_row = self.AttendanceReportTable.focus()
        content = self.AttendanceReportTable.item(cursor_row)
        row = content['values']
        if row:
            self.student_id.set(row[0])
            self.attendance_date.set(row[1])
            self.attendance_status.set(row[2])

    def reset(self):
        self.student_id.set("")
        self.attendance_date.set("")
        self.attendance_status.set("")

        # Clear the table
        # self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        # mydata.clear()

    def update(self):
        if self.student_id.get() == "" or self.attendance_date.get() == "" or self.attendance_status.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            for index, row in enumerate(mydata):
                if len(row) >= 3 and row[0] == self.student_id.get():
                    mydata[index] = (self.student_id.get(), self.attendance_date.get(), self.attendance_status.get())
                    break
            self.fetch_data(mydata)
            self.reset()

if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()