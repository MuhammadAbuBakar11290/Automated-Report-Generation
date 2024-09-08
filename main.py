from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw
from datetime import datetime

# Function to create a circular image
def create_circular_image(input_image_path, output_image_path):
    im = Image.open(input_image_path).convert("RGBA")
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.Resampling.LANCZOS)  # Use LANCZOS for resizing
    im.putalpha(mask)
    im.save(output_image_path)


# Function to create the patient summary PDF
def create_patient_summary(output_file, doc_name, patient_name, patient_cnic, patient_gender, age, disease_detected, medicine_recommendations, special_instructions, hospital_name, hospital_logo):
    # Create circular hospital logo
    circular_logo_path = "circular_logo.png"
    create_circular_image(hospital_logo, circular_logo_path)

    # Create the PDF document
    doc = SimpleDocTemplate(output_file, pagesize=A4)

    # Styles
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(name='Header', fontSize=22, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=12, backColor='#D6E4F0', borderPadding=8)
    subheader_style = ParagraphStyle(name='Subheader', fontSize=12, fontName='Helvetica-Bold', alignment=TA_LEFT)
    normal_style = ParagraphStyle(name='Normal', fontSize=10, fontName='Helvetica', alignment=TA_LEFT, spaceAfter=12)

    # Create a story (list of elements) for the document
    story = []

    # Add the main heading
    story.append(Paragraph("Patient Report", header_style))
    story.append(Spacer(1, 12))  # Spacer for visual separation

    # Add hospital logo and name
    story.append(Paragraph(f'<img src="{circular_logo_path}" width="50" height="50"/> {hospital_name}', subheader_style))
    story.append(Spacer(1, 12))

    # Add doctor name and date
    date_today = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Doctor: {doc_name}", subheader_style))
    story.append(Paragraph(f"Date: {date_today}", subheader_style))
    story.append(Spacer(1, 12))

    # Patient demographics table
    data = [
        ["Patient Name", "Patient CNIC", "Gender", "Age"],
        [patient_name, patient_cnic, patient_gender, age]
    ]
    table = Table(data, colWidths=[2.5 * inch] * 4)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    # Add the disease detected section
    story.append(Paragraph("Disease Detected", subheader_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(disease_detected, normal_style))
    story.append(Spacer(1, 12))

    # Add medicine recommendations section
    story.append(Paragraph("Medicine Recommendations", subheader_style))
    story.append(Spacer(1, 6))
    for medicine in medicine_recommendations:
        story.append(Paragraph(medicine, normal_style))
    story.append(Spacer(1, 12))

    # Add special instructions section
    story.append(Paragraph("Special Instructions", subheader_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(special_instructions, normal_style))

    # Build the PDF
    doc.build(story)

# Example usage
if __name__ == "__main__":
    doc_name = "Dr. John Doe"
    patient_name = "Muhammad AbuBakar"
    patient_cnic = "12345-6789012-3"
    patient_gender = "Male"
    age = "25"
    disease_detected = "Flu"
    medicine_recommendations = ["Calpol 25mg", "Panadol 2 tablets"]
    special_instructions = "Stay hydrated and rest."
    hospital_name = "City Hospital"
    hospital_logo = "Logo.png"  # Path to your logo

    create_patient_summary("patient_summary_report.pdf", doc_name, patient_name, patient_cnic, patient_gender, age, disease_detected, medicine_recommendations, special_instructions, hospital_name, hospital_logo)
