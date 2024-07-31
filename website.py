from pathlib import Path
import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import easyocr as ocr

# YOLOv3 object detection
model_yolo = None
confidence_yolo = 0.4

def load_model_yolo(model_path):
    return YOLO(model_path)

def detect_objects(image):
    if model_yolo is None:
        return None

    pil_image = Image.open(image)
    np_image = np.array(pil_image)
    results = model_yolo(np_image, conf=confidence_yolo, hide_conf=True)
    annotated_image = results[0].plot()
    return annotated_image

# EasyOCR text extraction
@st.cache_resource
def load_model_ocr():
    return ocr.Reader(['ar'], model_storage_directory=r"D:\car_plate_detection\car plates-\Automatic-number-plate-recognition-in-real-time-")

model_ocr = load_model_ocr()

# Initialize YOLOv3 model
model_path_yolo = Path(r"D:\car_plate_detection\car plates-\Automatic-number-plate-recognition-in-real-time-\best.pt")
model_yolo = load_model_yolo(model_path_yolo)

# Streamlit app
st.title("Object Detection with YOLO and EasyOCR")

# Choose to upload an image or take a photo with the camera
upload_option = st.radio(
    "Choose an option to provide an image:",
    ("Upload an image", "Take a photo with camera")
)

if upload_option == "Upload an image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "webp"])
elif upload_option == "Take a photo with camera":
    uploaded_file = st.camera_input("Take a photo...")

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

    # Detect objects in the image using YOLOv3
    detected_image_yolo = detect_objects(uploaded_file)
    if detected_image_yolo is not None:
        st.image(detected_image_yolo, caption="Detected Objects (YOLO).", use_column_width=True)

    # Extract text from the image using EasyOCR
    input_image_ocr = Image.open(uploaded_file)
    result_ocr = model_ocr.readtext(np.array(input_image_ocr))

    result_text_ocr = []
    for text in result_ocr:
        result_text_ocr.append(text[1])

    st.write("OCR Results:", result_text_ocr)
    st.balloons()
