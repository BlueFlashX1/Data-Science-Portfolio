#!/usr/bin/env bash

# System Automation Projects - Interactive Demo
# =============================================
# Academic project demonstration script
#
# Author: Matthew Thompson
# Course: Master's Data Science Program
# Institution: University of Arizona

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════╗
║                System Automation Projects Demo                   ║
║                                                                  ║
║           🎓 Academic Project - Master's Data Science           ║
║                    University of Arizona                         ║
╚══════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}This interactive demo showcases:"
echo "• Voice-controlled system automation"
echo "• Automated error documentation system"
echo "• System integration and scripting capabilities"
echo -e "${NC}"

sleep 2

show_menu() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}              DEMO MENU                ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}1.${NC} Voice Control System Demo"
    echo -e "${YELLOW}2.${NC} Error Management System Demo"
    echo -e "${YELLOW}3.${NC} View Project Documentation"
    echo -e "${YELLOW}4.${NC} System Requirements Check"
    echo -e "${YELLOW}5.${NC} Configuration Overview"
    echo -e "${YELLOW}6.${NC} Quick Functionality Test"
    echo -e "${YELLOW}7.${NC} Project Structure"
    echo -e "${YELLOW}8.${NC} Exit Demo"
    echo ""
    echo -ne "${CYAN}Select option (1-8): ${NC}"
}

voice_control_demo() {
    echo ""
    echo -e "${BLUE}Voice Control System Demo${NC}"
    echo "============================="
    echo ""
    echo -e "${YELLOW}This demo will show the voice automation system.${NC}"
    echo "The system can:"
    echo "• Control system volume and brightness"
    echo "• Manage applications (open, close, minimize)"
    echo "• Handle WiFi and power controls"
    echo "• Process natural language commands"
    echo ""
    
    echo -ne "${CYAN}Start voice control demo? (y/n): ${NC}"
    read -r response
    
    if [[ $response == "y" ]]; then
        echo ""
        echo -e "${GREEN}Starting voice control system...${NC}"
        echo -e "${YELLOW}Note: This requires microphone permissions and speech recognition.${NC}"
        echo ""
        
        if [[ -f "voice-automation/voice_demo.py" ]]; then
            python3 voice-automation/voice_demo.py
        else
            echo -e "${RED}Error: voice_demo.py not found${NC}"
        fi
    fi
}

error_management_demo() {
    echo ""
    echo -e "${BLUE}Error Management System Demo${NC}"
    echo "==============================="
    echo ""
    echo -e "${YELLOW}This demo shows the automated error documentation system.${NC}"
    echo ""
    
    # Create example error
    echo -e "${CYAN}Creating example error documentation...${NC}"
    ./error-management/log-error.sh terminal "Demo error - testing system functionality"
    
    echo ""
    echo -e "${CYAN}Listing documented errors:${NC}"
    ./error-management/list-errors.sh --summary
    
    echo ""
    echo -e "${CYAN}Viewing detailed error log:${NC}"
    if [[ -f "error-management/logs/terminal-errors.txt" ]]; then
        echo -e "${YELLOW}Last few lines of terminal-errors.txt:${NC}"
        tail -20 error-management/logs/terminal-errors.txt
    fi
}

view_documentation() {
    echo ""
    echo -e "${BLUE}Project Documentation${NC}"
    echo "========================"
    echo ""
    
    if [[ -f "README.md" ]]; then
        echo -e "${CYAN}Showing project README (first 50 lines):${NC}"
        head -50 README.md
        echo ""
        echo -e "${YELLOW}... (see README.md for complete documentation)${NC}"
    else
        echo -e "${RED}README.md not found${NC}"
    fi
    
    echo ""
    echo -ne "${CYAN}View requirements.txt? (y/n): ${NC}"
    read -r response
    if [[ $response == "y" && -f "requirements.txt" ]]; then
        echo ""
        echo -e "${CYAN}Python Requirements:${NC}"
        cat requirements.txt
    fi
}

system_check() {
    echo ""
    echo -e "${BLUE}System Requirements Check${NC}"
    echo "============================"
    echo ""
    
    # Check OS
    echo -e "${CYAN}Operating System:${NC}"
    if [[ "$(uname)" == "Darwin" ]]; then
        echo -e "${GREEN}✅ macOS $(sw_vers -productVersion)${NC}"
    else
        echo -e "${RED}❌ Not macOS (this project requires macOS)${NC}"
    fi
    
    # Check Python
    echo -e "${CYAN}Python Installation:${NC}"
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version)
        echo -e "${GREEN}✅ ${python_version}${NC}"
    else
        echo -e "${RED}❌ Python 3 not found${NC}"
    fi
    
    # Check dependencies
    echo -e "${CYAN}Python Dependencies:${NC}"
    dependencies=("speech_recognition" "pyaudio")
    for dep in "${dependencies[@]}"; do
        if python3 -c "import ${dep}" &> /dev/null; then
            echo -e "${GREEN}✅ ${dep}${NC}"
        else
            echo -e "${RED}❌ ${dep} (install with: pip3 install ${dep})${NC}"
        fi
    done
    
    # Check permissions
    echo -e "${CYAN}System Permissions:${NC}"
    echo -e "${YELLOW}ℹ️  Check System Preferences → Privacy & Security for:${NC}"
    echo "   • Microphone access (for voice control)"
    echo "   • Accessibility access (for system automation)"
}

