"""
Certificate PDF generation module using ReportLab
"""
from reportlab.lib.pagesizes import landscape, portrait, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from PIL import Image
import io
from datetime import datetime, timedelta
from typing import Optional, Tuple, TYPE_CHECKING
import json
import sys
from pathlib import Path

if TYPE_CHECKING:
    from app import crud
    from app.utils import FileHelper

class CertificateGenerator:
    """Generate PDF certificates"""
    
    def __init__(self, width: float = 11, height: float = 8.5):
        """Initialize with certificate dimensions in inches"""
        self.width = width * inch
        self.height = height * inch
    
    def generate(self, 
                 output_path: str,
                 background_image: Optional[bytes] = None,
                 template_json: Optional[str] = None,
                 data: dict = None) -> str:
        """Generate certificate PDF"""
        
        c = canvas.Canvas(output_path, pagesize=(self.width, self.height))
        
        # Draw background image
        if background_image:
            self._draw_background(c, background_image)
        else:
            self._draw_default_background(c)
        
        # Draw template elements
        if template_json:
            self._draw_template(c, template_json, data or {})
        else:
            self._draw_default_content(c, data or {})
        
        c.save()
        return output_path
    
    def _draw_background(self, c: canvas.Canvas, bg_image: bytes):
        """Draw background image"""
        try:
            img = Image.open(io.BytesIO(bg_image))
            img_width = self.width
            img_height = self.height
            
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            c.drawImage(img_buffer, 0, 0, width=img_width, height=img_height)
        except Exception as e:
            print(f"Error drawing background: {e}")
    
    def _draw_default_background(self, c: canvas.Canvas):
        """Draw default certificate background"""
        # White background
        c.setFillColor(HexColor("#FFFFFF"))
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        
        # Gold border
        c.setStrokeColor(HexColor("#D4AF37"))
        c.setLineWidth(2)
        c.rect(0.2*inch, 0.2*inch, self.width - 0.4*inch, self.height - 0.4*inch)
    
    def _draw_template(self, c: canvas.Canvas, template_json: str, data: dict):
        """Draw template elements onto certificate"""
        try:
            template = json.loads(template_json)
            
            for element in template.get('elements', []):
                element_type = element.get('type')
                
                if element_type == 'text':
                    self._draw_text_element(c, element, data)
                elif element_type == 'image':
                    self._draw_image_element(c, element, data)
                elif element_type == 'qrcode':
                    self._draw_qrcode_element(c, element, data)
                elif element_type == 'date':
                    self._draw_date_element(c, element, data)
        except Exception as e:
            print(f"Error drawing template: {e}")
    
    def _draw_text_element(self, c: canvas.Canvas, element: dict, data: dict):
        """Draw text element"""
        content = element.get('content', '')
        
        # Replace field placeholders
        for key, value in data.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
        
        x = (element.get('x', 0) / 100) * self.width
        y = (element.get('y', 0) / 100) * self.height
        font_size = element.get('fontSize', 12)
        font_name = element.get('fontName', 'Helvetica')
        color = element.get('color', '#000000')
        
        c.setFont(font_name, font_size)
        c.setFillColor(HexColor(color))
        c.drawString(x, y, content)
    
    def _draw_image_element(self, c: canvas.Canvas, element: dict, data: dict):
        """Draw image element"""
        pass
    
    def _draw_qrcode_element(self, c: canvas.Canvas, element: dict, data: dict):
        """Draw QR code element"""
        pass
    
    def _draw_date_element(self, c: canvas.Canvas, element: dict, data: dict):
        """Draw date element"""
        date_format = element.get('format', '%Y-%m-%d')
        date_value = datetime.utcnow().strftime(date_format)
        
        x = (element.get('x', 0) / 100) * self.width
        y = (element.get('y', 0) / 100) * self.height
        font_size = element.get('fontSize', 12)
        
        c.setFont('Helvetica', font_size)
        c.setFillColor(HexColor('#000000'))
        c.drawString(x, y, date_value)
    
    def _draw_default_content(self, c: canvas.Canvas, data: dict):
        """Draw default certificate content"""
        # Title
        c.setFont('Helvetica-Bold', 32)
        c.setFillColor(HexColor('#1F4788'))
        c.drawString(1*inch, self.height - 1.5*inch, 'Certificate of Achievement')
        
        # Recipient
        c.setFont('Helvetica', 14)
        c.setFillColor(HexColor('#000000'))
        c.drawString(1*inch, self.height - 2.5*inch, 'This certifies that')
        
        c.setFont('Helvetica-Bold', 18)
        c.drawString(1*inch, self.height - 3*inch, data.get('student_name', 'Student Name'))
        
        # Achievement
        c.setFont('Helvetica', 12)
        c.drawString(1*inch, self.height - 3.7*inch, f"Has successfully completed {data.get('course', 'the course')}")
        
        # Date
        c.setFont('Helvetica', 10)
        date_str = datetime.utcnow().strftime('%B %d, %Y')
        c.drawString(1*inch, self.height - 5*inch, f'Date: {date_str}')
        
        # Certificate Number
        c.setFont('Helvetica-Oblique', 8)
        cert_num = data.get('certificate_number', 'CERT-XXXX-XXXX')
        c.drawString(1*inch, 0.5*inch, f'Certificate #: {cert_num}')

class CertificateBulkGenerator:
    """Generate certificates in bulk"""
    
    def __init__(self, template_id: int, db):
        self.template_id = template_id
        self.db = db
        self.generator = CertificateGenerator()
    
    def process_batch(self, records: list, output_dir: str) -> dict:
        """Process batch of certificate records"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
        from app import crud
        from app.utils import FileHelper
        
        results = {
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        template = crud.TemplateCRUD.get_template(self.db, self.template_id)
        if not template:
            results['errors'].append(f"Template {self.template_id} not found")
            return results
        
        for record in records:
            try:
                # Generate certificate
                filename = f"cert_{record.get('student_id', 'unknown')}.pdf"
                filepath = FileHelper.save_file(
                    self._generate_pdf(template, record),
                    filename,
                    output_dir
                )
                
                cert_data = {
                    'student_name': record.get('student_name'),
                    'student_email': record.get('student_email'),
                    'student_id': record.get('student_id'),
                    'marks': record.get('marks'),
                    'template_id': self.template_id
                }
                
                results['successful'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Error processing {record.get('student_name')}: {str(e)}")
        
        return results
    
    def _generate_pdf(self, template, record) -> bytes:
        """Generate single PDF"""
        output = io.BytesIO()
        self.generator.generate(
            output_path=output,
            background_image=template.background_image,
            template_json=template.template_json,
            data=record
        )
        output.seek(0)
        return output.read()
