from ultralytics import YOLO
import cv2
import json

model = YOLO("runs/detect/grocery_detector_cpu4/weights/best.pt")

with open("products.json", "r") as f:
    product_list = json.load(f)

product_prices = {}

for product in product_list:
    while True:
        price_input = input(f"Enter the price for {product} ($): ")
        try:
            price = round(float(price_input), 2)
            product_prices[product] = price
            break
        except ValueError:
            print("Please enter a valid number!")

with open("products.json", "w") as f:
    json.dump(product_prices, f, indent=2)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

captured_frame = None
detection_results = None
detection_class_ids = None

print("Press 's' to capture an image and display the bill, or 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    results = model.predict(frame, imgsz=640, conf=0.25)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
    class_names = results[0].names

    annotated_frame = frame.copy()
    for box, cls_id in zip(boxes, class_ids):
        x1, y1, x2, y2 = map(int, box)
        label = class_names[cls_id]
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    cv2.imshow("Live Detection - Press 's' to Save Bill", annotated_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        
        captured_frame = annotated_frame
        detection_results = results[0]
        detection_class_ids = class_ids
        break
    elif key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()


cap.release()
cv2.destroyAllWindows()


if captured_frame is not None and detection_results is not None:
 
    cv2.imwrite('grocery_items_annotated.jpg', captured_frame)
    

    class_names = detection_results.names
    

    item_counts = {}
    for cls_id in detection_class_ids:
        class_name = class_names[cls_id]
        if class_name in product_prices:
            item_counts[class_name] = item_counts.get(class_name, 0) + 1
        else:
            print(f"Warning: {class_name} not in price list - skipping")

  
    total = 0.0
    print("\n--- Your Grocery Bill ---")
    for item, count in item_counts.items():
        item_total = product_prices[item] * count
        total += item_total
        print(f"{item:<15} x{count:<2} @ ${product_prices[item]:.2f} = ${item_total:.2f}")
    print(f"\n{'Total:':<20} ${total:.2f}")
else:
    print("No valid capture detected!")