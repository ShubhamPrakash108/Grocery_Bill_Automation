import os
import json
import shutil
import random

def list_pictures(folder_path, extensions=('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(extensions)]

def list_text_files(folder_path, extensions=('.txt')):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(extensions)]

os.makedirs("YOLO_Dataset", exist_ok=True)
os.makedirs("YOLO_Dataset/pictures", exist_ok=True)
os.makedirs("YOLO_Dataset/labels", exist_ok=True)

with open('products.json', 'r') as f:
    products = json.load(f)

pictures = []
texts = []

main_dir = "E:/Grocery_Bill_Automation/"

for product in products:
    img_dir = os.path.join(main_dir, product)
    picture_files = list_pictures(img_dir)
    for pic in picture_files:
        pictures.append(pic)
        shutil.copy(pic, "YOLO_Dataset/pictures")

    txt_dir = os.path.join(img_dir, f"{product}_coords")
    text_files = list_text_files(txt_dir)
    for txt in text_files:
        texts.append(txt)
        shutil.copy(txt, "YOLO_Dataset/labels")

print("Pictures")
print(pictures)
print("\n")
print("Texts")
print(texts)

base_dir = "YOLO_FINAL_DATA"
os.makedirs(f"{base_dir}/images/train", exist_ok=True)
os.makedirs(f"{base_dir}/images/val", exist_ok=True)
os.makedirs(f"{base_dir}/labels/train", exist_ok=True)
os.makedirs(f"{base_dir}/labels/val", exist_ok=True)

with open('products.json', 'r') as f:
    products = json.load(f)

main_dir = "E:/Grocery_Bill_Automation/"

def list_files(folder_path, extensions):
    return [f for f in os.listdir(folder_path) if f.lower().endswith(extensions)]

for product in products:
    img_dir = os.path.join(main_dir, product)
    txt_dir = os.path.join(img_dir, f"{product}_coords")

    images = list_files(img_dir, ('.jpg', '.jpeg', '.png'))
    labels = list_files(txt_dir, ('.txt',))

    images.sort()
    labels.sort()
    data = [(img, f"{os.path.splitext(img)[0]}.txt") for img in images if f"{os.path.splitext(img)[0]}.txt" in labels]

    random.shuffle(data)
    split_idx = int(len(data) * 0.8)
    train_data = data[:split_idx]
    val_data = data[split_idx:]

    for img, lbl in train_data:
        shutil.copy(os.path.join(img_dir, img), f"{base_dir}/images/train")
        shutil.copy(os.path.join(txt_dir, lbl), f"{base_dir}/labels/train")

    for img, lbl in val_data:
        shutil.copy(os.path.join(img_dir, img), f"{base_dir}/images/val")
        shutil.copy(os.path.join(txt_dir, lbl), f"{base_dir}/labels/val")

pictures_folder = "YOLO_Dataset/pictures"
labels_folder = "YOLO_Dataset/labels"
if os.path.exists(pictures_folder):
    shutil.rmtree(pictures_folder)
if os.path.exists(labels_folder):
    shutil.rmtree(labels_folder)

print("YOLO dataset has been created in the 'YOLO_FINAL_DATA' folder with the required format.")
print("Temporary folders have been deleted to save space.")