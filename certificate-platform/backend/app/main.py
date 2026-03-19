"""
Main FastAPI application and WebSocket handling
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Set, TYPE_CHECKING
import uuid
import os
import io
import sys
from pathlib import Path

if TYPE_CHECKING:
    from certificate_engine.generator import CertificateGenerator, CertificateBulkGenerator
    from exports.exporter import RankingExporter, CertificateReportExporter

from .database import get_db, engine, Base
from . import models, schemas, crud
from .auth import create_access_token, verify_token
from .utils import QRCodeGenerator, CertificateNumberGenerator, SystemMonitor

# Add parent directory to path for importing certificate-engine and exports modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Certificate Management System",
    description="Real-time certificate management and monitoring",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[int, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str, user_id: int):
        """Connect WebSocket client"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = set()
        self.user_sessions[user_id].add(session_id)
    
    def disconnect(self, session_id: str, user_id: int):
        """Disconnect WebSocket client"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        
        if user_id in self.user_sessions:
            self.user_sessions[user_id].discard(session_id)
            if not self.user_sessions[user_id]:
                del self.user_sessions[user_id]
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections.values():
            try:
                await connection.send_json(message)
            except Exception:
                pass
    
    async def send_personal(self, session_id: str, message: dict):
        """Send message to specific session"""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)
    
    def get_active_user_count(self) -> int:
        """Get count of active users"""
        return len(self.user_sessions)

manager = ConnectionManager()

# ==================== Authentication Routes ====================

@app.post("/api/auth/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing = crud.UserCRUD.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = crud.UserCRUD.create_user(db, user)
    return db_user

@app.post("/api/auth/login", response_model=schemas.TokenResponse)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Login user"""
    user = crud.UserCRUD.get_user_by_username(db, credentials.username)
    
    if not user or not crud.UserCRUD.verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update last login
    crud.UserCRUD.update_last_login(db, user.id)
    
    # Create token
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username, "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/api/auth/me", response_model=schemas.UserResponse)
def get_current_user(token: str = None, db: Session = Depends(get_db)):
    """Get current user"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = crud.UserCRUD.get_user(db, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# ==================== Dashboard Routes ====================

@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    certs_today = crud.CertificateCRUD.get_certificates_today(db)
    active_users = manager.get_active_user_count()
    total_templates = db.query(models.Template).filter(models.Template.is_active == True).count()
    total_certificates = db.query(models.Certificate).count()
    
    # System stats
    sys_stats = SystemMonitor.get_system_stats()
    
    return {
        "certificates_today": certs_today,
        "active_users": active_users,
        "total_templates": total_templates,
        "total_certificates": total_certificates,
        "cpu_usage": sys_stats['cpu_usage'],
        "memory_usage": sys_stats['memory_usage'],
        "disk_usage": sys_stats['disk_usage']
    }

@app.get("/api/dashboard/activity-logs")
def get_activity_logs(limit: int = 50, db: Session = Depends(get_db)):
    """Get recent activity logs"""
    logs = crud.ActivityLogCRUD.get_logs(db, skip=0, limit=limit)
    return logs

# ==================== Template Routes ====================

@app.post("/api/templates", response_model=schemas.TemplateResponse)
def create_template(
    template: schemas.TemplateCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new template"""
    db_template = crud.TemplateCRUD.create_template(db, template, user_id)
    return db_template

@app.get("/api/templates", response_model=List[schemas.TemplateResponse])
def list_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all templates"""
    templates = crud.TemplateCRUD.get_all_templates(db, skip, limit)
    return templates

@app.get("/api/templates/{template_id}", response_model=schemas.TemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    """Get template by ID"""
    template = crud.TemplateCRUD.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@app.put("/api/templates/{template_id}", response_model=schemas.TemplateResponse)
def update_template(
    template_id: int,
    update: schemas.TemplateUpdate,
    db: Session = Depends(get_db)
):
    """Update template"""
    template = crud.TemplateCRUD.update_template(db, template_id, update)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@app.post("/api/templates/{template_id}/upload-background")
async def upload_background(
    template_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload background image for template"""
    template = crud.TemplateCRUD.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    content = await file.read()
    template.background_image = content
    template.background_filename = file.filename
    db.commit()
    
    return {"filename": file.filename, "message": "Background uploaded successfully"}

