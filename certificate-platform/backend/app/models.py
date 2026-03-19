"""
SQLAlchemy models for all database tables
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, LargeBinary, Enum, Numeric, ForeignKey, Date, Timestamp
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    student = "student"

class CertificateStatus(str, enum.Enum):
    draft = "draft"
    generated = "generated"
    issued = "issued"
    downloaded = "downloaded"

class AlertType(str, enum.Enum):
    error = "error"
    warning = "warning"
    info = "info"
    success = "success"

class AlertSeverity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class JobStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Orientation(str, enum.Enum):
    portrait = "portrait"
    landscape = "landscape"

class LogLevel(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.student)
    department = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    templates = relationship("Template", back_populates="creator")
    certificates = relationship("Certificate", back_populates="generator")

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    orientation = Column(Enum(Orientation), default=Orientation.landscape)
    width = Column(Numeric(10, 2))
    height = Column(Numeric(10, 2))
    background_image = Column(LargeBinary)
    background_filename = Column(String(255))
    template_json = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = relationship("User", back_populates="templates")
    certificates = relationship("Certificate", back_populates="template")

class Certificate(Base):
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    certificate_number = Column(String(50), unique=True, index=True, nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    student_name = Column(String(255), nullable=False)
    student_id = Column(String(100))
    student_email = Column(String(255), index=True)
    department = Column(String(255))
    course = Column(String(255))
    marks = Column(Numeric(10, 2))
    grade = Column(String(10))
    achievement_title = Column(String(255))
    issue_date = Column(Date)
    expiry_date = Column(Date)
    qr_code = Column(String(500))
    certificate_path = Column(String(500))
    certificate_data = Column(LargeBinary)
    status = Column(Enum(CertificateStatus), default=CertificateStatus.draft, index=True)
    generated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    template = relationship("Template", back_populates="certificates")
    generator = relationship("User", back_populates="certificates")

class Ranking(Base):
    __tablename__ = "rankings"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    student_name = Column(String(255), nullable=False)
    student_email = Column(String(255))
    department = Column(String(255), index=True)
    event = Column(String(255), index=True)
    academic_year = Column(String(10), index=True)
    marks = Column(Numeric(10, 2), nullable=False, index=True)
    rank_position = Column(Integer, index=True)
    grade = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(255), nullable=False)
    module = Column(String(100))
    description = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    status = Column(String(50), default="success")
    affected_record = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    log_level = Column(Enum(LogLevel), default=LogLevel.INFO, index=True)
    module = Column(String(100), index=True)
    message = Column(Text, nullable=False)
    error_details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(Enum(AlertType), default=AlertType.warning, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.medium)
    phone_numbers = Column(String(500))
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class OnlineUser(Base):
    __tablename__ = "online_users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String(255), unique=True, nullable=False)
    current_page = Column(String(500))
    login_time = Column(DateTime, default=datetime.utcnow, index=True)
    last_activity = Column(DateTime)

class BulkUploadJob(Base):
    __tablename__ = "bulk_upload_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), unique=True, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    file_name = Column(String(255))
    total_records = Column(Integer)
    processed_records = Column(Integer, default=0)
    successful_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)
    status = Column(Enum(JobStatus), default=JobStatus.pending, index=True)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime)

class Setting(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, index=True, nullable=False)
    setting_value = Column(Text)
    description = Column(Text)
    data_type = Column(String(50), default="string")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
