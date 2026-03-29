from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(candidate):
    file_name = f"{candidate['name']}_report.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Candidate: {candidate['name']}", styles["Title"]))
    content.append(Paragraph(f"ATS Score: {candidate['score']}", styles["Normal"]))

    content.append(Paragraph("Skills:", styles["Heading2"]))
    content.append(Paragraph(", ".join(candidate["skills"]), styles["Normal"]))

    content.append(Paragraph("Missing Skills:", styles["Heading2"]))
    content.append(Paragraph(", ".join(candidate["missing"]), styles["Normal"]))

    doc.build(content)

    return file_name