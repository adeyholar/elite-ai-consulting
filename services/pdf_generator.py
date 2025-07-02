from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import re

class PDFGenerator:
    def create_pdf(self, content, output_path, title):
        """
        Generate a PDF report with the given content and title, cleaning formatting artifacts.
        """
        # Use the provided output_path directly (already includes 'reports/' from report_agent.py)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(title, styles["Title"]))
        story.append(Spacer(1, 12))
        # Clean content (remove extra quotes, "lnn", excessive asterisks, and initial artifacts)
        cleaned_content = re.sub(r'["\']|lnn|\*+|^In/n', '', content, flags=re.MULTILINE)  # Remove quotes, "lnn", asterisks, and "In/n"
        paragraphs = [p.strip() for p in cleaned_content.split("\n\n") if p.strip()]
        for paragraph in paragraphs:
            story.append(Paragraph(paragraph, styles["Normal"]))
            story.append(Spacer(1, 12))

        try:
            doc.build(story)
            return output_path
        except Exception as e:
            print(f"Error building PDF: {e}")
            return None