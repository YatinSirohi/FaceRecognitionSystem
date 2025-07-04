from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.title("Train Data")
        self.root.geometry("1270x700+0+0")

        # Title
        title_lbl = Label(self.root, text="TRAIN DATA SET", 
                          font=("times new roman", 35, "bold"), bg="black", fg="white")
        title_lbl.pack(side=TOP, fill=X)

        label_for_button = Label(self.root, text="Click below button to train the data set", 
                            font=("times new roman", 12, "bold"), bg="#FFFFFF")
        label_for_button.place(x=10, y=100, width=1250, height=50)

        # Btton
        self.save_button = Button(self.root, command=self.train_model, cursor="hand2", text="TRAIN DATA SET", font=("times new roman", 18, "bold"), bg="#3001FF", fg="white")
        self.save_button.place(x=10, y=150, width=1250, height=50)
 
    def train_model(self):
        data_dir = "data"
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data directory does not exist.", parent=self.root)
            return
        if not os.listdir(data_dir):
            messagebox.showerror("Error", "Data directory is empty.", parent=self.root)
            return
        path = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.jpg') or f.endswith('.png')]
        
        id_map = {}
        current_id = 0
        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')
            img_np = np.array(img, 'uint8')
            filename = os.path.basename(image)
            parts = filename.split('.')
            if len(parts) > 2:
                str_id = parts[1]
                if str_id not in id_map:
                    id_map[str_id] = current_id
                    current_id += 1
                faces.append(img_np)
                ids.append(id_map[str_id])
                cv2.imshow("Training", img_np)
                cv2.waitKey(1)
            else:
                continue
        ids = np.array(ids)
        if len(faces) == 0 or len(ids) == 0:
            messagebox.showerror("Error", "No valid training data found.", parent=self.root)
            return

        # Save id_map for use in recognition
        import pickle
        with open("id_map.pkl", "wb") as f:
            pickle.dump(id_map, f)

        # Train the model
        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(faces, ids)
        model.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", "Model trained successfully.", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()