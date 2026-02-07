#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 Starting JARVIS MARK I..."
echo "Version: 1.0.0"
echo "Created by: Singh Industries"
echo ""
if [ -d "macOS/JARVIS.app" ]; then
    open "macOS/JARVIS.app"
elif [ -f "JARVIS" ]; then
    chmod +x "JARVIS"
    ./JARVIS
else
    echo "❌ JARVIS not found!"
    echo "Please check the README.txt file."
fi
