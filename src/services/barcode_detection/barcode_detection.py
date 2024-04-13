"""
Created By: ishwor subedi
Date: 2024-04-13
"""
import os

import cv2
import numpy as np
from numpy import ndarray
from ultralytics import YOLO
from src.services.barcode_decode.barcode_decode import BarcodeDecoder


class BarcodeDetection:
    def __init__(self, model_path: str):
        self.model_instance = YOLO(model_path)

    def image_detect(self, image, confidence_threshold: float, nms_threshold: float, display: bool):

        results = self.model_instance.predict(image, conf=confidence_threshold, iou=nms_threshold, show=display)
        return results

    def video_detection(self, video_path: str, display: bool, confidence_threshold: float, nms_threshold: float):
        cap = cv2.VideoCapture(video_path)
        detections = []
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame")
                break
            frame = cv2.resize(frame, (640, 480))
            results = self.model_instance(frame, conf=confidence_threshold, iou=nms_threshold)
            for prediction in results:
                bboxes = prediction.boxes.xyxy
                try:
                    bbox = bboxes[0].int().tolist()
                    x1, y1, x2, y2 = bbox
                    cropped = frame[y1:y2, x1:x2]
                    detections.append((prediction, cropped))

                    if display:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(frame, f'Detected', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (0, 0, 255), 2)
                except Exception as e:
                    print(e)
            if display:
                cv2.imshow('frame', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    break
        cap.release()
        return detections
