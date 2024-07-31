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

# Function to determine the governorate from the plate name
def determine_governorate(plate_number, plate_letters):
    if len(re.findall(r'\d', plate_number)) == 3 and len(plate_letters) == 3:
        return "Cairo"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 2:
        return "Giza"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'س':
        return "Alex"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ب':
        return "Beheira"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ف':
        return "Fayoum"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ر':
        return "Sharqia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ل':
        return "Kafr El Sheikh"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'و':
        return "Beni Suef"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'د':
        return "Dakahlia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ع':
        return "Gharbia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ن':
        return "Minya"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'م':
        return "Monufia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ق':
        return "Qalyubia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ي':
        return "Asyut"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ه':
        return "Sohag"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ج' and plate_letters[1] == 'ه':
        return "Matrouh"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ج' and plate_letters[1] == 'ب':
        return "El Wadi El Gedid"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ص' and plate_letters[1] == 'أ':
        return "Qena"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ص' and plate_letters[1] == 'ق':
        return "Luxor"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ص' and plate_letters[1] == 'و':
        return "Aswan"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'س':
        return "Suez"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'ص':
        return "Ismailia"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'ع':
        return "Port Said"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'د':
        return "Dameitta"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'أ':
        return "North Sinai"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'ج':
        return "South Sinai"
    elif len(re.findall(r'\d', plate_number)) == 4 and len(plate_letters) == 3 and plate_letters[0] == 'ط' and plate_letters[1] == 'ر':
        return "Red Sea"
    
    else:
        return "Unknown"

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
def create_pdf(search_result, cropped_images, detected_image, plate_number, plate_number_en, plate_letters_filtered, governorate):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    # Font paths
    regular_font_path = 'D:/car_plate_detection/website1/fonts/dejavu-sans/DejaVuSans.ttf'
    bold_font_path = 'D:/car_plate_detection/website1/fonts/dejavu-sans/DejaVuSans-Bold.ttf'

    # Add fonts
    if os.path.exists(regular_font_path):
        pdf.add_font('DejaVuSans', '', regular_font_path, uni=True)
    else:
        raise FileNotFoundError(f"Font file not found: {regular_font_path}")

    if os.path.exists(bold_font_path):
        pdf.add_font('DejaVuSans', 'B', bold_font_path, uni=True)
    else:
        raise FileNotFoundError(f"Font file not found: {bold_font_path}")

    # Set font
    pdf.set_font('DejaVuSans', size=12)

    # Title
    pdf.set_font("DejaVuSans", 'B', 16)
    pdf.cell(200, 10, txt="Car Plate Recognition Results", ln=True, align='C')
    pdf.ln(10)

    # Plate Information
    pdf.set_font("DejaVuSans", size=12)
    pdf.cell(200, 10, txt=f"Plate Number (Original): {plate_number}", ln=True)
    pdf.cell(200, 10, txt=f"Plate Number (Converted to English): {plate_number_en}", ln=True)
    pdf.cell(200, 10, txt=f"Plate Letters (Filtered): {plate_letters_filtered}", ln=True)
    pdf.cell(200, 10, txt=f"Governorate: {governorate}", ln=True)
    pdf.ln(10)

    # Search Results
    pdf.set_font("DejaVuSans", 'B', 12)
    pdf.cell(200, 10, txt="Search Results:", ln=True)
    pdf.set_font("DejaVuSans", size=12)

    for record in search_result:
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(0, 10, txt=f"ID: {record[0]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Plate Number: {record[1]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Plate Letters: {record[2]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Car Type: {record[3]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Car Owner: {record[4]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Governorate: {record[5]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Chassis Number: {record[6]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Email: {record[7]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Irregularities: {record[8]}", border=1, ln=True, fill=True)
        pdf.cell(0, 10, txt=f"Irregularities Reason: {record[9]}", border=1, ln=True, fill=True)
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
    # Object detection using YOLO
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    detected_image_yolo, boxes_yolo = detect_objects(uploaded_file)
    
    if detected_image_yolo is not None and boxes_yolo:
        st.image(detected_image_yolo, caption="Detected Objects with YOLO", use_column_width=True)
        
        # Crop detected objects from the image
        cropped_images = crop_detected_objects(uploaded_file, boxes_yolo)
        
        # Display cropped images
        st.subheader("Cropped Images")
        for cropped_image in cropped_images:
            st.image(cropped_image, caption="Cropped Image", use_column_width=True)
        
        # Text extraction using EasyOCR
        all_text_ocr = []
        for cropped_image in cropped_images:
            cropped_image_np = np.array(cropped_image)
            result_text_ocr = model_ocr.readtext(cropped_image_np, detail=0)
            all_text_ocr.extend(result_text_ocr)
        
        # Combine and display all text extracted using EasyOCR
        st.subheader("Extracted Text with EasyOCR")
        combined_text = " ".join(all_text_ocr)
        st.write(combined_text)
        
        # Split result_text_ocr into numbers and alphabets
        plate_number = "".join(re.findall(r'\d+', " ".join(all_text_ocr)))
        plate_letters = "".join(re.findall(r'\D+', " ".join(all_text_ocr)))
        
        # Convert Arabic numbers to English if found
        plate_number_en = convert_arabic_to_english(plate_number)
        
        # Filter plate_letters to keep only Arabic alphabetic characters
        plate_letters_filtered = filter_arabic_letters(plate_letters)
        
        # Determine governorate
        governorate = determine_governorate(plate_number, plate_letters_filtered)
        
        st.write("Plate Number (Original):", plate_number)
        st.write("Plate Number (Converted to English):", plate_number_en)
        st.write("Plate Letters (Filtered):", plate_letters_filtered)
        st.write("Governorate:", governorate)

        # Database search
        conn = connect_to_database()
        if conn:
            search_result = search_data(conn, plate_number_en, plate_number, plate_letters_filtered)
            if search_result:
                st.subheader("Search Results")
                for record in search_result:
                    st.write(f"ID: {record[0]}")
                    st.write(f"Plate Number: {record[1]}")
                    st.write(f"Plate Letters: {record[2]}")
                    st.write(f"Car Type: {record[3]}")
                    st.write(f"Car Owner: {record[4]}")
                    st.write(f"Governorate: {record[5]}")
                    st.write(f"Chassis Number: {record[6]}")
                    st.write(f"Email: {record[7]}")
                    st.write(f"Irregularities: {record[8]}")
                    st.write(f"Irregularities Reason: {record[9]}")
                    st.write("---")
                
                # Create PDF with the search results and images
                pdf_data = create_pdf(search_result, cropped_images, detected_image_yolo, plate_number, plate_number_en, plate_letters_filtered, governorate)
                st.download_button("Download PDF", data=pdf_data, file_name=f"{record[4]}.pdf", mime="application/pdf")
            else:
                st.write("No matching records found in the database.")
            conn.close()
        else:
            st.write("Failed to connect to the database.")
    else:
        st.write("No objects detected.")
else:
    st.write("Please upload an image or take a photo.")


st.balloons()
