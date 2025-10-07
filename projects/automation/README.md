# System Automation Projects

**Academic Development Projects** - Python and Shell automation solutions

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Shell](https://img.shields.io/badge/Shell-Bash/Zsh-green?style=for-the-badge&logo=gnu-bash)](https://gnu.org/software/bash/)
[![macOS](https://img.shields.io/badge/macOS-Compatible-black?style=for-the-badge&logo=apple)](https://apple.com/macos)

> Collection of automation tools developed during Master's Data Science program to improve development workflow efficiency and system management.

## Quick Navigation
**Jump to:** [Voice Automation](#voice-controlled-system-automation) | [Error Management](#smart-error-management-system) | [Installation](#installation--setup) | [Demo](#demos) | [Technical Details](#technical-implementation)

## Projects Overview

### Voice-Controlled System Automation
**Advanced Python automation using speech recognition for macOS system control**  
*Personal productivity project demonstrating system integration skills*

**Key Features:**
- **Voice-Controlled System Management**: Volume, brightness, WiFi, power controls via natural language
- **Application Management**: Launch, minimize, close applications by voice command  
- **Window Management**: Full screen, split screen, window positioning through speech
- **Media Control**: Play/pause, track navigation across system media players
- **Smart Command Processing**: Natural language understanding with command variations
- **Comprehensive Logging**: Detailed activity logging with error tracking

**Technologies**: `Python | SpeechRecognition | macOS AppleScript | System Integration | Natural Language Processing`

### Smart Error Management System
**Shell-based automated error documentation and resolution tracking**  
*Development workflow optimization project*

**Key Features:**
- **Automated Error Documentation**: Structured error logging with unique ID system
- **Smart Resolution Detection**: Test-based verification of error resolution
- **Cross-Environment Support**: Terminal, VS Code, system, and development environment tracking
- **Status Management**: Comprehensive error lifecycle tracking (ongoing → resolved)
- **Template-Based Documentation**: Consistent error reporting structure

**Technologies**: `Shell Scripting | Process Automation | System Administration | Documentation Systems`

## Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/[username]/system-automation-projects.git
cd system-automation-projects

# Install Python dependencies
pip install -r requirements.txt

# Set up error management system
chmod +x error-management/*.sh
```

### Voice Control Demo
```bash
# Test voice automation (requires microphone)
python voice-automation/voice_demo.py

# Example commands to try:
# "Set volume to 50"
# "Open Visual Studio Code"  
# "Full screen window"
```

### Error Management Demo
```bash
# Document an error
./error-management/log-error.sh terminal "example error description"

# Test error resolution
./error-management/smart-resolve.sh TERM-001 "echo 'test command'"

# Check error status
./error-management/list-errors.sh
```

## Technical Implementation

### Voice Automation Architecture
```
Voice Input → Speech Recognition → Command Processing → System Execution → Logging
     ↓              ↓                    ↓                   ↓             ↓
  Microphone    Google API         Regex Matching      AppleScript    Python Logging
```

**Core Components:**
- **Speech Recognition**: Google Speech API integration
- **Command Processing**: Regex pattern matching for natural language
- **System Integration**: AppleScript execution for macOS control
- **Application Control**: macOS System Events automation
- **Logging System**: Comprehensive activity and error logging

### Error Management Workflow
```
Error Occurs → Auto-Documentation → Resolution Tracking → Verification Testing → Status Update
     ↓               ↓                     ↓                    ↓                ↓
 Real Problem    Template Form      Progress Tracking    Test Commands     RESOLVED
```

## File Structure

```
system-automation-projects/
├── README.md                          # This documentation
├── requirements.txt                   # Python dependencies
├── setup.sh                          # Installation script
├── voice-automation/                  # Voice control system
│   ├── voice_demo.py                 # Main demo script
│   ├── system_control.py             # Core system control
│   ├── window_management.py          # Window management
│   ├── command_processor.py          # Command processing
│   └── config.py                     # Configuration settings
├── error-management/                  # Error tracking system
│   ├── log-error.sh                  # Error documentation
│   ├── smart-resolve.sh              # Resolution testing
│   ├── update-status.sh              # Status management
│   ├── list-errors.sh                # Error listing
│   └── templates/                    # Documentation templates
├── config/                           # Configuration files
│   ├── voice_commands.json           # Voice command mappings
│   └── app_paths.json                # Application paths
└── docs/                             # Additional documentation
    ├── VOICE_COMMANDS.md             # Voice command reference
    ├── ERROR_MANAGEMENT.md           # Error system guide
    └── DEVELOPMENT.md                # Development notes
```

## Demos

### Voice Control Commands
```python
# System Control
"Set volume to 75"
"Turn off WiFi"  
"Lock screen"
"Sleep system"

# Application Management
"Open Spotify"
"Minimize Safari"
"Close Notion"

# Window Management
"Full screen window"
"Split window left"
"Move window right"
```

### Error Management Examples
```bash
# Document new errors
./log-error.sh terminal "git authentication failed"
./log-error.sh vscode "extension not loading properly"

# Test resolutions
./smart-resolve.sh TERM-001 "git push origin main"
./smart-resolve.sh VS-001 "code --list-extensions"

# Check status
./list-errors.sh                    # All errors
./list-errors.sh --ongoing         # Only ongoing
./list-errors.sh --resolved        # Only resolved
```

## Skills Demonstrated

### **System Programming**
- **Multi-API Integration**: Speech recognition, system control, application management
- **Cross-Platform Scripting**: macOS AppleScript, Unix shell commands, Python subprocess
- **Real-Time Processing**: Voice command recognition with immediate system response
- **Error Handling**: Comprehensive exception management and graceful degradation

### **Automation Design**
- **User-Centric Interface**: Natural language command variations for intuitive use
- **Modular Architecture**: Separate modules for different automation domains
- **Extensible Framework**: Easy addition of new commands and applications
- **Production Logging**: Detailed activity tracking for troubleshooting

### **Development Workflow**
- **Problem Identification**: Systematic error documentation approach
- **Process Automation**: Reduced manual system management tasks
- **Quality Assurance**: Automated testing of error resolution
- **Knowledge Management**: Structured documentation for future reference

## Academic Context

**Course Relevance**: Developed during Master's Data Science program as practical applications of:
- **System Programming Concepts**: API integration and subprocess management
- **Process Automation**: Workflow optimization and efficiency improvement  
- **User Interface Design**: Natural language processing and command interpretation
- **Software Engineering**: Error handling, logging, and documentation practices

**Learning Outcomes**:
- **Python System Integration**: Combining multiple libraries for system control
- **Shell Scripting Proficiency**: Advanced automation and system administration
- **API Usage**: Working with external services and system APIs
- **Technical Documentation**: Creating comprehensive user and developer guides

## Requirements

### System Requirements
- **Operating System**: macOS 10.14+ (Mojave or later)
- **Python**: 3.9 or higher
- **Microphone**: Required for voice automation
- **Permissions**: Microphone and accessibility permissions for system control

### Python Dependencies
```
speechrecognition>=3.10.0
pyaudio>=0.2.11
requests>=2.31.0
```

### macOS Permissions
- **Microphone Access**: System Preferences → Privacy → Microphone
- **Accessibility**: System Preferences → Privacy → Accessibility
- **AppleScript**: Allow Terminal/applications to control system

## Future Enhancements

- **Cross-Platform Support**: Extend to Linux and Windows systems
- **Machine Learning**: Custom voice models for improved recognition
- **Web Dashboard**: Browser-based error management interface
- **API Integration**: Connect with GitHub issues, Slack, etc.
- **Voice Training**: Personalized voice command recognition

## Contributing

This is an academic project portfolio, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## License

MIT License - Feel free to use these automation concepts in your own projects.

## Contact

**Matthew Thompson** - Master's Data Science Student  
**Focus**: Healthcare informatics and biological data systems  
**Portfolio**: [GitHub Portfolio](https://github.com/[username]/portfolio)

---

<div align="center">

**Academic project demonstrating practical programming skills and automation thinking**

*Part of Master's Data Science program - University of Arizona*

[![Portfolio](https://img.shields.io/badge/View-Portfolio-blue?style=for-the-badge)](https://github.com/[username]/portfolio)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077B5?style=for-the-badge)](https://linkedin.com/in/[username])

</div>