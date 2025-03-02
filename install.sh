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
apt-get install -y python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0 mpg123

# Create installation directory
echo "Creating installation directory..."
install -d /opt/speak-it

# Copy application files
echo "Copying application files..."
cp main.py /opt/speak-it/
cp VERSION /opt/speak-it/
cp README.md /opt/speak-it/
cp CHANGELOG.md /opt/speak-it/

# Create launcher script
echo "Creating launcher script..."
cat > /usr/local/bin/speak-it << 'EOF'
#!/bin/bash
cd /opt/speak-it
python3 main.py
EOF

# Make launcher executable
chmod +x /usr/local/bin/speak-it

# Install desktop entry
echo "Installing desktop entry..."
cp speak-it.desktop /usr/share/applications/
cp speak-it.desktop /etc/xdg/autostart/

# Set permissions
echo "Setting permissions..."
chmod -R 755 /opt/speak-it
chown -R root:root /opt/speak-it

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install openai pygobject

echo "Installation complete!"
echo "SPEAK-IT! will start automatically on next login"
echo "To start now, run: speak-it"
