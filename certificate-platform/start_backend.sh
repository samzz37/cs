#!/bin/bash

# Start Backend Server

cd backend

# Activate virtual environment
if [ -d "venv/bin" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

echo "Starting Certificate Management System Backend..."
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "API documentation: http://localhost:8000/docs"
echo ""

# Start uvicorn server
python -m uvicorn asgi:app --reload --host 0.0.0.0 --port 8000
