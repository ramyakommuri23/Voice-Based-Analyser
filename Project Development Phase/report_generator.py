from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def generate_pdf_report(report_data, waveform_buf, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Voice Based Concept Understanding Report")
    c.setFont("Helvetica", 11)
    y = height - 100

    # Reference and transcript
    ref = report_data.get("Reference", "")
    transcript = report_data.get("Transcript", "")
    c.drawString(72, y, "Reference Concept:")
    y -= 16
    c.setFont("Helvetica", 10)
    text = c.beginText(72, y)
    for line in ref.splitlines():
        text.textLine(line)
        y -= 12
    c.drawText(text)

    y -= 8
    c.setFont("Helvetica", 10)
    text = c.beginText(72, y)
    text.textLine("Student Transcription:")
    y -= 14
    for line in transcript.splitlines():
        text.textLine(line)
        y -= 12
    c.drawText(text)

    # Waveform image
    if waveform_buf is not None:
        try:
            img = ImageReader(waveform_buf)
            c.drawImage(img, 72, y - 160, width=450, height=120)
            y -= 170
        except Exception:
            pass

    # Metrics table
    y -= 8
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Evaluation Summary")
    y -= 18
    c.setFont("Helvetica", 10)
    for k in ["Semantic Similarity", "Filler Word Ratio", "Pause Ratio", "Confidence (Energy)", "Final Score", "Understanding Level"]:
        v = report_data.get(k, "")
        c.drawString(72, y, f"{k}")
        c.drawString(300, y, str(v))
        y -= 14

    c.showPage()
    c.save()
