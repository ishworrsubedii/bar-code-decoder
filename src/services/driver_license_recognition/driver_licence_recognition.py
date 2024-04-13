"""
Created By: ishwor subedi
Date: 2024-04-13
"""
import os

import cv2

from paddleocr import PaddleOCR, draw_ocr
from PIL import Image


class EmbossedNumberPlate:
    def __init__(self, det_model, recognition_model, cls_model_dir, char_dict):
        """
        Initialize the paddleocr model

        """

        self.ocr = PaddleOCR(det_model_dir=det_model, cls_model_dir=cls_model_dir,
                             rec_model_dir=recognition_model, lang="en",

                             use_gpu=True)

    def detection_recognition_cls(self, img):
        """
         recognize the text from the image
        :param img:  image path
        :return:  boxes, txts, scores
        """
        try:
            result = self.ocr.ocr(img, cls=False)
            print(result)

            for idx in range(len(result)):

                if result[idx] is None:
                    return [], [], []
                else:

                    result = result[0]
                    boxes = [line[0] for line in result]
                    txts = [line[1][0] for line in result]
                    scores = [line[1][1] for line in result]
                    return boxes, txts, scores

        except Exception as e:
            print(f"An error occurred: {e}")
            return [], [], []


if __name__ == '__main__':
    det_model = 'resources/model/det/'
    recognition_model = 'resources/model/rec/'
    cls_model_dir = 'resources/model/cls'
    char_dict = 'resources/model/en_dict.txt'
    font_path = "resources/model/arial.ttf"
    output_path = "resources/output_images"
    image_dir = "resources/license_dataset"
    images = os.listdir(image_dir)

    paddle_ocr = EmbossedNumberPlate(det_model=det_model, recognition_model=recognition_model,
                                     cls_model_dir=cls_model_dir, char_dict=char_dict
                                     )
    for image_path in images:
        img_path = os.path.join(image_dir, image_path)
        boxes, txts, scores = paddle_ocr.detection_recognition_cls(
            img=img_path)
        img = Image.open(img_path)

        img = draw_ocr(img, boxes, txts, scores, font_path=font_path)
        img = Image.fromarray(img)
        new_output_image = os.path.basename(img_path)
        new_output_image = os.path.join(output_path, new_output_image)
        img.save(new_output_image)