# ==================== Certificate Routes ====================

@app.post("/api/certificates", response_model=schemas.CertificateResponse)
def create_certificate(
    cert: schemas.CertificateCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new certificate"""
    db_cert = crud.CertificateCRUD.create_certificate(db, cert, user_id)
    return db_cert

@app.get("/api/certificates", response_model=List[schemas.CertificateResponse])
def list_certificates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all certificates"""
    certificates = crud.CertificateCRUD.get_certificates(db, skip, limit)
    return certificates

@app.get("/api/certificates/{cert_id}", response_model=schemas.CertificateResponse)
def get_certificate(cert_id: int, db: Session = Depends(get_db)):
    """Get certificate by ID"""
    cert = crud.CertificateCRUD.get_certificate(db, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert

@app.post("/api/certificates/{cert_id}/generate")
def generate_certificate(cert_id: int, db: Session = Depends(get_db)):
    """Generate certificate PDF"""
    from certificate_engine.generator import CertificateGenerator
    
    cert = crud.CertificateCRUD.get_certificate(db, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    # Generate PDF
    output_dir = "generated_certificates"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{cert.certificate_number}.pdf")
    
    generator = CertificateGenerator()
    generator.generate(filepath)
    
    # Update certificate
    cert.certificate_path = filepath
    cert.status = models.CertificateStatus.generated
    db.commit()
    
    return {"message": "Certificate generated", "path": filepath}

@app.post("/api/certificates/bulk-upload")
async def bulk_upload(
    template_id: int = Form(...),
    file: UploadFile = File(...),
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Upload bulk certificates"""
    import pandas as pd
    
    job_id = str(uuid.uuid4())
    
    # Create bulk upload job
    bulk_job = models.BulkUploadJob(
        job_id=job_id,
        uploaded_by=user_id,
        template_id=template_id,
        file_name=file.filename,
        status=models.JobStatus.pending
    )
    db.add(bulk_job)
    db.commit()
    
    # Read Excel file
    file_content = await file.read()
    df = pd.read_excel(io.BytesIO(file_content))
    
    bulk_job.total_records = len(df)
    db.commit()
    
    # Process in background
    asyncio.create_task(process_bulk_certificates(job_id, df, template_id, user_id, db))
    
    return {"job_id": job_id, "message": "Bulk upload started"}

# ==================== Ranking Routes ====================

@app.post("/api/rankings/import")
def import_rankings(rankings: List[schemas.RankingCreate], db: Session = Depends(get_db)):
    """Import rankings from CSV/Excel"""
    # Sort by marks
    sorted_rankings = sorted(rankings, key=lambda x: x.marks, reverse=True)
    
    # Create ranking objects with positions
    db_rankings = []
    for position, ranking in enumerate(sorted_rankings, 1):
        ranking_dict = ranking.dict()
        ranking_dict['rank_position'] = position
        db_ranking = models.Ranking(**ranking_dict)
        db_rankings.append(db_ranking)
    
    db.add_all(db_rankings)
    db.commit()
    
    return {"message": f"Imported {len(db_rankings)} rankings"}

@app.get("/api/rankings/event/{event}")
def get_rankings_by_event(
    event: str,
    year: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get rankings by event"""
    rankings = crud.RankingCRUD.get_rankings_by_event(db, event, year, skip, limit)
    return rankings

@app.get("/api/rankings/department/{department}")
def get_rankings_by_department(
    department: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get rankings by department"""
    rankings = crud.RankingCRUD.get_rankings_by_department(db, department, skip, limit)
    return rankings

# ==================== Export Routes ====================

@app.get("/api/export/rankings/{format_type}")
def export_rankings(format_type: str, db: Session = Depends(get_db)):
    """Export rankings in various formats"""
    from exports.exporter import RankingExporter
    
    rankings = db.query(models.Ranking).all()
    exporter = RankingExporter([r.__dict__ for r in rankings])
    
    os.makedirs("exports", exist_ok=True)
    
    if format_type == "pdf":
        filepath = exporter.export_pdf("exports/rankings.pdf")
    elif format_type == "excel":
        filepath = exporter.export_excel("exports/rankings.xlsx")
    elif format_type == "csv":
        filepath = exporter.export_csv("exports/rankings.csv")
    elif format_type == "word":
        filepath = exporter.export_word("exports/rankings.docx")
    else:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    return FileResponse(filepath, media_type='application/octet-stream')

@app.get("/api/export/certificates/{format_type}")
def export_certificates(format_type: str, db: Session = Depends(get_db)):
    """Export certificates in various formats"""
    from exports.exporter import CertificateReportExporter
    
    certificates = db.query(models.Certificate).all()
    exporter = CertificateReportExporter([c.__dict__ for c in certificates])
    
    os.makedirs("exports", exist_ok=True)
    
    if format_type == "pdf":
        filepath = exporter.export_pdf("exports/certificates.pdf")
    elif format_type == "excel":
        filepath = exporter.export_excel("exports/certificates.xlsx")
    elif format_type == "csv":
        filepath = exporter.export_csv("exports/certificates.csv")
    elif format_type == "word":
        filepath = exporter.export_word("exports/certificates.docx")
    else:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    return FileResponse(filepath, media_type='application/octet-stream')

# ==================== Monitoring Routes ====================

@app.get("/api/monitoring/system")
def get_system_monitoring():
    """Get real-time system monitoring data"""
    stats = SystemMonitor.get_system_stats()
    return stats

@app.get("/api/monitoring/active-users")
def get_active_users(db: Session = Depends(get_db)):
    """Get active users"""
    users = db.query(models.OnlineUser).all()
    return [
        {
            "user_id": user.user_id,
            "session_id": user.session_id,
            "current_page": user.current_page,
            "login_time": user.login_time,
            "last_activity": user.last_activity
        }
        for user in users
    ]

# ==================== WebSocket Routes ====================

@app.websocket("/ws/monitoring/{user_id}")
async def websocket_monitoring(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    """WebSocket for real-time monitoring"""
    session_id = str(uuid.uuid4())
    
    try:
        await manager.connect(websocket, session_id, user_id)
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Broadcast to all clients
            await manager.broadcast({
                "type": message.get("type"),
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Handle system monitoring update
            if message.get("type") == "monitoring":
                stats = SystemMonitor.get_system_stats()
                await manager.broadcast({
                    "type": "system_stats",
                    "data": stats,
                    "timestamp": datetime.utcnow().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(session_id, user_id)

@app.websocket("/ws/live-session/{target_user_id}")
async def websocket_live_session(
    websocket: WebSocket,
    target_user_id: int,
    admin_id: int = None
):
    """WebSocket for live session monitoring"""
    session_id = str(uuid.uuid4())
    
    try:
        await manager.connect(websocket, session_id, admin_id or target_user_id)
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Send to specific user's sessions
            if target_user_id in manager.user_sessions:
                for target_session in manager.user_sessions[target_user_id]:
                    await manager.send_personal(target_session, {
                        "type": "session_update",
                        "data": message
                    })
    
    except WebSocketDisconnect:
        manager.disconnect(session_id, admin_id or target_user_id)

# ==================== Health Check ====================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# ==================== Background Tasks ====================

async def process_bulk_certificates(job_id: str, df, template_id: int, user_id: int, db: Session):
    """Process bulk certificate generation"""
    from certificate_engine.generator import CertificateBulkGenerator
    
    job = db.query(models.BulkUploadJob).filter(
        models.BulkUploadJob.job_id == job_id
    ).first()
    
    if job:
        job.status = models.JobStatus.processing
        db.commit()
        
        try:
            generator = CertificateBulkGenerator(template_id, db)
            results = generator.process_batch(df.to_dict("records"), "generated_certificates")
            
            job.processed_records = len(df)
            job.successful_records = results['successful']
            job.failed_records = results['failed']
            job.status = models.JobStatus.completed
            job.completed_at = datetime.utcnow()
            
            if results['errors']:
                job.error_message = "\n".join(results['errors'])
            
        except Exception as e:
            job.status = models.JobStatus.failed
            job.error_message = str(e)
        
        db.commit()
        
        await manager.broadcast({
            "type": "bulk_upload_complete",
            "job_id": job_id,
            "status": job.status
        })
