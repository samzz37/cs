# Certificate Management System - CertHub

A comprehensive **real-time certificate management and monitoring system** for educational institutions. Designed for the Computer Science Department with features for certificate template design, bulk generation, student ranking, and live system monitoring.

## 🎯 Key Features

### 📜 Certificate Management
- **Template Designer**: Drag-and-drop visual certificate editor using Fabric.js
- **Dynamic Templates**: Support portrait and landscape orientations
- **QR Code Generation**: Auto-generate unique QR codes for each certificate
- **Bulk Generation**: Import Excel/CSV files to generate certificates in batch
- **Multiple Export Formats**: PDF, Word, Excel, CSV

### 👥 User Management
- **Role-Based Access**: Admin, Staff, and Student roles
- **Secure Authentication**: JWT-based token authentication
- **Session Management**: Track active users and their activities
- **Activity Logging**: Comprehensive audit trail of all operations

### 🏆 Merit Ranking System
- **Student Rankings**: Sort and rank students by marks
- **Department Filtering**: View rankings by department
- **Event-based Rankings**: Organize by events and academic years
- **Rank Visualization**: Top performers highlighting

### 🔍 Real-Time Monitoring
- **System Health**: Monitor CPU, memory, and disk usage
- **Active User Tracking**: See who's online and what they're doing
- **Live Dashboard**: Real-time statistics and charts
- **WebSocket Updates**: Live streaming of system data
- **Alert System**: SMS notifications for critical events

### 📊 Advanced Features
- **Data Export**: Generate reports in PDF, Excel, Word, CSV formats
- **Admin Settings**: Configure SMS alerts, themes, timeouts
- **Dark Mode**: Professional light and dark theme support
- **Responsive Design**: Works on Windows and Android browsers
- **Server Monitoring**: Track system resources and performance

## 🏗️ System Architecture

### Technology Stack

**Frontend:**
- React 18 + Vite
- Tailwind CSS (responsive design)
- Recharts (data visualization)
- Chart.js (advanced charts)
- Fabric.js (canvas-based template editor)
- WebSocket (real-time updates)

**Backend:**
- FastAPI (Python web framework)
- PostgreSQL/MySQL (database)
- SQLAlchemy (ORM)
- ReportLab (PDF generation)
- Pillow (image processing)
- psutil (system monitoring)

**Key Libraries:**
- python-docx (Word generation)
- Pandas (data processing)
- qrcode (QR code generation)
- WebSockets (real-time communication)

## 📁 Project Structure

```
certificate-platform/
├── frontend/                 # React Vite application
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── context/         # Zustand store
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # API and utilities
│   │   └── styles/          # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py          # Main FastAPI app
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # Database operations
│   │   ├── auth.py          # Authentication
│   │   ├── utils.py         # Utilities
│   │   ├── database.py      # DB connection
│   │   └── ws/              # WebSocket handlers
│   ├── requirements.txt
│   └── asgi.py
│
├── certificate-engine/      # Certificate generation
│   └── generator.py
│
├── exports/                 # Export utilities
│   └── exporter.py
│
├── monitoring/              # System monitoring
│   └── monitor.py
│
├── database/                # Database schema
│   └── schema.sql
│
├── configs/                 # Configuration files
│   └── .env.example
│
└── scripts/                 # Setup and utility scripts
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MySQL 5.7+ (or PostgreSQL)
- Git

### Installation

1. **Clone Repository**
```bash
cd certificate-platform
```

2. **Run Setup Script**

Windows:
```bash
setup.bat
```

Linux/Mac:
```bash
bash setup.sh
```

3. **Configure Environment**

Update `backend/.env`:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/CS
SECRET_KEY=your-secret-key-here
```

4. **Start Services**

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

5. **Access Application**

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Default Login: admin / admin123

## 📚 API Documentation

Complete API documentation available at:
```
http://localhost:8000/docs
```

