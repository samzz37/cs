#!/bin/bash

# Certificate Platform - Setup Script
# This script automates the setup process

set -e

echo "========================================="
echo "Certificate Management System Setup"
echo "========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL not found. Make sure MySQL is installed and running"
fi

echo "✅ Prerequisites check passed"
echo ""

# Backend Setup
echo "Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp ../configs/.env.example .env
    echo "⚠️  Please update .env with your database credentials"
fi

cd ..

# Frontend Setup
echo ""
echo "Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install -q

cd ..

# Database Setup
echo ""
echo "Database Setup"
echo "Creating database schema..."

read -p "Enter MySQL user (default: root): " DB_USER
DB_USER=${DB_USER:-root}

read -sp "Enter MySQL password: " DB_PASS
echo ""

read -p "Enter database name (default: CS): " DB_NAME
DB_NAME=${DB_NAME:-CS}

# Create database
mysql -u "$DB_USER" -p"$DB_PASS" << EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME;
USE $DB_NAME;
source database/schema.sql;
EOF

echo "✅ Database created successfully"
echo ""

# Create startup scripts
echo "Creating startup scripts..."

# Windows batch script
cat > start_backend.bat << 'EOF'
@echo off
cd backend
call venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
EOF

cat > start_frontend.bat << 'EOF'
@echo off
cd frontend
npm run dev
pause
EOF

# Unix shell script
cat > start_backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

cat > start_frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm run dev
EOF

chmod +x start_backend.sh start_frontend.sh

echo "✅ Startup scripts created"
echo ""

# Summary
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "📝 Next Steps:"
echo "1. Update backend/.env with your configuration"
echo "2. Start Backend:"
echo "   - Windows: start_backend.bat"
echo "   - Linux/Mac: ./start_backend.sh"
echo "3. Start Frontend (in new terminal):"
echo "   - Windows: start_frontend.bat"
echo "   - Linux/Mac: ./start_frontend.sh"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Default Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
