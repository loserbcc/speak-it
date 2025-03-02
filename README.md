# SPEAK-IT! v0.9.0 (Pre-Beta)

## Overview
SPEAK-IT! is a system tray application that converts selected text to speech using a local Kokoro TTS API. It features an auto-play mode, silent audio playback, and a Zork-style interactive introduction. Perfect for seamless text-to-speech integration in your workflow.

## Features
- System tray integration with GTK3
- Text-to-speech conversion using Kokoro TTS
- Standard OpenAI voice selection (alloy, echo, fable, etc.)
- Auto-play mode for automatic speech of selected text
- Silent audio playback (no media player windows)
- Clipboard monitoring for text selection
- Clean temporary file management
- Interactive Zork-style About dialog

## Requirements
### System Dependencies
```bash
sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 mpg123
```

### Python Environment
- Conda environment (recommended)
- Python 3.10
- GTK3 bindings
- OpenAI client library
- mpg123 for audio playback

## Installation
1. Clone the repository
2. Create and activate the conda environment:
```bash
conda create -n speak-gui python=3.10 -y
conda activate speak-gui
conda install -c conda-forge pygobject gtk3
conda install openai
```

## Usage
1. Activate the conda environment:
```bash
conda activate speak-gui
```

2. Run the application:
```bash
python main.py
```

3. Using the application:
   - Look for the speaker icon in your system tray
   - Right-click the icon to see available options:
     - "Speak Selected Text": Converts currently selected text to speech
     - "Auto Play Selected": Automatically speaks any newly selected text
     - "Select Model": Choose TTS model
     - "Select Voice": Choose from standard OpenAI voices
     - "About": View the interactive introduction
     - "Exit": Closes the application
   - When Auto Play is enabled, the icon changes to a record symbol

## API Configuration
The application uses a local Kokoro TTS API:
- Endpoint: http://localhost:8880/v1
- Default voice: alloy
- Model: kokoro
- No API key required (using "not-needed")

## Version History
See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Development
- Language: Python 3.10
- GUI Framework: GTK3 via PyGObject
- Audio Playback: mpg123
- API Client: OpenAI Python Client

## Contact
For questions or feedback: Brian@Loser.com
