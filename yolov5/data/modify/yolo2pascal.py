import os.path
import re
import cv2
import pandas as pd


class ConvertYOLOToPascal:
    """
    YOLO label format: class_id, x, y, width, height, score
    Pascal VOC format: class_id, score, xmin, ymin, xmax, ymax
    """

    def __init__(self, txt_folder, img_folder, save_path):
        self.txt_folder = txt_folder
        self.img_folder = img_folder
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def get_img_shape(self, img_path):
        img = cv2.imread(img_path)
        try:
            return img.shape
        except AttributeError:
            print("error!", img_path)
            return (None, None, None)

    def get_img_id(self):
        pattern = re.compile(r"[0-9]{4}\.jpg")
        img_ids = []
        for file_name in sorted(os.listdir(self.img_folder)):
            if pattern.fullmatch(file_name):
                img_ids.append(file_name[:4])
        return img_ids

    def txtfile_to_string(self, txt_path, img_path):
        image_name = re.findall(r"[0-9]{4}\.jpg", img_path)[0]
        image_id = f"test/{image_name}"
        image_width, image_height, _ = self.get_img_shape(img_path)

        if os.path.isfile(txt_path) == False:
            return image_id, ""

        with open(txt_path, "r") as f:
            lines = f.readlines()
        pascal_voc_string = f""
        for line in lines:
            class_id, x, y, w, h, score = line.strip().split()
            xmin = int(float(x) * image_width - 0.5 * float(w) * image_width)
            ymin = int(float(y) * image_height - 0.5 * float(h) * image_height)
            xmax = int(float(x) * image_width + 0.5 * float(w) * image_width)
            ymax = int(float(y) * image_height + 0.5 * float(h) * image_height)
            pascal_voc_string += f"{class_id} {score} {xmin} {ymin} {xmax} {ymax} "
        return image_id, pascal_voc_string.strip()

    def convert(self):
        pred_dict = {"image_id": [], "PredictionString": []}
        for img_id in self.get_img_id():
            id_col, pred_str = self.txtfile_to_string(
                self.txt_folder + f"/{img_id}.txt", self.img_folder + f"/{img_id}.jpg"
            )
            pred_dict["image_id"].append(id_col)
            pred_dict["PredictionString"].append(pred_str)

        pred_in_pascal = pd.DataFrame(pred_dict)
        pred_in_pascal.to_csv(self.save_path + "/result.csv", index=False)
        return


# To run in as a class
if __name__ == "__main__":
    ConvertYOLOToPascal(txt_folder="", img_folder="", save_path="").convert()
