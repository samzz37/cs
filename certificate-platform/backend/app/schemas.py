"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

# Base schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = "student"
    department: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    orientation: str = "landscape"
    width: Optional[float] = None
    height: Optional[float] = None


class TemplateCreate(TemplateBase):
    template_json: Optional[str] = None


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    template_json: Optional[str] = None
    is_active: Optional[bool] = None


class TemplateResponse(TemplateBase):
    id: int
    created_by: int
    is_active: bool
    background_filename: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CertificateBase(BaseModel):
    student_name: str
    student_id: Optional[str] = None
    student_email: str
    department: Optional[str] = None
    course: Optional[str] = None
    marks: Optional[float] = None
    grade: Optional[str] = None
    achievement_title: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None


class CertificateCreate(CertificateBase):
    template_id: int


class CertificateResponse(CertificateBase):
    id: int
    certificate_number: str
    template_id: int
    status: str
    qr_code: Optional[str]
    certificate_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RankingBase(BaseModel):
    student_name: str
    student_email: Optional[str] = None
    department: Optional[str] = None
    event: str
    academic_year: str
    marks: float
    grade: Optional[str] = None


class RankingCreate(RankingBase):
    pass


class RankingResponse(RankingBase):
    id: int
    rank_position: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityLogCreate(BaseModel):
    user_id: int
    action: str
    module: Optional[str] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status: str = "success"
    affected_record: Optional[str] = None


class ActivityLogResponse(ActivityLogCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SystemLogCreate(BaseModel):
    log_level: str = "INFO"
    module: str
    message: str
    error_details: Optional[str] = None


class AlertCreate(BaseModel):
    alert_type: str
    title: str
    message: str
    severity: str = "medium"
    phone_numbers: Optional[str] = None


class AlertResponse(AlertCreate):
    id: int
    is_sent: bool
    sent_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class BulkUploadCreate(BaseModel):
    template_id: int
    file_name: str


class BulkUploadResponse(BaseModel):
    id: int
    job_id: str
    template_id: int
    total_records: int
    processed_records: int
    successful_records: int
    failed_records: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    certificates_today: int
    active_users: int
    total_templates: int
    total_certificates: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class OnlineUserResponse(BaseModel):
    id: int
    user_id: int
    session_id: str
    current_page: Optional[str]
    login_time: datetime
    last_activity: Optional[datetime]

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"
    user: UserResponse

    class Config:
        from_attributes = True