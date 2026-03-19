## Certificate Management System - Setup & Deployment Guide

### System Requirements

- **Python**: 3.9 or higher
- **Node.js**: 16.0 or higher
- **npm**: 7.0 or higher
- **MySQL**: 5.7 or higher
- **Git**: Latest version

### Database Setup

1. Install MySQL and create database:

```bash
mysql -u root -p
CREATE DATABASE CS;
USE CS;
source database/schema.sql;
```

2. Create database user (optional):

```sql
CREATE USER 'cert_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON CS.* TO 'cert_user'@'localhost';
FLUSH PRIVILEGES;
```

### Backend Setup

1. Navigate to backend directory:

```bash
cd certificate-platform/backend
```

2. Create virtual environment:

```bash
python -m venv venv
```

3. Activate virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create `.env` file from `.env.example`:

```bash
cp ../configs/.env.example .env
```

6. Update `.env` with your configuration:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/CS
SECRET_KEY=your-secret-key-here-change-in-production
ENVIRONMENT=development
DEBUG=True
```

7. Run migrations (if needed):

```bash
python -m app.database
```

8. Start backend server:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd certificate-platform/frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start development server:

```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173`

### Production Deployment

#### Backend Production Setup

1. Install production ASGI server:

```bash
pip install gunicorn
```

2. Create production environment variables:

```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-very-secret-production-key
DATABASE_URL=mysql+pymysql://user:password@db_host:3306/CS
```

3. Run with Gunicorn:

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend Production Deployment

1. Build for production:

```bash
npm run build
```

2. Preview build:

```bash
npm run preview
```

3. Deploy `dist/` folder to:
   - Cloud storage (AWS S3, Azure Blob)
   - Web server (Nginx, Apache)
   - CDN (Cloudflare, CloudFront)

#### Nginx Configuration

Create `/etc/nginx/sites-available/certificate-platform`:

```nginx
upstream api {
    server localhost:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/certificate-platform/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Docker Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: CS
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=mysql+pymysql://root:root_password@mysql:3306/CS
      - SECRET_KEY=your-secret-key
    ports:
      - "8000:8000"
    depends_on:
      - mysql
    volumes:
      - ./backend:/app

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:80"
    depends_on:
      - backend

volumes:
  mysql_data:
```

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

Create `frontend/Dockerfile`:

```dockerfile
FROM node:16 as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Running with Docker

```bash
docker-compose up -d
```

Access the application at `http://localhost`

### System Features

#### Authentication
- Admin, Staff, and Student roles
- JWT-based tokens
- Session management
- Secure password hashing

#### Certificate Management
- Drag-drop template designer
- QR code generation
- Bulk certificate generation
- PDF/Word/Excel export

#### Monitoring
- Real-time system stats (CPU, Memory, Disk)
- Active user tracking
- Activity logs
- Automated alerts

#### Data Management
- Rankings/merit lists
- Student information
- Certificate records
- Export in multiple formats

### Default Credentials

For testing:

```
Username: admin
Password: admin123
Role: Administrator
```

### Troubleshooting

**Database Connection Error:**
- Check MySQL is running
- Verify DATABASE_URL in .env
- Ensure database exists

**Port Already in Use:**
```bash
# Change port in .env or use different port
npm run dev -- --port 3000
python -m uvicorn app.main:app --port 8001
```

**Module Import Errors:**
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Clear npm cache: `npm cache clean --force && npm install`

**CORS Errors:**
- Update CORS_ORIGINS in .env
- Check API URL in frontend .env

### Performance Optimization

1. Enable caching headers
2. Use CDN for static assets
3. Database connection pooling
4. Implement pagination for large datasets
5. Compress API responses
6. Use Redis for session management

### Security Recommendations

1. Change default SECRET_KEY
2. Use HTTPS in production
3. Implement rate limiting
4. Enable CSRF protection
5. Regular security audits
6. Update dependencies monthly
7. Use environment variables for secrets

### Monitoring & Logging

Log files location:
- Backend: `logs/app.log`
- System: `logs/system.log`
- Activity: Database `activity_logs` table

### Support & Documentation

- API Docs: `http://localhost:8000/docs`
- Report Issues: GitHub Issues
- Contributing: See CONTRIBUTING.md

---

**Last Updated**: 2026-03-19
**Version**: 1.0.0
