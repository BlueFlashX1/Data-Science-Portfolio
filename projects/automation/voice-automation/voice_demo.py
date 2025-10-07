#!/usr/bin/env python3
"""
Voice Control System Demo
=========================

Academic project demonstrating voice-controlled system automation for macOS.
Developed during Master's Data Science program as an example of system integration
and natural language processing applications.

Author: Matthew Thompson
Course: Master's Data Science Program
Institution: University of Arizona

Usage:
    python voice_demo.py

Requirements:
    - macOS 10.14+
    - Python 3.9+
    - Microphone access
    - Accessibility permissions
"""

import os
import sys
import subprocess
import re
import time
import logging
from datetime import datetime
from pathlib import Path

try:
    import speech_recognition as sr
except ImportError:
    print("ERROR: speech_recognition not installed. Run: pip install speechrecognition")
    sys.exit(1)

# Configure logging
log_dir = Path.home() / "Documents" / "automation-logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"voice_automation_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class VoiceControlSystem:
    """Main voice control system for macOS automation."""
    
    def __init__(self):
        """Initialize the voice control system."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.setup_microphone()
        self.load_commands()
        
    def setup_microphone(self):
        """Configure microphone settings."""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                logger.info("Microphone configured successfully")
        except Exception as e:
            logger.error(f"Microphone setup failed: {e}")
            print("ERROR: Microphone not accessible. Check System Preferences > Privacy > Microphone")
            sys.exit(1)
    
    def load_commands(self):
        """Load command patterns and system applications."""
        # System control commands with parameter patterns
        self.param_commands = {
            "set_volume": [
                r"set volume to (\d+)%?",
                r"volume (\d+)%?", 
                r"change volume to (\d+)%?"
            ],
            "set_brightness": [
                r"set brightness to (\d+)%?",
                r"brightness (\d+)%?",
                r"change brightness to (\d+)%?"
            ]
        }
        
        # Simple system commands
        self.simple_commands = {
            "mute": ["mute", "mute volume", "silence"],
            "unmute": ["unmute", "unmute volume", "sound on"],
            "lock_screen": ["lock screen", "lock", "secure screen"],
            "sleep": ["sleep", "sleep system", "go to sleep"],
            "wifi_off": ["turn off wifi", "disable wifi", "wifi off"],
            "wifi_on": ["turn on wifi", "enable wifi", "wifi on"]
        }
        
        # Application commands  
        self.app_commands = {
            "open": ["open", "launch", "start"],
            "close": ["close", "quit", "exit"],
            "minimize": ["minimize", "hide"]
        }
        
        # Common applications
        self.applications = {
            "safari": "Safari",
            "chrome": "Google Chrome", 
            "firefox": "Firefox",
            "code": "Visual Studio Code",
            "vscode": "Visual Studio Code",
            "terminal": "Terminal",
            "finder": "Finder",
            "music": "Music",
            "spotify": "Spotify",
            "notes": "Notes",
            "calculator": "Calculator"
        }
        
        logger.info("Command patterns loaded successfully")
    
    def listen_for_command(self, timeout=5):
        """Listen for voice command with timeout."""
        try:
            with self.microphone as source:
                print(f"\nListening for command (timeout: {timeout}s)...")
                audio = self.recognizer.listen(source, timeout=timeout)
                
            print("Processing speech...")
            command = self.recognizer.recognize_google(audio).lower()
            print(f"Recognized: '{command}'")
            logger.info(f"Voice command recognized: {command}")
            return command
            
        except sr.UnknownValueError:
            print("Could not understand the audio")
            logger.warning("Speech recognition failed - unclear audio")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            logger.error(f"Speech recognition request failed: {e}")
            return None
        except sr.WaitTimeoutError:
            print("Listening timeout - no speech detected")
            logger.info("Voice listening timeout")
            return None
    
    def process_command(self, command):
        """Process and execute voice command."""
        if not command:
            return False
            
        # Check parameter commands first
        for action, patterns in self.param_commands.items():
            for pattern in patterns:
                match = re.search(pattern, command)
                if match:
                    value = int(match.group(1))
                    return self.execute_param_command(action, value)
        
        # Check simple system commands
        for action, phrases in self.simple_commands.items():
            if any(phrase in command for phrase in phrases):
                return self.execute_simple_command(action)
        
        # Check application commands
        for app_action, action_phrases in self.app_commands.items():
            for action_phrase in action_phrases:
                if action_phrase in command:
                    # Find application name in command
                    for app_name, system_name in self.applications.items():
                        if app_name in command:
                            return self.execute_app_command(app_action, system_name)
        
        print(f"Command not recognized: '{command}'")
        logger.warning(f"Unrecognized command: {command}")
        return False
    
    def execute_param_command(self, action, value):
        """Execute system command with parameter."""
        try:
            if action == "set_volume":
                cmd = f'osascript -e "set volume output volume {value}"'
                result = os.system(cmd)
                if result == 0:
                    print(f"Volume set to {value}%")
                    logger.info(f"Volume changed to {value}%")
                    return True
                    
            elif action == "set_brightness":
                # Note: Requires brightness utility (brew install brightness)
                cmd = f"brightness {value / 100.0}"
                result = subprocess.run(cmd, shell=True, capture_output=True)
                if result.returncode == 0:
                    print(f"Brightness set to {value}%")
                    logger.info(f"Brightness changed to {value}%")
                    return True
                else:
                    print("Brightness control requires 'brightness' utility")
                    print("   Install with: brew install brightness")
                    
        except Exception as e:
            print(f"Error executing {action}: {e}")
            logger.error(f"Parameter command error: {action} with value {value} - {e}")
            
        return False
    
    def execute_simple_command(self, action):
        """Execute simple system command."""
        try:
            commands = {
                "mute": 'osascript -e "set volume output muted true"',
                "unmute": 'osascript -e "set volume output muted false"',
                "lock_screen": 'osascript -e "tell application \\"System Events\\" to keystroke \\"q\\" using {control down, command down}"',
                "sleep": 'osascript -e "tell application \\"System Events\\" to sleep"',
                "wifi_off": "networksetup -setairportpower en0 off",
                "wifi_on": "networksetup -setairportpower en0 on"
            }
            
            if action in commands:
                cmd = commands[action]
                result = os.system(cmd)
                
                action_messages = {
                    "mute": "Volume muted",
                    "unmute": "Volume unmuted", 
                    "lock_screen": "Screen locked",
                    "sleep": "System sleeping...",
                    "wifi_off": "WiFi disabled",
                    "wifi_on": "WiFi enabled"
                }
                
                if result == 0:
                    print(action_messages.get(action, f"{action} executed"))
                    logger.info(f"System command executed: {action}")
                    return True
                    
        except Exception as e:
            print(f"Error executing {action}: {e}")
            logger.error(f"Simple command error: {action} - {e}")
            
        return False
    
    def execute_app_command(self, action, app_name):
        """Execute application command."""
        try:
            if action == "open":
                cmd = f'osascript -e "tell application \\"{app_name}\\" to activate"'
                result = os.system(cmd)
                if result == 0:
                    print(f"Opened {app_name}")
                    logger.info(f"Application opened: {app_name}")
                    return True
                    
            elif action == "close":
                cmd = f'osascript -e "tell application \\"{app_name}\\" to quit"'
                result = os.system(cmd)
                if result == 0:
                    print(f"Closed {app_name}")
                    logger.info(f"Application closed: {app_name}")
                    return True
                    
            elif action == "minimize":
                cmd = f'osascript -e "tell application \\"System Events\\" to set visible of process \\"{app_name}\\" to false"'
                result = os.system(cmd)
                if result == 0:
                    print(f"Minimized {app_name}")
                    logger.info(f"Application minimized: {app_name}")
                    return True
                    
        except Exception as e:
            print(f"Error with {app_name}: {e}")
            logger.error(f"Application command error: {action} {app_name} - {e}")
            
        return False
    
    def show_help(self):
        """Display available commands."""
        print("\n" + "="*60)
        print("VOICE CONTROL SYSTEM - Available Commands")
        print("="*60)
        
        print("\nSYSTEM CONTROL:")
        print("  • 'Set volume to 50' - Change system volume (0-100)")
        print("  • 'Mute' / 'Unmute' - Control volume muting")
        print("  • 'Set brightness to 75' - Change screen brightness")
        print("  • 'Lock screen' - Lock the system")
        print("  • 'Sleep' - Put system to sleep")
        print("  • 'Turn on/off WiFi' - Control WiFi connection")
        
        print("\nAPPLICATION CONTROL:")
        print("  • 'Open [app]' - Launch application")
        print("  • 'Close [app]' - Quit application") 
        print("  • 'Minimize [app]' - Hide application")
        
        print("\nSUPPORTED APPLICATIONS:")
        apps = list(self.applications.keys())
        for i in range(0, len(apps), 4):
            row = apps[i:i+4]
            print("  " + " | ".join(f"{app:<12}" for app in row))
            
        print("\nCONTROL COMMANDS:")
        print("  • 'help' - Show this help")
        print("  • 'quit' / 'exit' - Exit voice control")
        print("  • 'test' - Test microphone")
        
        print("\n" + "="*60)
    
    def run_demo(self):
        """Run the voice control demo."""
        print("\nVoice Control System - Academic Demo")
        print("====================================")
        print("Developed during Master's Data Science Program")
        print("University of Arizona")
        print("")
        print("This demo showcases system integration and speech recognition")
        print("applied to macOS automation and productivity enhancement.")
        print("")
        
        # Check permissions
        self.check_permissions()
        
        print("\nSystem ready! Say 'help' for commands or 'quit' to exit.")
        logger.info("Voice control system started")
        
        while True:
            try:
                command = self.listen_for_command()
                
                if command:
                    if command in ['quit', 'exit', 'stop']:
                        print("Goodbye!")
                        logger.info("Voice control system stopped by user")
                        break
                    elif command == 'help':
                        self.show_help()
                    elif command == 'test':
                        print("Microphone test successful!")
                    else:
                        success = self.process_command(command)
                        if success:
                            print("Command executed successfully")
                        else:
                            print("Command failed or not recognized")
                            print("Say 'help' to see available commands")
                
                print("\n" + "-"*40)
                time.sleep(1)  # Brief pause between commands
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! (Interrupted by Ctrl+C)")
                logger.info("Voice control system interrupted by user")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                logger.error(f"Unexpected error in main loop: {e}")
    
    def check_permissions(self):
        """Check required system permissions."""
        print("Checking system permissions...")
        
        # Check microphone access by attempting to use it
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Microphone access: OK")
        except Exception:
            print("Microphone access: DENIED")
            print("   Please enable microphone access in System Preferences")
            return False
        
        # Check if we can run AppleScript
        try:
            result = subprocess.run(
                ['osascript', '-e', 'return "test"'], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("AppleScript access: OK")
            else:
                print("AppleScript access: LIMITED")
        except Exception:
            print("AppleScript access: FAILED")
        
        print("Log file:", log_file)
        return True


def main():
    """Main entry point for voice control demo."""
    try:
        # Create voice control system
        voice_system = VoiceControlSystem()
        
        # Run the demo
        voice_system.run_demo()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"Failed to start voice control system: {e}")
        logger.error(f"System startup error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()