"""
Created By: ishwor subedi
Date: 2024-04-13
"""
from numpy import ndarray
import cv2
from pyzbar.pyzbar import decode


class BarcodeDecoder:

    def image_decode(self, image: ndarray):
        # Convert image to grayscale
        # gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Detect barcodes in the image
        barcodes = decode(image)

        decoded_data = []
        # Loop over detected barcodes
        for barcode in barcodes:
            # Extract barcode data
            barcode_data = barcode.data.decode("utf-8")
            decoded_data.append(barcode_data)

        return decoded_data


if __name__ == "__main__":

    image_path = "/home/ishwor/Pictures/Screenshots/Screenshot from 2024-04-13 14-18-03.png"
    image = cv2.imread(image_path)

    decoder = BarcodeDecoder()
    decoded_data = decoder.image_decode(image)

    for data in decoded_data:
        print("Decoded barcode:", data)
