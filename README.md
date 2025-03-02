# SPEAK-IT! v0.9.0 (Pre-Beta)

## Overview
SPEAK-IT! is a system tray application that converts selected text to speech using a local Kokoro TTS API. It features an auto-play mode, silent audio playback, and an interactive introduction. Perfect for seamless text-to-speech integration in your workflow.

## Features
- System tray integration with GTK3
- Text-to-speech conversion using Kokoro TTS
- Standard OpenAI voice selection (alloy, echo, fable, etc.)
- Auto-play mode for automatic speech of selected text
- Silent audio playback (no media player windows)
- Clipboard monitoring for text selection
- Clean temporary file management
- Interactive About dialog with surprises

## Requirements
### System Dependencies
```bash
sudo apt-get install -y python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0 mpg123 python3-venv
```

### Python Environment
- Python 3.10+
- GTK3 bindings (via system packages)
- OpenAI client library
- mpg123 for audio playback

### Kokoro TTS API
This application requires a running instance of the Kokoro TTS API. We recommend using the Docker version available at:
- [https://github.com/remsky/Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI)

Follow the instructions in that repository to set up the API server before installing SPEAK-IT!

## Installation

### Quick Start for Friends (Ubuntu)
If you're sharing this application with friends who are not familiar with GitHub, here's what they need to do:

1. Set up the Kokoro TTS API using the Docker version:
   - Follow instructions at [https://github.com/remsky/Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI)
   - Make sure the API is running on http://localhost:8880/v1

2. Download the project as a ZIP file from GitHub
   - Visit https://github.com/loserbcc/speak-it
   - Click the green "Code" button
   - Select "Download ZIP"
   - Extract the ZIP file to a location of their choice

3. Open a terminal in the extracted directory and run:
```bash
sudo ./install.sh
```

4. Once installation is complete, they can start the application by:
   - Running `speak-it` in a terminal, or
   - Finding "SPEAK-IT!" in their applications menu

5. The application will also start automatically on next login

### Option 1: System-wide Installation (Ubuntu)
1. Clone the repository
```bash
git clone https://github.com/loserbcc/speak-it.git
cd speak-it
```

2. Run the installer script
```bash
sudo ./install.sh
```

3. The application will:
   - Install all required system dependencies
   - Create a dedicated Python virtual environment with access to system packages
   - Set up the application in `/opt/speak-it/`
   - Create a launcher in `/usr/local/bin/speak-it`
   - Add a desktop entry to your applications menu
   - Configure auto-start on login

### Option 2: Manual Installation (Development)
1. Clone the repository
```bash
git clone https://github.com/loserbcc/speak-it.git
cd speak-it
```

2. Create and activate a virtual environment with system site packages:
```bash
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Uninstallation
To uninstall SPEAK-IT! from your system:

```bash
sudo ./uninstall.sh
```

This will:
- Remove all application files from `/opt/speak-it/`
- Remove the launcher script
- Remove desktop entries
- Stop any running instances

## Usage
1. Look for the speaker icon in your system tray
2. Right-click the icon to see available options:
   - "Speak Selected Text": Converts currently selected text to speech
   - "Auto Play Selected": Automatically speaks any newly selected text
   - "Select Model": Choose TTS model
   - "Select Voice": Choose from standard OpenAI voices
   - "About": View the interactive introduction
   - "Exit": Closes the application
3. When Auto Play is enabled, the icon changes to a record symbol

## API Configuration
The application uses a local Kokoro TTS API:
- Endpoint: http://localhost:8880/v1
- Default voice: alloy
- Model: kokoro
- No API key required (using "not-needed")

For setting up the API, please refer to [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI).

## Version History
See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Development
- Language: Python 3.10+
- GUI Framework: GTK3 via PyGObject
- Audio Playback: mpg123
- API Client: OpenAI Python Client

## Contact
For questions or feedback: Brian@Loser.com
