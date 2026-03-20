#!/bin/bash

# Start Frontend Development Server

cd frontend

echo "Starting Certificate Management System Frontend..."
echo ""
echo "Frontend will be available at: http://localhost:5173"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo ""
fi

# Start development server
npm run dev
