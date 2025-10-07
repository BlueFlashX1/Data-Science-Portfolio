#!/usr/bin/env bash

# System Automation Projects Setup Script
# =======================================
# Academic project setup and installation script
# 
# Author: Matthew Thompson
# Course: Master's Data Science Program
# Institution: University of Arizona

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "========================================="
echo "   System Automation Projects Setup"
echo "========================================="
echo -e "${NC}"
echo "Academic project demonstrating:"
echo "• Voice-controlled system automation"  
echo "• Automated error documentation"
echo "• System integration with Python/Shell"
echo ""

# Check system requirements
echo -e "${BLUE}🔍 Checking system requirements...${NC}"

# Check macOS version
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ Error: This project requires macOS${NC}"
    exit 1
fi

echo -e "${GREEN}✅ macOS detected: $(sw_vers -productVersion)${NC}"

# Check Python version
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
    echo -e "${GREEN}✅ Python detected: ${python_version}${NC}"
    
    # Check if version is 3.9+
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
        echo -e "${GREEN}   Python version is compatible (3.9+)${NC}"
    else
        echo -e "${YELLOW}⚠️  Python version may be too old. Recommend 3.9+${NC}"
    fi
else
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.9+${NC}"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 available${NC}"
else
    echo -e "${RED}❌ pip3 not found${NC}"
    exit 1
fi

echo ""

# Install Python dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"

if [[ -f "requirements.txt" ]]; then
    echo "Installing from requirements.txt..."
    pip3 install -r requirements.txt
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, installing core dependencies...${NC}"
    pip3 install speechrecognition pyaudio
    echo -e "${GREEN}✅ Core dependencies installed${NC}"
fi

echo ""

# Set up voice automation
echo -e "${BLUE}🎤 Setting up voice automation...${NC}"

if [[ -d "voice-automation" ]]; then
    chmod +x voice-automation/*.py
    echo -e "${GREEN}✅ Voice automation scripts configured${NC}"
    
    # Test microphone access
    echo "Testing microphone access..."
    if python3 -c "import speech_recognition; sr = speech_recognition.Recognizer(); mic = speech_recognition.Microphone(); print('Microphone test passed')" 2>/dev/null; then
        echo -e "${GREEN}✅ Microphone access OK${NC}"
    else
        echo -e "${YELLOW}⚠️  Microphone access may require permissions${NC}"
        echo "   Go to System Preferences → Privacy & Security → Microphone"
        echo "   Enable microphone access for Terminal or your IDE"
    fi
else
    echo -e "${YELLOW}⚠️  voice-automation directory not found${NC}"
fi

echo ""

# Set up error management
echo -e "${BLUE}📝 Setting up error management system...${NC}"

if [[ -d "error-management" ]]; then
    chmod +x error-management/*.sh
    
    # Create logs directory
    mkdir -p error-management/logs
    
    echo -e "${GREEN}✅ Error management scripts configured${NC}"
    echo -e "${GREEN}✅ Logs directory created${NC}"
else
    echo -e "${YELLOW}⚠️  error-management directory not found${NC}"
fi

echo ""

# Create configuration directories
echo -e "${BLUE}⚙️  Setting up configuration...${NC}"

mkdir -p config docs

# Create basic configuration files
if [[ ! -f "config/voice_commands.json" ]]; then
    cat > config/voice_commands.json << 'EOF'
{
    "system_commands": {
        "volume": ["set volume to", "volume", "change volume to"],
        "brightness": ["set brightness to", "brightness", "change brightness to"],
        "mute": ["mute", "mute volume", "silence"],
        "unmute": ["unmute", "unmute volume", "sound on"]
    },
    "applications": {
        "safari": "Safari",
        "chrome": "Google Chrome",
        "firefox": "Firefox",
        "code": "Visual Studio Code",
        "vscode": "Visual Studio Code",
        "terminal": "Terminal",
        "finder": "Finder"
    }
}
EOF
    echo -e "${GREEN}✅ Voice commands configuration created${NC}"
fi

# Create log directories
mkdir -p logs

echo ""

# System permissions check
echo -e "${BLUE}🔒 Checking system permissions...${NC}"

echo "Checking accessibility permissions..."
if [[ $(sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "SELECT allowed FROM access WHERE service='kTCCServiceAccessibility' AND client='com.apple.Terminal';" 2>/dev/null) == "1" ]]; then
    echo -e "${GREEN}✅ Accessibility permissions OK${NC}"
else
    echo -e "${YELLOW}⚠️  Accessibility permissions needed for full functionality${NC}"
    echo "   Go to System Preferences → Privacy & Security → Accessibility"
    echo "   Enable access for Terminal or your IDE"
fi

echo ""

# Final setup
echo -e "${BLUE}🎯 Final setup steps...${NC}"

# Create quick start script
cat > quick-start.sh << 'EOF'
#!/usr/bin/env bash
echo "System Automation Projects - Quick Start"
echo "======================================="
echo ""
echo "Voice Control Demo:"
echo "  python3 voice-automation/voice_demo.py"
echo ""
echo "Error Management:"  
echo "  ./error-management/log-error.sh terminal 'example error'"
echo ""
echo "Documentation:"
echo "  cat README.md"
EOF

chmod +x quick-start.sh

echo -e "${GREEN}✅ Quick start script created${NC}"
echo -e "${GREEN}✅ Setup completed successfully!${NC}"

echo ""
echo -e "${BLUE}🚀 Ready to use!${NC}"
echo ""
echo "Quick commands to get started:"
echo ""
echo -e "${YELLOW}Voice Control Demo:${NC}"
echo "  python3 voice-automation/voice_demo.py"
echo ""
echo -e "${YELLOW}Error Documentation:${NC}" 
echo "  ./error-management/log-error.sh terminal 'test error'"
echo ""
echo -e "${YELLOW}View Documentation:${NC}"
echo "  cat README.md"
echo ""
echo -e "${YELLOW}Quick Start Guide:${NC}"
echo "  ./quick-start.sh"
echo ""

echo -e "${BLUE}📝 Important Notes:${NC}"
echo "• Enable microphone permissions for voice control"
echo "• Enable accessibility permissions for system automation" 
echo "• Check logs/ directory for automation logs"
echo "• All scripts are now executable"
echo ""

echo -e "${GREEN}🎓 Academic Project Setup Complete!${NC}"
echo "Developed during Master's Data Science Program"
echo "University of Arizona"