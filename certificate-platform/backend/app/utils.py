"""
Utility functions for certificate generation, monitoring, and exports
"""
import qrcode
from io import BytesIO
import json
from datetime import datetime
from typing import Optional, List, Dict

class QRCodeGenerator:
    """Generate QR codes for certificates"""
    
    @staticmethod
    def generate(data: str, size: int = 5) -> bytes:
        """Generate QR code and return as bytes"""
        qr = qrcode.QRCode(version=1, box_size=size, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()

class CertificateNumberGenerator:
    """Generate unique certificate numbers"""
    
    @staticmethod
    def generate(template_id: int, student_id: str) -> str:
        """Generate certificate number"""
        import uuid
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        unique_id = uuid.uuid4().hex[:8].upper()
        return f"CERT-{timestamp}-{unique_id}"

class DateHelper:
    """Date utility functions"""
    
    @staticmethod
    def add_days(base_date: datetime, days: int) -> datetime:
        """Add days to date"""
        from datetime import timedelta
        return base_date + timedelta(days=days)
    
    @staticmethod
    def is_expired(expiry_date: datetime) -> bool:
        """Check if certificate is expired"""
        return datetime.utcnow() > expiry_date

class FieldParser:
    """Parse template fields"""
    
    @staticmethod
    def replace_fields(template_json: str, data: dict) -> str:
        """Replace template fields with actual data"""
        template = json.loads(template_json)
        
        for key, value in data.items():
            template_str = json.dumps(template)
            template_str = template_str.replace(f"{{{{{key}}}}}", str(value))
            template = json.loads(template_str)
        
        return json.dumps(template)
    
    @staticmethod
    def get_fields(template_json: str) -> List[str]:
        """Extract field names from template"""
        import re
        fields = re.findall(r'\{\{(\w+)\}\}', template_json)
        return list(set(fields))

class ValidationHelper:
    """Validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number"""
        import re
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None

class FileHelper:
    """File handling utilities"""
    
    @staticmethod
    def save_file(content: bytes, filename: str, directory: str) -> str:
        """Save file and return path"""
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write(content)
        return filepath
    
    @staticmethod
    def read_file(filepath: str) -> bytes:
        """Read file content"""
        with open(filepath, 'rb') as f:
            return f.read()

class SystemMonitor:
    """System monitoring utilities"""
    
    @staticmethod
    def get_system_stats() -> dict:
        """Get system statistics"""
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_usage': cpu_percent,
            'memory_usage': memory.percent,
            'memory_total_gb': memory.total / (1024 ** 3),
            'memory_available_gb': memory.available / (1024 ** 3),
            'disk_usage': disk.percent,
            'disk_total_gb': disk.total / (1024 ** 3),
            'disk_free_gb': disk.free / (1024 ** 3)
        }
    
    @staticmethod
    def get_process_info() -> dict:
        """Get current process information"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        return {
            'pid': process.pid,
            'memory_mb': process.memory_info().rss / (1024 ** 2),
            'cpu_percent': process.cpu_percent(),
            'num_threads': process.num_threads()
        }

class SMSHelper:
    """SMS notification utilities"""
    
    @staticmethod
    def format_alert_message(alert_type: str, title: str, message: str, timestamp: str = None) -> str:
        """Format SMS alert message"""
        if not timestamp:
            timestamp = datetime.utcnow().strftime("%H:%M")
        
        return f"""CERTIFICATE SYSTEM ALERT
{title}
{message}
Time: {timestamp}"""
    
    @staticmethod
    def validate_phone_numbers(phone_numbers: str) -> List[str]:
        """Validate and parse phone numbers from comma-separated string"""
        phones = [p.strip() for p in phone_numbers.split(',') if p.strip()]
        return [p for p in phones if ValidationHelper.validate_phone(p)]
