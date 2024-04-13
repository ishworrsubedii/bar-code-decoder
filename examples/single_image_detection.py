"""
Created By: ishwor subedi
Date: 2024-04-13
"""
import cv2

from src.services.barcode_detection.barcode_detection import BarcodeDetection
from src.services.barcode_decode.barcode_decode import BarcodeDecoder

if __name__ == '__main__':
    model_path = "resources/model/best.pt"
    image_path = "resources/dataset/test/images/05102009082.jpg"

    barcode_detection = BarcodeDetection(model_path)
    barcode_decode = BarcodeDecoder()
    image = cv2.imread(image_path)

    results = barcode_detection.image_detect(image, display=False, confidence_threshold=0.25, nms_threshold=0.45)
    for prediction in results:
        bboxes = prediction.boxes.xyxy
        try:
            bbox = bboxes[0].int().tolist()
            x1, y1, x2, y2 = bbox
            cropped = image[y1:y2, x1:x2]
            decoded_data = barcode_decode.image_decode(cropped)
            cv2.putText(image, f'{decoded_data}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.imshow('frame', image)
            cv2.waitKey(0)

            print("Decoded barcode:", decoded_data)
        except Exception as e:
            print(e)
