#!/usr/bin/env zsh

# AUTOMATED ERROR DOCUMENTATION SYSTEM
# ====================================
# Academic project demonstrating structured error tracking and documentation
# 
# Author: Matthew Thompson
# Course: Master's Data Science Program  
# Institution: University of Arizona
#
# Usage: ./log-error.sh [environment] [description]
# Example: ./log-error.sh terminal "git authentication failed"

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERROR_LOG_DIR="${SCRIPT_DIR}/logs"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
DATE_ONLY=$(date "+%Y-%m-%d")

# Create logs directory if it doesn't exist
mkdir -p "${ERROR_LOG_DIR}"

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo "${BLUE}AUTOMATED ERROR DOCUMENTATION SYSTEM${NC}"
    echo "===================================="
    echo "Academic project for systematic error tracking and resolution"
    echo ""
    echo "Usage: ./log-error.sh [environment] [description]"
    echo ""
    echo "Supported Environments:"
    echo "  terminal    - Terminal/shell errors (TERM-XXX)"
    echo "  python      - Python development errors (PY-XXX)"
    echo "  vscode      - VS Code editor errors (VS-XXX)"
    echo "  system      - macOS system errors (SYS-XXX)"
    echo "  database    - Database-related errors (DB-XXX)"
    echo ""
    echo "Examples:"
    echo "  ./log-error.sh terminal \"zsh function not loading\""
    echo "  ./log-error.sh python \"import module failed\""
    echo "  ./log-error.sh vscode \"extension not working\""
    echo ""
    echo "Features:"
    echo "  - Automatic error ID generation"
    echo "  - Structured documentation templates"
    echo "  - Error resolution tracking"
    echo "  - Cross-environment categorization"
}

get_next_error_id() {
    local env=$1
    local file="${ERROR_LOG_DIR}/${env}-errors.txt"
    local prefix
    
    # Map environment to prefix
    case $env in
        terminal) prefix="TERM" ;;
        python) prefix="PY" ;;
        vscode) prefix="VS" ;;
        system) prefix="SYS" ;;
        database) prefix="DB" ;;
        *) prefix="UNK" ;;
    esac
    
    if [[ ! -f "$file" ]]; then
        echo "${prefix}-001"
        return
    fi
    
    # Find highest existing error number
    local highest=$(grep -oE "${prefix}-[0-9]+" "$file" 2>/dev/null | \
                   sed "s/${prefix}-//" | \
                   sort -n | \
                   tail -1)
    
    if [[ -z "$highest" ]]; then
        echo "${prefix}-001"
    else
        printf "${prefix}-%03d" $((highest + 1))
    fi
}

create_error_entry() {
    local env=$1
    local description=$2
    local error_id=$3
    local file="${ERROR_LOG_DIR}/${env}-errors.txt"
    
    # Create file header if it's a new file
    if [[ ! -f "$file" ]]; then
        cat > "$file" << EOF
# ${env^^} ENVIRONMENT ERRORS
# ===========================
# Academic Error Documentation System
# Generated: $(date "+%Y-%m-%d %H:%M")
# Environment: ${env}
# 
# This file tracks errors encountered in the ${env} environment
# for systematic learning and resolution documentation.

EOF
    fi
    
    # Add the new error entry
    cat >> "$file" << EOF

=====================================
ERROR ${error_id}: ${description}
=====================================
Date: ${TIMESTAMP}
Environment: ${env}
System: macOS $(sw_vers -productVersion), zsh ${ZSH_VERSION}

WHAT HAPPENED:
[Describe the specific error or problem encountered]
- Error message: 
- Command/action that failed: 
- Expected behavior vs actual behavior: 

WHY IT HAPPENED:
[Root cause analysis - what led to this error]
- Primary cause: 
- Contributing factors: 
- Environment conditions: 

HOW TO RESOLVE:
[Step-by-step solution that works]
1. 
2. 
3. 

VERIFICATION:
[How to confirm the fix works]
- Test command: 
- Expected result: 

PREVENTION:
[How to avoid this error in the future]
- Configuration changes: 
- Best practices: 
- Monitoring setup: 

RELATED ERRORS:
[Links to similar errors if any]
- Related error IDs: 

STATUS: ONGOING
RESOLUTION_DATE: 
RESOLUTION_METHOD: 

=====================================

EOF
}

