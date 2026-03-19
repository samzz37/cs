"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from . import models, schemas
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCRUD:
    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate):
        """Create a new user"""
        hashed_password = pwd_context.hash(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            password_hash=hashed_password,
            full_name=user.full_name,
            role=user.role,
            department=user.department
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user(db: Session, user_id: int):
        """Get user by ID"""
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """Get user by email"""
        return db.query(models.User).filter(models.User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        """Get user by username"""
        return db.query(models.User).filter(models.User.username == username).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        """Get all users"""
        return db.query(models.User).offset(skip).limit(limit).all()
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def update_last_login(db: Session, user_id: int):
        """Update user's last login time"""
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.last_login = datetime.utcnow()
            db.commit()
        return user

class TemplateCRUD:
    @staticmethod
    def create_template(db: Session, template: schemas.TemplateCreate, user_id: int):
        """Create a new template"""
        db_template = models.Template(
            name=template.name,
            description=template.description,
            created_by=user_id,
            orientation=template.orientation,
            width=template.width,
            height=template.height,
            template_json=template.template_json
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        return db_template
    
    @staticmethod
    def get_template(db: Session, template_id: int):
        """Get template by ID"""
        return db.query(models.Template).filter(models.Template.id == template_id).first()
    
    @staticmethod
    def get_all_templates(db: Session, skip: int = 0, limit: int = 100):
        """Get all active templates"""
        return db.query(models.Template).filter(
            models.Template.is_active == True
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_template(db: Session, template_id: int, update_data: schemas.TemplateUpdate):
        """Update template"""
        db_template = db.query(models.Template).filter(models.Template.id == template_id).first()
        if db_template:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(db_template, key, value)
            db.commit()
            db.refresh(db_template)
        return db_template
    
    @staticmethod
    def delete_template(db: Session, template_id: int):
        """Soft delete template"""
        db_template = db.query(models.Template).filter(models.Template.id == template_id).first()
        if db_template:
            db_template.is_active = False
            db.commit()
        return db_template

class CertificateCRUD:
    @staticmethod
    def create_certificate(db: Session, cert: schemas.CertificateCreate, user_id: int):
        """Create a new certificate"""
        import uuid
        cert_number = f"CERT-{uuid.uuid4().hex[:10].upper()}"
        
        db_cert = models.Certificate(
            certificate_number=cert_number,
            template_id=cert.template_id,
            student_name=cert.student_name,
            student_id=cert.student_id,
            student_email=cert.student_email,
            department=cert.department,
            course=cert.course,
            marks=cert.marks,
            grade=cert.grade,
            achievement_title=cert.achievement_title,
            issue_date=cert.issue_date,
            expiry_date=cert.expiry_date,
            generated_by=user_id,
            status=models.CertificateStatus.draft
        )
        db.add(db_cert)
        db.commit()
        db.refresh(db_cert)
        return db_cert
    
    @staticmethod
    def get_certificate(db: Session, cert_id: int):
        """Get certificate by ID"""
        return db.query(models.Certificate).filter(models.Certificate.id == cert_id).first()
    
    @staticmethod
    def get_certificates(db: Session, skip: int = 0, limit: int = 100):
        """Get all certificates"""
        return db.query(models.Certificate).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_certificates_by_template(db: Session, template_id: int, skip: int = 0, limit: int = 100):
        """Get certificates by template"""
        return db.query(models.Certificate).filter(
            models.Certificate.template_id == template_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_certificate_status(db: Session, cert_id: int, status: str):
        """Update certificate status"""
        db_cert = db.query(models.Certificate).filter(models.Certificate.id == cert_id).first()
        if db_cert:
            db_cert.status = status
            db.commit()
            db.refresh(db_cert)
        return db_cert
    
    @staticmethod
    def get_certificates_today(db: Session) -> int:
        """Count certificates generated today"""
        today = datetime.utcnow().date()
        return db.query(models.Certificate).filter(
            models.Certificate.created_at >= datetime.combine(today, datetime.min.time())
        ).count()

class RankingCRUD:
    @staticmethod
    def create_ranking(db: Session, ranking: schemas.RankingCreate):
        """Create a new ranking"""
        db_ranking = models.Ranking(**ranking.dict())
        db.add(db_ranking)
        db.commit()
        db.refresh(db_ranking)
        return db_ranking
    
    @staticmethod
    def get_rankings_by_event(db: Session, event: str, academic_year: str, skip: int = 0, limit: int = 100):
        """Get rankings by event and year"""
        return db.query(models.Ranking).filter(
            and_(
                models.Ranking.event == event,
                models.Ranking.academic_year == academic_year
            )
        ).order_by(desc(models.Ranking.marks)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_rankings_by_department(db: Session, department: str, skip: int = 0, limit: int = 100):
        """Get rankings by department"""
        return db.query(models.Ranking).filter(
            models.Ranking.department == department
        ).order_by(desc(models.Ranking.marks)).offset(skip).limit(limit).all()
    
    @staticmethod
    def bulk_create_rankings(db: Session, rankings: list):
        """Bulk create rankings and assign positions"""
        db_rankings = []
        for rank, ranking_data in enumerate(rankings, 1):
            ranking_obj = models.Ranking(
                **ranking_data.dict(),
                rank_position=rank
            )
            db_rankings.append(ranking_obj)
        db.add_all(db_rankings)
        db.commit()
        return db_rankings

class ActivityLogCRUD:
    @staticmethod
    def create_log(db: Session, log: schemas.ActivityLogCreate):
        """Create activity log"""
        db_log = models.ActivityLog(**log.dict())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    @staticmethod
    def get_logs(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
        """Get activity logs"""
        query = db.query(models.ActivityLog)
        if user_id:
            query = query.filter(models.ActivityLog.user_id == user_id)
        return query.order_by(desc(models.ActivityLog.created_at)).offset(skip).limit(limit).all()

class SystemLogCRUD:
    @staticmethod
    def create_log(db: Session, log: schemas.SystemLogCreate):
        """Create system log"""
        db_log = models.SystemLog(**log.dict())
        db.add(db_log)
        db.commit()
        return db_log
    
    @staticmethod
    def get_logs(db: Session, module: str = None, skip: int = 0, limit: int = 100):
        """Get system logs"""
        query = db.query(models.SystemLog)
        if module:
            query = query.filter(models.SystemLog.module == module)
        return query.order_by(desc(models.SystemLog.timestamp)).offset(skip).limit(limit).all()
