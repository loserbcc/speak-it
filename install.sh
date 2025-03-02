#!/bin/bash

# Exit on error
set -e

echo "Installing SPEAK-IT! v0.9.0 (Pre-Beta)"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0 mpg123 python3-venv

# Create installation directory
echo "Creating installation directory..."
install -d /opt/speak-it

# Copy application files
echo "Copying application files..."
cp main.py /opt/speak-it/
cp VERSION /opt/speak-it/
cp README.md /opt/speak-it/
cp CHANGELOG.md /opt/speak-it/
cp requirements.txt /opt/speak-it/

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv /opt/speak-it/venv --system-site-packages

# Install Python dependencies
echo "Installing Python dependencies..."
/opt/speak-it/venv/bin/pip install -r /opt/speak-it/requirements.txt

# Create launcher script
echo "Creating launcher script..."
cat > /usr/local/bin/speak-it << 'EOF'
#!/bin/bash
cd /opt/speak-it
/opt/speak-it/venv/bin/python main.py
EOF

# Make launcher executable
chmod +x /usr/local/bin/speak-it

# Install desktop entry
echo "Installing desktop entry..."
cp speak-it.desktop /usr/share/applications/
cp speak-it.desktop /etc/xdg/autostart/

# Update desktop entry paths
sed -i 's|Exec=.*|Exec=/usr/local/bin/speak-it|g' /usr/share/applications/speak-it.desktop
sed -i 's|Exec=.*|Exec=/usr/local/bin/speak-it|g' /etc/xdg/autostart/speak-it.desktop

# Set permissions
echo "Setting permissions..."
chmod -R 755 /opt/speak-it
chown -R root:root /opt/speak-it

echo "Installation complete!"
echo "SPEAK-IT! will start automatically on next login"
echo "To start now, run: speak-it"
echo ""
echo "To uninstall, run: sudo ./uninstall.sh"
