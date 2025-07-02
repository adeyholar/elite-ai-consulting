from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

class PDFGenerator:
    def create_pdf(self, content, output_path, title):
        """
        Generate a PDF report with the given content and title.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(title, styles["Title"]))
        story.append(Spacer(1, 12))
        for line in content.split("\n"):
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 12))

        doc.build(story)
        return output_path