import cv2
import json
import os.path
import shutil


class SeperateImg:

    """
    ultralytics의 데이터 설정을 위해 훈련 이미지를 별도의 두 개의 폴더로 구성
    """

    def __init__(self, img_folder):
        self.img_folder = img_folder
        self.annotation_key = "annotations"
        self.img_id = "image_id"

    def save_img(self, json_path, save_path):
        data = json.load(open(json_path))
        # Retrieve data

        for i in range(len(data[self.annotation_key])):
            # Get required data
            image_id = f"{data[self.annotation_key][i][self.img_id]}"

            while len(image_id) != 4:
                image_id = "0" + image_id

            if self.img_folder == None:
                image_path = f"{image_id}.jpg"
            else:
                image_path = f"./{self.img_folder}/{image_id}.jpg"
            shutil.copyfile(image_path, save_path + f"{image_id}.jpg")


# To run in as a class
if __name__ == "__main__":
    sepimg = SeperateImg(img_folder="../../dataset/train")
    sepimg.save_img(
        json_path="../../dataset/validation_set/indent_val.json",
        save_path="./../../dataset/yolo_dataset/yolo_val/",
    )