update_error_index() {
    local error_id=$1
    local description=$2
    local env=$3
    
    local index_file="${ERROR_LOG_DIR}/error-index.md"
    
    # Create index if it doesn't exist
    if [[ ! -f "$index_file" ]]; then
        cat > "$index_file" << EOF
# Error Documentation Index

**Academic Error Tracking System**  
*Master's Data Science Program - University of Arizona*

## Summary Statistics

- **Total Errors Documented**: 0
- **Resolved Errors**: 0  
- **Ongoing Errors**: 0
- **Last Updated**: $(date -Iseconds)

## Errors by Environment

### Terminal Errors (terminal-errors.txt)
======================================
[No errors documented yet]

### Python Errors (python-errors.txt)
=====================================
[No errors documented yet]

### VS Code Errors (vscode-errors.txt)
======================================
[No errors documented yet]

### System Errors (system-errors.txt)
=====================================
[No errors documented yet]

### Database Errors (database-errors.txt)
=========================================
[No errors documented yet]

## Usage

To document a new error:
\`\`\`bash
./log-error.sh [environment] [description]
\`\`\`

To update error status:
\`\`\`bash  
./update-status.sh [error-id] [RESOLVED|ONGOING]
\`\`\`

To list errors:
\`\`\`bash
./list-errors.sh [--environment] [--status]
\`\`\`

EOF
    fi
    
    # Update the index with new error
    local section_line=$(grep -n "### ${env^} Errors" "$index_file" | cut -d: -f1)
    if [[ -n "$section_line" ]]; then
        local next_line=$((section_line + 2))
        if grep -q "\[No errors documented yet\]" "$index_file"; then
            sed -i '' "${next_line}s/\[No errors documented yet\]/${error_id}: ${description} [ONGOING] - ${DATE_ONLY}/" "$index_file"
        else
            sed -i '' "${next_line}i\\
${error_id}: ${description} [ONGOING] - ${DATE_ONLY}
" "$index_file"
        fi
    fi
    
    # Update statistics
    local total_errors=$(find "${ERROR_LOG_DIR}" -name "*-errors.txt" -exec grep -c "^ERROR.*:" {} \; 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
    local resolved_errors=$(find "${ERROR_LOG_DIR}" -name "*-errors.txt" -exec grep -c "STATUS: RESOLVED" {} \; 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
    local ongoing_errors=$((total_errors - resolved_errors))
    
    sed -i '' "s/Total Errors Documented\*\*: [0-9]*/Total Errors Documented**: $total_errors/" "$index_file"
    sed -i '' "s/Resolved Errors\*\*: [0-9]*/Resolved Errors**: $resolved_errors/" "$index_file"  
    sed -i '' "s/Ongoing Errors\*\*: [0-9]*/Ongoing Errors**: $ongoing_errors/" "$index_file"
    sed -i '' "s/Last Updated\*\*: .*/Last Updated**: $(date -Iseconds)/" "$index_file"
}

# Main script logic
if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

if [[ $# -lt 2 ]]; then
    echo "${RED}Error: Missing arguments${NC}"
    echo "Usage: ./log-error.sh [environment] [description]"
    echo "Run './log-error.sh --help' for more information"
    exit 1
fi

ENVIRONMENT=$1
DESCRIPTION=$2

# Validate environment
case $ENVIRONMENT in
    terminal|python|vscode|system|database) ;;
    *) 
        echo "${RED}Error: Invalid environment '$ENVIRONMENT'${NC}"
        echo "Supported: terminal, python, vscode, system, database"
        exit 1 
        ;;
esac

# Generate unique error ID
ERROR_ID=$(get_next_error_id "$ENVIRONMENT")

echo "${BLUE}Creating error documentation...${NC}"
echo "Environment: $ENVIRONMENT"
echo "Error ID: $ERROR_ID" 
echo "Description: $DESCRIPTION"
echo ""

# Create error documentation entry
create_error_entry "$ENVIRONMENT" "$DESCRIPTION" "$ERROR_ID"

# Update the master index
update_error_index "$ERROR_ID" "$DESCRIPTION" "$ENVIRONMENT"

echo "${GREEN}Error documented successfully!${NC}"
echo ""
echo "${YELLOW}Next steps:${NC}"
echo "1. Edit: ${ERROR_LOG_DIR}/${ENVIRONMENT}-errors.txt"
echo "2. Fill in details for error ${ERROR_ID}"
echo "3. When resolved, run: ${BLUE}./update-status.sh ${ERROR_ID} RESOLVED${NC}"
echo ""
echo "${BLUE}Quick edit command:${NC}"
echo "code ${ERROR_LOG_DIR}/${ENVIRONMENT}-errors.txt"

# Show location of files
echo ""
echo "${BLUE}Files created/updated:${NC}"
echo "  Error log: ${ERROR_LOG_DIR}/${ENVIRONMENT}-errors.txt"
echo "  Index: ${ERROR_LOG_DIR}/error-index.md"