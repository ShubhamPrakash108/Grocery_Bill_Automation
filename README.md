# 🛒 Grocery Bill Automation with YOLOv8


Automate grocery billing using YOLO object detection! This project captures product images, trains a custom YOLO model, and generates itemized bills in real-time.


 📋 Table of Contents
- [Prerequisites](#-prerequisites)
- [Setup](#-setup)
- [File Structure](#-file-structure)
- [Usage Sequence](#-usage-sequence)
- [Sample Workflow](#-sample-workflow)
- [License](#-license)

---

 📦 Prerequisites
- Python 3.8+
- Required Packages:
  
  pip install opencv-python ultralytics pyyaml
 
- Webcam (for image capture/detection)
- Recommended: NVIDIA GPU (for faster training)

---

 🛠️ Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/grocery-bill-automation.git
   cd grocery-bill-automation
   ```

2. Create base directory:
   ```bash
   mkdir Grocery_Bill_Automation
   ```

---

 📂 File Structure
```
.
├── Grocery_Bill_Automation/       # Product images/labels
├── products.json                  # Product database
│
├── camera.py                      # Capture product images
├── label.py                       # Draw bounding boxes
├── format_files.py                # Prepare YOLO dataset
├── train_yolo.py                  # Train detection model
└── final_bill_maker.py            # Generate bills
```

---

## 🚀 Usage Sequence

### 1. **Capture Images** (`camera.py`)
**Purpose**: Collect training images via webcam  
**Command**:
```bash
python camera.py
```
- Enter product name (e.g., "apple")
- Specify number of images to capture
- Press `S` to capture, `Q` to exit

---

### 2. **Label Images** (`label.py`)
**Purpose**: Annotate bounding boxes in YOLO format  
**Command**:
```bash
python label.py
```
- Enter same product name used in `camera.py`
- **Controls**:
  - `0-9`: Set class ID (matches product order in `products.json`)
  - `Mouse`: Draw bounding boxes
  - `S`: Save annotations
  - `N`: Skip image

---

### 3. **Format Dataset** (`format_files.py`)
**Purpose**: Organize data for YOLO training  
**Command**:
```bash
python format_files.py
```
- Automatically:
  - Creates train/val split (80/20)
  - Generates YOLO-compatible folder structure
  - Deletes temporary files

---

### 4. **Train Model** (`train_yolo.py`)
**Purpose**: Train custom YOLOv8 detector  
**Command**:
```bash
python train_yolo.py
```
- Default config:
  - Model: `yolov8n.pt` (nano version)
  - Epochs: 50
  - Batch size: 4
  - Input size: 320x320
- Training logs saved to `runs/detect/grocery_detector_cpu`

---

### 5. **Generate Bill** (`final_bill_maker.py`)
**Purpose**: Real-time detection + billing  
**Command**:
```bash
python final_bill_maker.py
```
1. Enter product prices when prompted
2. Point camera at items
3. Press `S` to capture and calculate bill
4. Press `Q` to exit

**Output**:
- Annotated image: `grocery_items_annotated.jpg`
- Terminal bill display

---

## 🔄 Sample Workflow
```bash
# Add "chocolate" product
python camera.py
> Product name: chocolate
> Images to capture: 30

# Label chocolate boxes
python label.py
> Product name: chocolate
> (Draw boxes with class ID 0)

# Prepare dataset and train
python format_files.py
python train_yolo.py

# Run detection
python final_bill_maker.py
> Enter price for chocolate: 2.99
```

---

## 💻 Sample Bill Output
```plaintext
--- Your Grocery Bill ---
chocolate     x2  @ $2.99 = $5.98
apple         x4  @ $0.75 = $3.00

Total:              $8.98
```

---

## 📝 Notes
1. **GPU Acceleration**: Modify `device="cuda"` in `train_yolo.py` for GPU training
2. **Class IDs**: Must match product order in `products.json`
3. **File Paths**: Default paths assume Windows - adjust for Linux/Mac
4. **Model Choice**: Switch to `yolov8x.pt` in `train_yolo.py` for higher accuracy

---

## 📜 License
MIT License - Free for personal and commercial use. See [LICENSE](LICENSE) for details.
```
