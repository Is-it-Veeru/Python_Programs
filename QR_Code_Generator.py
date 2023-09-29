import qrcode
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog

class QRCodeGenerator:
    def __init__(self, app):
        self.app = app

    def generate_qr_code(self, data):
        try:
            if data:
                qr = qrcode.QRCode(
                    version=4,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4
                )

                qr.add_data(data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                img = img.resize(self.app.QR_CODE_SIZE)

                qr_image = ImageTk.PhotoImage(image=img)
                self.app.qr_label.config(image=qr_image)
                self.app.qr_label.image = qr_image

                self.app.save_button.place(x=148, y=90)

        except Exception as e:
            if hasattr(self.app.qr_label, "image"):
                self.app.qr_label.image = None
                self.app.qr_label.destroy()
            self.app.error_label.config(text="Invalid Data", bg="red", font=("Arial", 14))
            self.app.error_label.place(x=120, y=280)
            self.app.reactivate_qr_label()

    def save_qr_code(self):
        try:
            if hasattr(self.app.qr_label, "image"):
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])

                if file_path:
                    qr_image = self.app.qr_label.image
                    img = Image.open(qr_image)

                    img = img.resize(self.app.QR_CODE_SIZE)
                    img.save(file_path)
        except Exception as e:
            self.app.error_label.config(text=str(e), bg="red", font=("Arial", 12))
            self.app.error_label.place(x=120, y=280)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("400x400")
        self.root.config(bg="green")
        self.root.resizable(False, False)

        self.QR_CODE_SIZE = (200, 200)

        self.entry = Entry(root, font=("Arial", 12))
        self.entry.place(x=100, y=30)

        self.generate_button = Button(root, text="Generate QR Code", fg="black", bg="gold", font=("Arial", 8),
                                      command=self.generate)
        self.generate_button.place(x=139, y=60)

        self.save_button = Button(root, text="Save QR Code", fg="black", bg="brown", font=("Arial", 8),
                                  command=self.save_qr_code)

        # Create a label to display the QR code
        self.qr_label = Label(root, bg="green")
        self.qr_label.place(x=80, y=120)

        # Create a label to display the error   
        self.error_label = Label(root)

    def generate(self):
        data = self.entry.get()
        qr_generator = QRCodeGenerator(self)
        qr_generator.generate_qr_code(data)

    def save_qr_code(self):
        qr_generator = QRCodeGenerator(self)
        qr_generator.save_qr_code()

    def reactivate_qr_label(self):
        self.qr_label = Label(root, bg="green")
        self.qr_label.place(x=80, y=120)


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()
