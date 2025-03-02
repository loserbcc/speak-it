#!/bin/bash

# Exit on error
set -e

echo "Testing SPEAK-IT! installation..."

# Check if speak-it is installed
if [ ! -f "/usr/local/bin/speak-it" ]; then
    echo "ERROR: SPEAK-IT! is not installed. Please run the installer first."
    exit 1
fi

# Check if application files exist
if [ ! -d "/opt/speak-it" ]; then
    echo "ERROR: Application directory not found."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "/opt/speak-it/venv" ]; then
    echo "ERROR: Python virtual environment not found."
    exit 1
fi

# Check if desktop entries exist
if [ ! -f "/usr/share/applications/speak-it.desktop" ]; then
    echo "ERROR: Desktop entry not found."
    exit 1
fi

if [ ! -f "/etc/xdg/autostart/speak-it.desktop" ]; then
    echo "ERROR: Autostart entry not found."
    exit 1
fi

# Check if Python dependencies are installed
echo "Checking Python dependencies..."
if ! /opt/speak-it/venv/bin/pip list | grep -q "openai"; then
    echo "ERROR: OpenAI package not installed."
    exit 1
fi

# All checks passed
echo "✅ All installation checks passed!"
echo "You can now run SPEAK-IT! by typing 'speak-it' in the terminal"
echo "or by finding it in your applications menu."
echo ""
echo "SPEAK-IT! will also start automatically on next login."
