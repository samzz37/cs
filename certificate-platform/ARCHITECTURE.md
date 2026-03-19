# System Architecture Documentation

## High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE (WEB)                          │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   Desktop    │  │   Tablet     │  │  Mobile/     │               │
│  │   Browser    │  │  Browser     │  │   Android    │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│         │                  │                  │                       │
│         └──────────────────┼──────────────────┘                       │
│                            │                                          │
└────────────────────────────┼──────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   HTTP/HTTPS    │
                    │   REST API      │
                    │   WebSocket     │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼──────────┐ ┌──────▼───────┐ ┌───────────▼───────┐
│   REACT FRONTEND │ │  VITE BUILD  │ │  TAILWIND CSS     │
│                  │ │   TOOL       │ │  STATE MGMT       │
│  • Dashboard     │ │              │ │  (ZUSTAND)        │
│  • Templates     │ │  npm run dev │ │                   │
│  • Certificates  │ │  (5173)      │ │  • Auth Store     │
│  • Rankings      │ │              │ │  • Dashboard      │
│  • Monitoring    │ │  npm build   │ │  • Certificates   │
│  • Settings      │ │              │ │  • Monitoring     │
└──────────────────┘ └──────────────┘ └───────────────────┘
        (SPA)
        │
        └────────────────────┬─────────────────────┬──────────────┐
                             │                     │              │
                    ┌────────▼──────────┐  ┌──────▼────┐  ┌──────▼────┐
                    │  REST API Calls   │  │ WS Events │  │   File    │
                    │  (Axios)          │  │ Upload    │  │   Upload  │
                    └───────────────────┘  └───────────┘  └───────────┘
                             │
        ┌────────────────────┼─────────────────────────────────┐
        │                    │                                 │
