from qrcode import QRCode

# Create a QR code object
qr_code = QRCode()

# Add data to the QR code
qr_code.add_data("Hello, world!")

# Generate the QR code
qr_code.make()