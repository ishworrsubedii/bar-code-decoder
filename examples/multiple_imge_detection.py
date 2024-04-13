"""
Created By: ishwor subedi
Date: 2024-04-12
"""

import os

import cv2

from src.services.barcode_decode.barcode_decode import BarcodeDecoder
from src.services.barcode_detection.barcode_detection import BarcodeDetection

if __name__ == '__main__':

    model_path = "resources/model/best.pt"
    barcode_detection = BarcodeDetection(model_path)
    decoder_instance = BarcodeDecoder()

    image_dir = "resources/dataset/test/images"
    images = os.listdir(image_dir)
    for image in images:
        image_path = os.path.join(image_dir, image)
        image = cv2.imread(image_path)
        image = cv2.resize(image, (1280, 720))
        results = barcode_detection.image_detect(image, display=False, confidence_threshold=0.25, nms_threshold=0.45)
        for prediction in results:
            bboxes = prediction.boxes.xyxy
        try:
            bbox = bboxes[0].int().tolist()
            x1, y1, x2, y2 = bbox
            cropped = prediction.orig_img[y1:y2, x1:x2]
            decoded_data = decoder_instance.image_decode(cropped)
            for data in decoded_data:
                print("Decoded barcode:", data)
                with open('resources/decoded_barcodes.txt', 'a') as f:
                    f.write(f'{image_path}\t{data}\n')
                cv2.putText(prediction.orig_img, f'{data}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255),
                            2)
                cv2.rectangle(prediction.orig_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.imshow('Barcode Decoder', prediction.orig_img)
                cv2.waitKey(200)


        except Exception as e:
            print(e)
