import os
import cv2

def list_pictures(folder_path, extensions=('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(extensions)]

def resize_image(image, width=None, height=None):
    if width is None and height is None:
        return image
    h, w = image.shape[:2]
    if width is None:  
        scale = height / h
        dim = (int(w * scale), height)
    elif height is None: 
        scale = width / w
        dim = (width, int(h * scale))
    else:  
        dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def draw_rectangle(event, x, y, flags, param):
    global drawing, x_start, y_start, x_end, y_end, boxes, current_class_id
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_start, y_start = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            x_end, y_end = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x_end, y_end = x, y
        boxes.append((current_class_id, x_start, y_start, x_end, y_end))

folder = input("Enter the product name: ")
folder_path = f"E:/Grocery_Bill_Automation/{folder}"

distinguishable_suffix = "_coords"
output_folder = os.path.join(folder_path, folder + distinguishable_suffix)
os.makedirs(output_folder, exist_ok=True)

pictures = list_pictures(folder_path)
print("Found images:", pictures)

desired_width = 800
desired_height = 500

drawing = False
x_start, y_start, x_end, y_end = -1, -1, -1, -1
current_class_id = 0

for pic in pictures:
    image = cv2.imread(pic)
    if image is None:
        print(f"Unable to read image: {pic}")
        continue

    original_height, original_width = image.shape[:2]  
    resized_image = resize_image(image, width=desired_width, height=desired_height)
    resized_height, resized_width = resized_image.shape[:2]  
    
    boxes = []
    filename = os.path.splitext(os.path.basename(pic))[0]
    txt_file_path = os.path.join(output_folder, filename + ".txt")

    cv2.namedWindow("Image Viewer - Draw Boxes (Press 's' to SAVE)")
    cv2.setMouseCallback("Image Viewer - Draw Boxes (Press 's' to SAVE)", draw_rectangle)

    print("Press '0-9' to set class ID | 's' to SAVE | 'n' to SKIP")

    while True:
        temp_image = resized_image.copy()
        for box in boxes:
            class_id, x1, y1, x2, y2 = box
            cv2.rectangle(temp_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(temp_image, str(class_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if drawing and x_start != -1 and y_start != -1 and x_end != -1 and y_end != -1:
            cv2.rectangle(temp_image, (x_start, y_start), (x_end, y_end), (255, 0, 0), 1)
        cv2.imshow("Image Viewer - Draw Boxes (Press 's' to SAVE)", temp_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            if boxes:
                
                with open(txt_file_path, 'w') as f:
                    for box in boxes:
                        class_id, x1, y1, x2, y2 = box
                        
                        x1_orig = x1 * (original_width / resized_width)
                        y1_orig = y1 * (original_height / resized_height)
                        x2_orig = x2 * (original_width / resized_width)
                        y2_orig = y2 * (original_height / resized_height)
                        
                        x_center = ((x1_orig + x2_orig) / 2) / original_width
                        y_center = ((y1_orig + y2_orig) / 2) / original_height
                        box_width = abs(x2_orig - x1_orig) / original_width
                        box_height = abs(y2_orig - y1_orig) / original_height
                        
                        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")
                print(f"Saved coordinates to {txt_file_path}")
            else:
                print("No boxes to save. File not created.")
            break
        elif key == ord('n'):
            print("Skipping without save.")
            break
        elif key == ord('q'):
            cv2.destroyAllWindows()
            exit()
        elif key in [ord(str(i)) for i in range(10)]:
            current_class_id = int(chr(key))
            print(f"Current class ID: {current_class_id}")

    cv2.destroyWindow("Image Viewer - Draw Boxes (Press 's' to SAVE)")

cv2.destroyAllWindows()