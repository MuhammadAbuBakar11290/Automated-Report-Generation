from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime
import os
from PIL import Image as PILImage, ImageDraw


# Function to create a circular image
def create_circular_image(input_image_path, output_image_path):
    im = PILImage.open(input_image_path).convert("RGBA")
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = PILImage.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, PILImage.Resampling.LANCZOS)
    im.putalpha(mask)
    im.save(output_image_path)

def create_patient_summary(filename, doc_name, patient_name, patient_cnic, patient_gender, age, nationality, disease_detected, medicine_recommendations, special_instructions, hospital_name, hospital_logo):
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4)
    content = []

    # Define styles
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(name='Header', fontSize=24, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=12, backColor='#D6E4F0', borderPadding=25)
    subheader_style = ParagraphStyle(name='Subheader', fontSize=12, fontName='Helvetica-Bold', alignment=TA_LEFT, spaceAfter=6, spaceBefore=6)
    normal_style = ParagraphStyle(name='Normal', fontSize=10, fontName='Helvetica', alignment=TA_LEFT, spaceAfter=12)
    medicine_style = ParagraphStyle(name='Medicine', fontSize=10, fontName='Helvetica', alignment=TA_LEFT, spaceAfter=12, backColor='#F2F2F2')
    special_instructions_style = ParagraphStyle(name='SpecialInstructions', fontSize=10, fontName='Helvetica', alignment=TA_LEFT, spaceAfter=12, backColor='#F2F2F2')

    # Add the main heading (centered)
    content.append(Paragraph("Patient Report", header_style))
    content.append(Spacer(1, 12))  # Spacer for visual separation

    # Create a table for logo and hospital name
    logo_image = None
    if hospital_logo and os.path.exists(hospital_logo):
        logo_image = Image(hospital_logo, width=5*cm, height=5*cm)

    # Create a row for the logo and hospital name
    logo_and_hospital_name_data = [
        [logo_image, Paragraph(f"<b>{hospital_name}</b>", normal_style)]
    ]
    
    logo_and_hospital_name_table = Table(logo_and_hospital_name_data, colWidths=[5*cm, 10*cm])  # Adjust column widths as needed
    logo_and_hospital_name_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Align logo to the left
        ('ALIGN', (1, 0), (1, 0), 'LEFT')    # Align hospital name to the left
    ]))
    
    content.append(logo_and_hospital_name_table)
    content.append(Spacer(1, 6))

    # Add doctor name on the left and date on the right
    doctor_and_date_data = [
        [Paragraph(f"Doctor: {doc_name}", normal_style), 
         Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style)]
    ]
    
    doctor_and_date_table = Table(doctor_and_date_data, colWidths=[9*cm, 6*cm])  # Adjust column widths
    doctor_and_date_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Align doctor name to the left
        ('ALIGN', (1, 0), (1, 0), 'RIGHT')   # Align date to the right
    ]))

    content.append(doctor_and_date_table)
    content.append(Spacer(1, 12))

    # Patient Demographics Header
    content.append(Paragraph("Patient Demographics", subheader_style))
    content.append(Spacer(1, 12))

    # Patient Demographics Table
    data = [
        ["Patient Name", "Patient CNIC", "Gender", "Age"],
        [patient_name, patient_cnic, patient_gender, age]
    ]
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica')
    ])
    
    table = Table(data, colWidths=[4.5*cm, 4.5*cm, 4.5*cm, 4.5*cm])
    table.setStyle(table_style)
    
    content.append(table)
    content.append(Spacer(1, 12))

    # Disease Detected Section
    content.append(Paragraph(f"<b>Disease Detected:</b> {disease_detected}", subheader_style))
    content.append(Spacer(1, 12))

    # Medicine Recommendations
    medicine_list = '\n'.join([f"{i+1}. {med}" for i, med in enumerate(medicine_recommendations)])
    medicine_recommendations_paragraph = Paragraph(f"<b>Medicine Recommendations:</b><br/>{medicine_list}", medicine_style)
    content.append(medicine_recommendations_paragraph)
    content.append(Spacer(1, 12))

    # Special Instructions
    special_instructions_paragraph = Paragraph(f"<b>Special Instructions:</b><br/>{special_instructions}", special_instructions_style)
    content.append(special_instructions_paragraph)

    # Build PDF
    doc.build(content)

# Example usage
doc_name = "Dr. John Doe"
patient_name = "Alice Smith"
patient_cnic = "1234567890"
patient_gender = "Female"
age = "30"
nationality = "American"
disease_detected = "Pneumonia"
medicine_recommendations = ["Calpol 25mg", "Panadol 2 tablets"]
special_instructions = "Rest for 7 days, avoid strenuous activity"
hospital_name = "St. Elizabeth Hospital"
hospital_logo = "Logo.png"  # Ensure this file exists

create_patient_summary("patient_summary_report.pdf", doc_name, patient_name, patient_cnic, patient_gender, age, nationality, disease_detected, medicine_recommendations, special_instructions, hospital_name, hospital_logo)
