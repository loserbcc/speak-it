#!/bin/bash

# Exit on error
set -e

echo "Uninstalling SPEAK-IT!"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Stop any running instances
echo "Stopping any running instances..."
pkill -f "python.*main.py" || true

# Remove application files
echo "Removing application files..."
rm -rf /opt/speak-it

# Remove launcher script
echo "Removing launcher script..."
rm -f /usr/local/bin/speak-it

# Remove desktop entries
echo "Removing desktop entries..."
rm -f /usr/share/applications/speak-it.desktop
rm -f /etc/xdg/autostart/speak-it.desktop

echo "Uninstallation complete!"
echo "Note: System dependencies were not removed."
echo "If you want to remove them manually, you can use:"
echo "sudo apt remove python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0 mpg123 python3-venv"
