# Changelog

## [1.1.0] - 2025-03-01

### Added
- Dynamic model selection from API
- Dynamic voice selection from API
- Refresh capability for models and voices
- Submenu for model selection
- Submenu for voice selection

### Changed
- Menu structure updated to include model and voice selection
- API integration enhanced to fetch available models and voices

## [1.0.0] - 2025-03-01

### Added
- Initial release of Speak-GUI
- System tray integration using GTK3
- Text-to-speech functionality using Kokoro TTS API
- Auto-play feature for automatic speech of selected text
- Silent audio playback using mpg123
- Clipboard monitoring for text selection
- Automatic cleanup of temporary audio files

### Technical Details
- Uses OpenAI-compatible API endpoint (local Kokoro TTS)
- Default voice: alloy
- Model: kokoro
- API endpoint: http://localhost:8880/v1
- Audio format: MP3

## [0.9.0] - 2025-03-02 (Pre-Beta)

### Added
- Zork-style interactive introduction
- Standard OpenAI voice selection (alloy, echo, fable, etc.)
- System tray integration with GTK3
- Text-to-speech with Kokoro TTS API
- Auto-play feature for selected text
- Silent audio playback using mpg123
- Model selection from API
- Voice selection menu
- About dialog with interactive reading
- Clipboard monitoring
- Automatic cleanup of temporary files

### Changed
- Switched to standard OpenAI voice names
- Improved About dialog with Zork-style narrative
- Updated contact to Brian@Loser.com
- Enhanced menu organization with current settings display

### Technical Details
- Uses OpenAI-compatible API endpoint (local Kokoro TTS)
- Default voice: alloy
- Model: kokoro
- API endpoint: http://localhost:8880/v1
- Audio format: MP3
