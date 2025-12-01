from fpdf import FPDF
import os

def create_sample_pdf(path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Medical Report", ln=1, align="C")
    pdf.cell(200, 10, txt="Patient: John Doe", ln=1, align="L")
    pdf.cell(200, 10, txt="Date: 2023-10-27", ln=1, align="L")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Findings:", ln=1, align="L")
    pdf.multi_cell(0, 10, txt="Blood Pressure: 120/80 mmHg\nHeart Rate: 72 bpm\nCholesterol: 180 mg/dL\n\nNotes: Patient is in good health. No significant abnormalities detected.")
    
    pdf.output(path)
    print(f"Created sample PDF at {path}")

if __name__ == "__main__":
    os.makedirs("healthmate_ai/samples", exist_ok=True)
    create_sample_pdf("healthmate_ai/samples/sample_report.pdf")