┌───────▼─────────────────────▼───────────────────────────────▼──────┐
│                     FASTAPI BACKEND SERVER                           │
│                     (Python, uvicorn, 8000)                          │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  ROUTING LAYER                                             │    │
│  │  ├─ /api/auth/* - Authentication                          │    │
│  │  ├─ /api/templates/* - Template management                │    │
│  │  ├─ /api/certificates/* - Certificate operations          │    │
│  │  ├─ /api/rankings/* - Merit rankings                      │    │
│  │  ├─ /api/monitoring/* - System monitoring                 │    │
│  │  ├─ /api/export/* - Data export                           │    │
│  │  ├─ /api/dashboard/* - Dashboard stats                    │    │
│  │  └─ /ws/* - WebSocket connections                         │    │
│  └────────────────────────────────────────────────────────────┘    │
│                            │                                         │
│  ┌─────────────────────────▼────────────────────────────────┐      │
│  │  BUSINESS LOGIC LAYER                                    │      │
│  │  ├─ CRUD Operations (crud.py)                            │      │
│  │  ├─ Authentication & JWT (auth.py)                       │      │
│  │  ├─ Data Validation (schemas.py)                         │      │
│  │  ├─ Utility Functions (utils.py)                         │      │
│  │  └─ WebSocket Management                                 │      │
│  └─────────────────────────┬─────────────────────────────────┘     │
│                            │                                         │
│  ┌─────────────────────────▼────────────────────────────────┐      │
│  │  MODULE LAYER                                             │      │
│  │  ├─ Certificate Generator (ReportLab)                    │      │
│  │  ├─ Export Manager (PDF/Excel/Word/CSV)                  │      │
│  │  ├─ Monitoring Service (psutil)                          │      │
│  │  └─ Ranking Processor                                    │      │
│  └─────────────────────────┬─────────────────────────────────┘     │
│                            │                                         │
│  ┌─────────────────────────▼────────────────────────────────┐      │
│  │  DATA LAYER (SQLAlchemy ORM)                             │      │
│  │  └─ models.py (11 SQLAlchemy Models)                     │      │
│  └─────────────────────────┬─────────────────────────────────┘     │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
        ┌────────────────────┼─────────────────────┐
        │                    │                    │
┌───────▼──────────┐ ┌──────▼───────┐ ┌───────────▼──────────┐
│                  │ │              │ │                      │
│  MYSQL DATABASE  │ │ FILE STORAGE │ │ SYSTEM RESOURCES     │
│                  │ │              │ │                      │
│  • users         │ │ • Uploads    │ │ • CPU              │
│  • templates     │ │ • Certs      │ │ • Memory           │
│  • certificates  │ │ • Exports    │ │ • Disk             │
│  • rankings      │ │ • Logs       │ │ • Network          │
│  • activity_logs │ │              │ │                    │
│  • system_logs   │ │              │ │                    │
│  • alerts        │ │              │ │                    │
│  • settings      │ │              │ │                    │
│  • online_users  │ │              │ │                    │
│                  │ │              │ │                    │
└──────────────────┘ └──────────────┘ └────────────────────┘
```

## Component Interaction Flow

### 1. Authentication Flow
```
Client Login
    │
    ├─→ POST /api/auth/login
    │
    ├─→ Backend: Verify credentials
    │
    ├─→ Generate JWT token
    │
    └─→ Return {token, user}
    │
    ├─→ Frontend: Store token in localStorage
    │
    └─→ Include token in all API requests
```

### 2. Certificate Generation Flow
```
User submits form
    │
    ├─→ POST /api/certificates (create draft)
    │
    ├─→ POST /api/certificates/{id}/generate (generate PDF)
    │
    ├─→ Backend: Load template
    │
    ├─→ Generate QR code
    │
    ├─→ Generate PDF using ReportLab
    │
    ├─→ Save certificate file
    │
    ├─→ Update database
    │
    └─→ Return download link
```

### 3. Bulk Upload Flow
```
User uploads Excel file
    │
    ├─→ POST /api/certificates/bulk-upload
    │
    ├─→ Backend: Create job
    │
    ├─→ Async processing starts
    │   ├─ Read Excel rows
    │   ├─ Validate data
    │   ├─ Generate certificates (parallel)
    │   └─ Update progress
    │
    ├─→ WebSocket broadcasts progress
    │
    └─→ Frontend updates UI in real-time
```

### 4. Real-Time Monitoring Flow
```
Frontend connects to WebSocket
    │
    ├─→ WS /ws/monitoring/{user_id}
    │
    ├─→ Backend: Accept connection
    │
    ├─→ Periodically collect system stats
    │
    ├─→ Send via WebSocket broadcast
    │
    ├─→ Frontend: Update charts in real-time
    │
    └─→ Auto-close on disconnect
```

## Data Model

### User Entity
```
User
├─ id (PK)
├─ username (unique)
├─ email (unique)
├─ password_hash
├─ full_name
├─ role (enum: admin, staff, student)
├─ department
├─ is_active
├─ last_login
├─ created_at
└─ updated_at
```

### Certificate Template Entity
```
Template
├─ id (PK)
├─ name
├─ description
├─ created_by (FK → User)
├─ orientation (portait/landscape)
├─ width, height
├─ background_image (binary)
├─ template_json (canvas data)
├─ is_active
├─ created_at
└─ updated_at
```

### Certificate Entity
```
Certificate
├─ id (PK)
├─ certificate_number (unique)
├─ template_id (FK → Template)
├─ student_name
├─ student_email
├─ student_id
├─ department
├─ course
├─ marks
├─ grade
├─ achievement_title
├─ issue_date
├─ expiry_date
├─ qr_code
├─ certificate_path
├─ certificate_data (binary)
├─ status (enum)
├─ generated_by (FK → User)
├─ created_at
└─ updated_at
```

## Deployment Architecture

### Single Server Deployment
```
┌───────────────────────────────┐
│      Cloud Server/VPS          │
│                               │
│  ┌──────────────────────────┐ │
│  │  Nginx (Reverse Proxy)   │ │
│  │  Port 80, 443            │ │
│  └──────────────────────────┘ │
│         │              │       │
│    ┌────▼────┐   ┌────▼────┐  │
│    │ Frontend│   │ Backend  │  │
│    │ (dist/) │   │(Gunicorn)│  │
│    │Port:80  │   │Port:8000 │  │
│    └─────────┘   └────┬────┘  │
│                       │        │
│    ┌──────────────────▼─────┐  │
│    │  MySQL Database         │  │
│    │  Port: 3306             │  │
│    └─────────────────────────┘  │
│                                │
└───────────────────────────────┘
```

### Containerized Deployment
```
Docker Host
├─ MySQL Container
├─ Backend Container (Gunicorn + Uvicorn)
├─ Frontend Container (Nginx)
└─ Nginx Container (Reverse Proxy)
```

## API Request/Response Flow

### Request Headers
```
GET /api/certificates
Host: api.example.com
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Accept: application/json
```

### Response Format
```
{
  "status": "success",
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
```

## Security Layers

```
┌─────────────────────────────────────┐
│      HTTPS/TLS Encryption           │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│      CORS Validation                │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│      JWT Authentication             │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│      Role-Based Access Control      │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│      Input Validation (Pydantic)    │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│      SQL Injection Prevention       │
│      (SQLAlchemy parameterized)     │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│      Rate Limiting (Optional)       │
└─────────────────────────────────────┘
```

## Monitoring & Logging Architecture

```
┌──────────────────────────────────────────┐
│     System & Application Metrics         │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │  psutil → System Stats            │   │
│  │  (CPU, Memory, Disk, Network)     │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │  Database → Activity Logs         │   │
│  │  (User actions, audit trail)      │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │  File → Application Logs         │   │
│  │  (logs/app.log, rotating)        │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │  WebSocket → Real-time Events    │   │
│  │  (Broadcast to all dashboards)   │   │
│  └──────────────────────────────────┘   │
│                                          │
└──────────────────────────────────────────┘
        │
        └─→ Dashboard: Real-time Display
        └─→ Alerts: SMS/Email Notifications
        └─→ Logs: Historical Analysis
```

---

**Architecture Version**: 1.0.0  
**Last Updated**: March 2026  
**Status**: Production Ready ✅
