from pathlib import Path
import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import easyocr as ocr
import mysql.connector
import re
import io
import tempfile
import os
from fpdf import FPDF

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import tempfile

# YOLOv8 object detection
model_yolo = None
confidence_yolo = 0.4

def load_model_yolo(model_path):
    return YOLO(model_path)

def detect_objects(image):
    if model_yolo is None:
        return None, []

    pil_image = Image.open(image)
    np_image = np.array(pil_image)
    results = model_yolo(np_image, conf=confidence_yolo, show_conf=True)
    
    annotated_image = results[0].plot()
    boxes = results[0].boxes.xyxy.tolist()  # List of bounding boxes
    return annotated_image, boxes

def crop_detected_objects(image, boxes):
    pil_image = Image.open(image)
    cropped_images = []
    
    for box in boxes:
        x1, y1, x2, y2 = [int(coord) for coord in box]
        cropped_image = pil_image.crop((x1, y1, x2, y2))
        cropped_images.append(cropped_image)
    
    return cropped_images

# EasyOCR text extraction
@st.cache_resource
def load_model_ocr():
    return ocr.Reader(['ar'], model_storage_directory=r"D:\car_plate_detection\car plates-\Automatic-number-plate-recognition-in-real-time-")

model_ocr = load_model_ocr()

# Initialize YOLOv8 model   
model_path_yolo = Path(r"D:\car_plate_detection\car plates-\Automatic-number-plate-recognition-in-real-time-\best.pt")
model_yolo = load_model_yolo(model_path_yolo)

# Connect to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="2442003",
            database="car_plates"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to convert Arabic numerals to English
def convert_arabic_to_english(arabic_num):
    arabic_to_english = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }
    english_num = ''.join(arabic_to_english.get(ch, ch) for ch in arabic_num)
    return english_num

# Function to remove non-Arabic alphabetic characters
def filter_arabic_letters(text):
    return ''.join(ch for ch in text if '\u0600' <= ch <= '\u06FF')

# Function to search for data in the database
def search_data(conn, plate_number_en, plate_number, plate_letters):
    cursor = conn.cursor()
    query = """
    SELECT * FROM car_data 
    WHERE (plate_number = %s OR plate_number = %s) 
    AND plate_letters = %s
    """
    cursor.execute(query, (plate_number_en, plate_number, plate_letters))
    result = cursor.fetchall()
    cursor.close()
    return result

# Function to create PDF
def create_pdf(search_result, cropped_images, detected_image, plate_number, plate_number_en, plate_letters_filtered):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="Car Plate Recognition Results", ln=True, align='C')
    pdf.ln(10)

    # Plate Information
    pdf.cell(200, 10, txt=f"Plate Number (Original): {plate_number}", ln=True)
    pdf.cell(200, 10, txt=f"Plate Number (Converted to English): {plate_number_en}", ln=True)
    pdf.cell(200, 10, txt=f"Plate Letters (Filtered): {plate_letters_filtered}", ln=True)
    pdf.ln(10)

    # Search Results
    pdf.cell(200, 10, txt="Search Results:", ln=True)
    for record in search_result:
        pdf.cell(200, 10, txt=f"ID: {record[0]}, Plate Number: {record[1]}, Plate Letters: {record[2]}, Car Type: {record[3]}, Car Owner: {record[4]}, Governorate: {record[5]}, Chassis Number: {record[6]}, Email: {record[7]}, Irregularities: {record[8]}, Irregularities Reason: {record[9]}", ln=True)
    
    pdf.ln(10)

    # Convert and Add Detected Objects Image
    if detected_image is not None:
        detected_image_pil = Image.fromarray(detected_image)  # Convert NumPy array to PIL Image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            detected_image_pil.save(temp_file, format='JPEG')
            temp_file_path = temp_file.name
        pdf.image(temp_file_path, x=10, y=None, w=180)
        os.remove(temp_file_path)  # Clean up temporary file
        pdf.ln(10)

    # Add Cropped Images
    for i, image in enumerate(cropped_images):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            image.save(temp_file, format='JPEG')
            temp_file_path = temp_file.name
        pdf.image(temp_file_path, x=10, y=None, w=180)
        os.remove(temp_file_path)  # Clean up temporary file
        pdf.ln(10)

    # Save PDF to a BytesIO object
    pdf_output = io.BytesIO()
    pdf.output(pdf_output, 'F')
    pdf_output.seek(0)
    return pdf_output

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

    # Detect objects in the image using YOLOv8
    detected_image_yolo, boxes = detect_objects(uploaded_file)
    if detected_image_yolo is not None:
        st.image(detected_image_yolo, caption="Detected Objects (YOLO).", use_column_width=True)

    # Crop detected objects
    cropped_images = crop_detected_objects(uploaded_file, boxes)
    
    # Display each cropped region
    st.header("Cropped Detected Objects:")
    ocr_results = []

    for i, cropped_image in enumerate(cropped_images):
        st.image(cropped_image, caption=f"Cropped Object {i+1}", use_column_width=True)

        # Apply OCR to each cropped image
        cropped_image_np = np.array(cropped_image)
        result_ocr = model_ocr.readtext(cropped_image_np)
        
        # Extract and store OCR results
        result_text_ocr = [text[1] for text in result_ocr]
        ocr_results.append((i+1, result_text_ocr))
        
        st.write(f"OCR Results for Cropped Object {i+1}:", result_text_ocr)

    # Combine results for all cropped images
    all_text_ocr = [text for _, texts in ocr_results for text in texts]
    
    # Split result_text_ocr into numbers and alphabets
    plate_number = "".join(re.findall(r'\d+', " ".join(all_text_ocr)))
    plate_letters = "".join(re.findall(r'\D+', " ".join(all_text_ocr)))

    # Convert Arabic numbers to English if found
    plate_number_en = convert_arabic_to_english(plate_number)

    # Filter plate_letters to keep only Arabic alphabetic characters
    plate_letters_filtered = filter_arabic_letters(plate_letters)

    st.write("Plate Number (Original):", plate_number)
    st.write("Plate Number (Converted to English):", plate_number_en)
    st.write("Plate Letters (Filtered):", plate_letters_filtered)

    # Connect to the database
    conn = connect_to_database()
    if conn:
        # Search with original and converted Arabic numbers
        search_result = search_data(conn, plate_number_en, plate_number, plate_letters_filtered)
        
        conn.close()

        st.header("Search Results:")
        if not search_result:
            st.info("No matching records found.")
        else:
            for record in search_result:
                st.text(f"ID: {record[0]}, Plate Number: {record[1]}, Plate Letters: {record[2]}, Car Type: {record[3]}, Car Owner: {record[4]}, Governorate: {record[5]}, Chassis Number: {record[6]}, Email: {record[7]}, Irregularities: {record[8]}, Irregularities Reason: {record[9]}")
        
            # Create PDF with the search results and images
            pdf_data = create_pdf(search_result, cropped_images, detected_image_yolo, plate_number, plate_number_en, plate_letters_filtered)

            # Allow user to download the PDF
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="car_plate_results.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Failed to connect to the database.")

    st.balloons()
