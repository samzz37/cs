# Quick Start Guide

## For Windows Users

### Step 1: Install Prerequisites
1. **Python 3.9+**: https://www.python.org/downloads/
2. **Node.js 16+**: https://nodejs.org/
3. **MySQL 8.0**: https://dev.mysql.com/downloads/mysql/

### Step 2: Run Setup
1. Open Command Prompt in the project folder
2. Run: `setup.bat`
3. Follow prompts and update `backend\.env`

### Step 3: Start Application
1. Open two Command Prompt windows
2. **Terminal 1** (Backend):
   ```
   start_backend.bat
   ```
3. **Terminal 2** (Frontend):
   ```
   start_frontend.bat
   ```

### Step 4: Access Application
- Open browser: http://localhost:5173
- Login with: admin / admin123

---

## For Linux/Mac Users

### Step 1: Install Prerequisites
```bash
# Ubuntu/Debian
sudo apt-get install python3.9 python3-pip nodejs npm mysql-server

# Mac (with Homebrew)
brew install python node mysql
```

### Step 2: Run Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Start Application
```bash
# Terminal 1
source backend/venv/bin/activate
python -m uvicorn app.main:app --reload

# Terminal 2
cd frontend
npm run dev
```

### Step 4: Access Application
- Open browser: http://localhost:5173
- Login with: admin / admin123

---

## System Features Overview

### 1. Dashboard
- Real-time system statistics
- Certificate generation count
- Active user monitoring
- System health status

### 2. Certificate Templates
- Drag-and-drop editor
- Upload background images
- Add text, images, QR codes
- Save and manage templates

### 3. Certificate Generation
- Single certificate generation
- Bulk upload (Excel/CSV)
- Preview before download
- Multiple format support

### 4. Merit Rankings
- View student rankings
- Filter by department/event
- Export in multiple formats
- Top performer highlighting

### 5. System Monitoring
- Real-time CPU/Memory/Disk monitoring
- Active user sessions
- System performance graphs
- Alert management

### 6. Settings
- Configure SMS alerts
- Theme preferences
- Session timeout
- Upload size limits

---

## Default Admin Account

```
Username: admin
Password: admin123
Email: admin@example.com
```

**⚠️ Important:** Change this password in production!

---

## Accessing Documentation

- **API Documentation**: http://localhost:8000/docs
- **Alternative**: http://localhost:8000/redoc
- **Setup Guide**: See SETUP_GUIDE.md
- **Full README**: See README.md

---

## Common First Steps

### 1. Create Certificate Template
1. Go to **Templates** → **Template Designer**
2. Add text, images, QR code
3. Click **Save Template**

### 2. Generate a Certificate
1. Go to **Certificates** → **Certificate Generator**
2. Select template
3. Fill in student information
4. Click **Generate Certificate**
5. PDF will download

### 3. Add Rankings
1. Go to **Rankings**
2. Upload Excel file with columns: student_name, marks
3. View and export rankings

### 4. Monitor System
1. Go to **Monitoring**
2. View real-time system statistics
3. See active users
4. Check performance graphs

---

## Troubleshooting

### Backend won't start
```
Error: Port 8000 in use
Solution: Kill process or use different port
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database connection error
```
Error: Can't connect to MySQL
Solution: 
1. Make sure MySQL is running
2. Check credentials in backend/.env
3. Create database: mysql -u root -p < database/schema.sql
```

### Frontend not loading
```
Error: Can't reach API
Solution:
1. Check backend is running (http://localhost:8000/health)
2. Check CORS settings in backend/.env
3. Clear browser cache
```

---

## Keyboard Shortcuts

### Template Designer
- **Ctrl+S**: Save template
- **Delete**: Remove selected element
- **Drag**: Move element
- **Ctrl+Drag**: Copy element

### Certificate Generator
- **Tab**: Move to next field
- **Enter**: Submit form

---

## File Locations

```
Generated Certificates: generated_certificates/
Uploaded Files: uploads/
Log Files: logs/
Database Backups: backups/
Exported Reports: exports/
```

---

## Contact & Support

- **Admin Dashboard**: http://localhost:5173/settings
- **API Support**: http://localhost:8000/docs
- **Technical Issues**: Check logs/app.log
- **Report Bugs**: GitHub Issues

---

## Next Steps

1. ✅ System is running
2. 📝 Customize certificate templates
3. 👥 Add student information
4. 📊 Generate certificates
5. 📈 View rankings and reports
6. ⚙️ Configure settings and alerts

---

**Version:** 1.0.0  
**Last Updated:** March 2026