configuration_overview() {
    echo ""
    echo -e "${BLUE}Configuration Overview${NC}"
    echo "========================="
    echo ""
    
    echo -e "${CYAN}Project Structure:${NC}"
    tree -L 3 2>/dev/null || find . -type d -maxdepth 3 | sed 's|[^/]*/|  |g'
    
    echo ""
    echo -e "${CYAN}Configuration Files:${NC}"
    if [[ -f "config/voice_commands.json" ]]; then
        echo -e "${GREEN}✅ Voice commands configuration${NC}"
    else
        echo -e "${YELLOW}⚠️  Voice commands config not found${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}Log Directories:${NC}"
    for dir in "logs" "error-management/logs"; do
        if [[ -d "$dir" ]]; then
            echo -e "${GREEN}✅ ${dir}/${NC}"
        else
            echo -e "${YELLOW}⚠️  ${dir}/ not found${NC}"
        fi
    done
}

quick_test() {
    echo ""
    echo -e "${BLUE}Quick Functionality Test${NC}"
    echo "=========================="
    echo ""
    
    # Test voice automation import
    echo -e "${CYAN}Testing voice automation imports:${NC}"
    if python3 -c "
import sys
sys.path.insert(0, 'voice-automation')
try:
    import speech_recognition
    print('✅ Speech recognition available')
except ImportError:
    print('❌ Speech recognition not available')
    
try:
    from voice_demo import VoiceControlSystem
    print('✅ Voice control system can be imported')
except ImportError as e:
    print(f'❌ Voice control import error: {e}')
" 2>/dev/null; then
        echo -e "${GREEN}Voice automation tests passed${NC}"
    else
        echo -e "${RED}Voice automation tests failed${NC}"
    fi
    
    # Test error management
    echo ""
    echo -e "${CYAN}Testing error management system:${NC}"
    if [[ -x "error-management/log-error.sh" ]]; then
        echo -e "${GREEN}✅ Error logging script is executable${NC}"
        # Create a test error
        ./error-management/log-error.sh system "Quick test error - can be ignored" &>/dev/null
        echo -e "${GREEN}✅ Test error created successfully${NC}"
    else
        echo -e "${RED}❌ Error management script issues${NC}"
    fi
}

project_structure() {
    echo ""
    echo -e "${BLUE}Project Structure${NC}"
    echo "==================="
    echo ""
    
    if command -v tree &> /dev/null; then
        tree -a -I '.git|__pycache__|*.pyc'
    else
        echo -e "${CYAN}Directory structure:${NC}"
        find . -type f -not -path './.git/*' | head -20 | sort
        echo "... (install 'tree' command for better view)"
    fi
    
    echo ""
    echo -e "${CYAN}Key Files:${NC}"
    key_files=(
        "README.md:Project documentation"
        "requirements.txt:Python dependencies"
        "setup.sh:Installation script" 
        "voice-automation/voice_demo.py:Voice control demo"
        "error-management/log-error.sh:Error documentation"
    )
    
    for file_desc in "${key_files[@]}"; do
        file="${file_desc%%:*}"
        desc="${file_desc##*:}"
        if [[ -f "$file" ]]; then
            echo -e "${GREEN}✅ ${file}${NC} - ${desc}"
        else
            echo -e "${RED}❌ ${file}${NC} - ${desc}"
        fi
    done
}

# Main demo loop
while true; do
    show_menu
    read -r choice
    
    case $choice in
        1) voice_control_demo ;;
        2) error_management_demo ;;
        3) view_documentation ;;
        4) system_check ;;
        5) configuration_overview ;;
        6) quick_test ;;
        7) project_structure ;;
        8) 
            echo ""
            echo -e "${GREEN}Thanks for viewing the System Automation Projects demo!${NC}"
            echo ""
            echo -e "${BLUE}Academic Project Information:${NC}"
            echo "  • Author: Matthew Thompson"
            echo "  • Course: Master's Data Science Program"
            echo "  • Institution: University of Arizona"
            echo "  • Focus: System integration and automation"
            echo ""
            echo -e "${CYAN}For more information, check the README.md file.${NC}"
            break
            ;;
        *)
            echo -e "${RED}Invalid option. Please choose 1-8.${NC}"
            sleep 1
            ;;
    esac
    
    echo ""
    echo -ne "${YELLOW}Press Enter to continue...${NC}"
    read -r
done