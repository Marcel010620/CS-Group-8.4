import qrcode
from PIL import Image

class QRCodeGenerator:
    def __init__(self, data_list):
        self.data_list = data_list

    def generate_qrcodes(self):
        for index, data in enumerate(self.data_list, start=1):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f"qrcode_{index}.png")

if __name__ == "__main__":
    # Example: 20 data strings for QR codes
    data_strings = ["Data1", "Data2", "Data3", "Data4", "Data5",
                    "Data6", "Data7", "Data8", "Data9", "Data10",
                    "Data11", "Data12", "Data13", "Data14", "Data15",
                    "Data16", "Data17", "Data18", "Data19", "Data20"]

    # Create an instance of QRCodeGenerator
    qr_generator = QRCodeGenerator(data_strings)

    # Generate QR codes
    qr_generator.generate_qrcodes()
