import qrcode
from PIL import Image

class QRCodeGenerator:
    def __init__(self, data):
        self.data = data

    def generate_qr_code(self, filename, version=None, box_size=10, border=4):
        qr = qrcode.QRCode(version, box_size=box_size, border=border)
        qr.add_data(self.data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)

if __name__ == "__main__":
    qr_code_generator = QRCodeGenerator("https://www.google.com")
    qr_code_generator.generate_qr_code("google_qr_code.png")
