import json
import yaml
from ultralytics import YOLO

with open("products.json", "r") as f:
    products = json.load(f)

yaml_content = {
    "path": "E:/Grocery_Bill_Automation/YOLO_FINAL_DATA",
    "train": "images/train",
    "val": "images/val",
    "names": {i: product for i, product in enumerate(products)}
}

with open("YOLO_FINAL_DATA/data.yaml", "w") as f:
    yaml.dump(yaml_content, f, sort_keys=False)

print("data.yaml created successfully!")


model = YOLO("yolov8n.pt")  
# model = YOLO("yolov8x.pt")

results = model.train(
    data="YOLO_FINAL_DATA/data.yaml",
    epochs=50,
    batch=4,  
    imgsz=320,
    device="cpu",  
    workers=3, 
    name="grocery_detector_cpu",
    patience=10,
    optimizer="Adam",
    lr0=0.001,
    verbose=True
)