### Key Endpoints

**Authentication:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

**Certificates:**
- `GET /api/certificates` - List certificates
- `POST /api/certificates` - Create certificate
- `POST /api/certificates/{id}/generate` - Generate PDF
- `POST /api/certificates/bulk-upload` - Bulk upload

**Templates:**
- `GET /api/templates` - List templates
- `POST /api/templates` - Create template
- `POST /api/templates/{id}/upload-background` - Upload background

**Rankings:**
- `GET /api/rankings/event/{event}` - Get event rankings
- `GET /api/rankings/department/{dept}` - Get department rankings
- `POST /api/rankings/import` - Import rankings

**Monitoring:**
- `GET /api/monitoring/system` - System stats
- `GET /api/monitoring/active-users` - Active users
- `WS /ws/monitoring/{user_id}` - Real-time monitoring

**Exports:**
- `GET /api/export/rankings/{format}` - Export rankings
- `GET /api/export/certificates/{format}` - Export certificates

## 🔐 Security

- JWT Authentication with token expiration
- Bcrypt password hashing
- SQL injection prevention (SQLAlchemy + parameterized queries)
- CORS configuration
- Rate limiting support
- Environment variable secrets management

## 📱 Browser Compatibility

- ✅ Chrome/Edge (Windows)
- ✅ Firefox (Windows)
- ✅ Safari (Windows/Mac)
- ✅ Chrome (Android)
- ✅ Firefox (Android)
- ✅ Samsung Internet (Android)

## 📊 Database Schema

### Main Tables
- **users** - User accounts and authentication
- **templates** - Certificate templates
- **certificates** - Generated certificates
- **rankings** - Student merit rankings
- **activity_logs** - User activity tracking
- **system_logs** - System event logs
- **alerts** - System alerts and notifications
- **online_users** - Active user sessions
- **bulk_upload_jobs** - Bulk generation jobs

## 🐳 Docker Deployment

Build and run with Docker:

```bash
docker-compose up -d
```

Access at: `http://localhost`

## 📝 Configuration

### Environment Variables

```env
# Database
DATABASE_URL=mysql+pymysql://user:pass@host:3306/CS

# Security
SECRET_KEY=change-this-in-production
ALGORITHM=HS256

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# File Upload
MAX_UPLOAD_SIZE_MB=100
UPLOAD_DIR=uploads

# SMS Alerts
SMS_ENABLED=False
SMS_API_KEY=your-key
SMS_FROM_NUMBER=+1234567890

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 🚢 Production Deployment

### Using Gunicorn
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Nginx Configuration
See `SETUP_GUIDE.md` for complete Nginx setup

### Database Backup
```bash
mysqldump -u root -p CS > backup.sql
```

## 🧪 Testing

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📊 Performance Optimization

- Database connection pooling
- Caching with Redis (optional)
- CDN for static assets
- API response compression
- Lazy loading for images
- Code splitting in React

## 🛠️ Maintenance

### Regular Tasks
- Monitor system logs (`logs/app.log`)
- Check database size and performance
- Review activity logs for suspicious activity
- Backup database regularly
- Update dependencies monthly
- Clear old generated files

### Health Check
```bash
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

**Issue:** Database connection failed
```bash
# Check MySQL is running
mysql -u root -p
# Verify DATABASE_URL in .env
```

**Issue:** Port 8000/5173 already in use
```bash
# Use different port
python -m uvicorn app.main:app --port 8001
npm run dev -- --port 3000
```

**Issue:** Module not found errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
npm install --legacy-peer-deps
```

## 📄 License

This project is proprietary and confidential for the Computer Science Department.

## 👥 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support

For issues and feature requests, please contact:
- Admin: admin@example.com
- Technical Support: support@example.com

---

**Version:** 1.0.0  
**Last Updated:** March 19, 2026  
**Maintained By:** Development Team  
**Status:** Production Ready ✅
