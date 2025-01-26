import cv2
import os
import json

products_file = 'products.json'

if os.path.exists(products_file):
    with open(products_file, 'r') as file:
        products = json.load(file)
else:
    products = []


cap = cv2.VideoCapture(0)
i = 0

product = input("Enter the product name: ")
os.makedirs(f'E:\\Grocery_Bill_Automation\\{product}', exist_ok=True)

if product not in products:
    products.append(product)


with open(products_file, 'w') as file:
    json.dump(products, file, indent=4)

print(f"Product '{product}' has been added.")
print(f"Current product list: {products}")

max_pictures = int(input("Enter the number of pictures you want to capture: "))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image.")
        break

    cv2.imshow('Webcam', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and i < max_pictures:
        image_path = f'E:\\Grocery_Bill_Automation\\{product}\\{product}{i}.jpg'
        cv2.imwrite(image_path, frame)
        print(f"Image {i + 1} captured and saved at {image_path}!")
        i += 1

    if i == max_pictures:
        print("Image capture limit reached.")
        break

    if key == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()


