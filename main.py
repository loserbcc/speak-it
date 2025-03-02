import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import tempfile
import os
import subprocess
from openai import OpenAI
import json
import requests

client = OpenAI(
    base_url="http://localhost:8880/v1",
    api_key="not-needed"
)

class SpeakGUI:
    def __init__(self):
        # Create the status icon
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_stock(Gtk.STOCK_MEDIA_PLAY)
        self.status_icon.connect('popup-menu', self.on_right_click)
        self.status_icon.set_tooltip_text('SPEAK-IT!')
        
        # Initialize auto-play state
        self.auto_play = False
        self.last_text = ""
        self.current_process = None
        
        # Initialize models and voices
        self.current_model = "kokoro"
        self.current_voice = "alloy"  # Updated to just alloy
        self.available_models = self.fetch_models()
        self.available_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]  # Default OpenAI voices
        print(f"Available voices: {self.available_voices}")
        
        # Start the timer for checking selections
        GLib.timeout_add(1000, self.check_selection)  # Check every 1 second

    def fetch_models(self):
        try:
            response = client.models.list()
            return [model.id for model in response]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return ["kokoro"]  # Default fallback

    def fetch_voices(self):
        try:
            response = requests.get("http://localhost:8880/v1/audio/voices")
            data = response.json()
            if "voices" in data:
                return data["voices"]
            return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]  # Default fallback
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]  # Default fallback

    def check_selection(self):
        if self.auto_play:
            try:
                # Get clipboard content
                clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
                text = clipboard.wait_for_text()
                
                if text and text.strip() and text != self.last_text:
                    self.last_text = text
                    self.speak_text(text)
            except Exception as e:
                print(f"Auto-play error: {e}")
        
        return True  # Keep the timer running

    def create_model_menu(self):
        model_menu = Gtk.Menu()
        for model in self.available_models:
            item = Gtk.CheckMenuItem(label=model)
            item.set_active(model == self.current_model)
            item.connect('activate', self.on_model_selected, model)
            model_menu.append(item)
        return model_menu

    def create_voice_menu(self):
        voice_menu = Gtk.Menu()
        for voice in self.available_voices:
            item = Gtk.CheckMenuItem(label=voice)
            item.set_active(voice == self.current_voice)
            item.connect('activate', self.on_voice_selected, voice)
            voice_menu.append(item)
        return voice_menu

    def on_model_selected(self, widget, model):
        if widget.get_active():
            self.current_model = model
            # Deselect other models
            parent_menu = widget.get_parent()
            for item in parent_menu.get_children():
                if item != widget:
                    item.set_active(False)
            print(f"Selected model: {self.current_model}")
            self.show_notification("Model Changed", f"Now using model: {model}")

    def on_voice_selected(self, widget, voice):
        if widget.get_active():
            self.current_voice = voice
            # Deselect other voices
            parent_menu = widget.get_parent()
            for item in parent_menu.get_children():
                if item != widget:
                    item.set_active(False)
            print(f"Selected voice: {self.current_voice}")
            self.show_notification("Voice Changed", f"Now using voice: {voice}")

    def on_right_click(self, icon, button, time):
        menu = Gtk.Menu()

        # Speak item
        speak_item = Gtk.MenuItem(label="Speak Selected Text")
        speak_item.connect('activate', self.speak)
        menu.append(speak_item)

        # Auto Play toggle
        auto_play_item = Gtk.CheckMenuItem(label="Auto Play Selected")
        auto_play_item.set_active(self.auto_play)
        auto_play_item.connect('toggled', self.toggle_auto_play)
        menu.append(auto_play_item)

        # Separator
        menu.append(Gtk.SeparatorMenuItem())

        # Model submenu
        model_item = Gtk.MenuItem(label="Select Model")
        model_item.set_submenu(self.create_model_menu())
        menu.append(model_item)

        # Voice submenu
        voice_item = Gtk.MenuItem(label="Select Voice")
        voice_item.set_submenu(self.create_voice_menu())
        menu.append(voice_item)

        # Separator
        menu.append(Gtk.SeparatorMenuItem())

        # Current Settings
        current_settings = Gtk.MenuItem(label=f"Current: {self.current_model} / {self.current_voice}")
        current_settings.set_sensitive(False)  # Make it non-clickable
        menu.append(current_settings)

        # Refresh Models/Voices
        refresh_item = Gtk.MenuItem(label="Refresh Models/Voices")
        refresh_item.connect('activate', self.refresh_models_voices)
        menu.append(refresh_item)

        # Separator
        menu.append(Gtk.SeparatorMenuItem())

        # About
        about_item = Gtk.MenuItem(label="About")
        about_item.connect('activate', self.show_about)
        menu.append(about_item)

        # Quit item
        quit_item = Gtk.MenuItem(label="Exit")
        quit_item.connect('activate', self.quit_app)
        menu.append(quit_item)

        menu.show_all()
        menu.popup(None, None, None, self.status_icon, button, time)

    def refresh_models_voices(self, widget):
        self.available_models = self.fetch_models()
        self.available_voices = self.fetch_voices()
        print(f"Refreshed voices: {self.available_voices}")
        self.show_notification("Refresh Complete", "Models and voices have been updated")

    def toggle_auto_play(self, widget):
        self.auto_play = widget.get_active()
        # Update icon to show auto-play state
        if self.auto_play:
            self.status_icon.set_from_stock(Gtk.STOCK_MEDIA_RECORD)
            self.show_notification("Auto Play", "Auto Play is now enabled")
        else:
            self.status_icon.set_from_stock(Gtk.STOCK_MEDIA_PLAY)
            self.show_notification("Auto Play", "Auto Play is now disabled")
            self.last_text = ""  # Reset last text

    def speak(self, widget=None):
        try:
            # Get clipboard content
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
            text = clipboard.wait_for_text()
            
            if not text or not text.strip():
                # Try clipboard selection
                clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
                text = clipboard.wait_for_text()
                
            if not text or not text.strip():
                self.show_notification("Warning", "No text selected!")
                return

            self.speak_text(text)

        except Exception as e:
            self.show_notification("Error", str(e))

    def speak_text(self, text):
        try:
            print(f"Speaking with model={self.current_model}, voice={self.current_voice}")
            
            # Stop any currently playing audio
            if self.current_process and self.current_process.poll() is None:
                self.current_process.terminate()
                self.current_process.wait()

            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_path = temp_file.name

            # Generate speech using the API
            with client.audio.speech.with_streaming_response.create(
                model=self.current_model,
                voice=self.current_voice,
                input=text
            ) as response:
                response.stream_to_file(temp_path)

            # Play the audio using mpg123 in quiet mode
            self.current_process = subprocess.Popen(['mpg123', '-q', temp_path])
            
            # Delete the temporary file after playback is done
            def cleanup_temp_file():
                self.current_process.wait()
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
            # Run cleanup in background
            GLib.timeout_add(100, cleanup_temp_file)

        except Exception as e:
            print(f"Error in speak_text: {e}")
            self.show_notification("Error", str(e))

    def show_about(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name("SPEAK-IT!")
        about.set_version(self.get_version())
        about.set_copyright(" 2025 Frobozz Magic Software Company")
        
        self.zork_intro = """West of House
You are standing in an open field west of a white house, with a boarded front door.
There is a small mailbox here.

>open mailbox

Opening the mailbox reveals a small leaflet.

>read leaflet

(Taken)

WELCOME TO SPEAK-IT!
Brought to you by the Frobozz Company and Brian@Loser.com

Speak-It is your premier solution for seamless AI-driven text-to-speech. Whether you're exploring, coding, or just need an assistant that truly listens, Speak-It has you covered!"""
        
        # Add the read button at the top
        content_area = about.get_content_area()
        read_button = Gtk.Button(label="Read Introduction")
        # Insert the button at the beginning of the content area
        content_area.pack_start(read_button, False, False, 0)
        content_area.reorder_child(read_button, 0)
        read_button.connect("clicked", self.on_read_leaflet_clicked)
        read_button.show()
        
        about.set_comments(self.zork_intro)
        about.set_website("mailto:Brian@Loser.com")
        about.set_website_label("Brian@Loser.com")
        about.set_authors(["The Frobozz Magic Software Company"])
        
        about.run()
        about.destroy()

    def on_read_leaflet_clicked(self, button):
        # Save current voice and model
        saved_voice = self.current_voice
        saved_model = self.current_model
        
        # Set to default voice and model
        self.current_voice = "alloy"
        self.current_model = "kokoro"
        print(f"Reading leaflet with voice={self.current_voice}, model={self.current_model}")
        
        # Speak the entire intro text
        self.speak_text(self.zork_intro)
        
        # Restore previous voice and model
        self.current_voice = saved_voice
        self.current_model = saved_model
        print(f"Restored to voice={self.current_voice}, model={self.current_model}")

    def show_notification(self, title, message):
        notification = Gtk.MessageDialog(
            None, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, title)
        notification.format_secondary_text(message)
        notification.run()
        notification.destroy()

    def get_version(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as f:
                return f.read().strip()
        except:
            return "1.1.0"  # Fallback version

    def quit_app(self, widget=None):
        # Cleanup any playing audio before quitting
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
            self.current_process.wait()
        Gtk.main_quit()

    def run(self):
        Gtk.main()

if __name__ == '__main__':
    app = SpeakGUI()
    app.run()
