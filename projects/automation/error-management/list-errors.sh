#!/usr/bin/env zsh

# ERROR LISTING UTILITY
# ====================
# Academic project utility for viewing documented errors
#
# Author: Matthew Thompson
# Course: Master's Data Science Program
# Institution: University of Arizona

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERROR_LOG_DIR="${SCRIPT_DIR}/logs"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

show_help() {
    echo "${BLUE}ERROR LISTING UTILITY${NC}"
    echo "===================="
    echo "Usage: ./list-errors.sh [options]"
    echo ""
    echo "Options:"
    echo "  --all         Show all errors (default)"
    echo "  --ongoing     Show only ongoing errors"
    echo "  --resolved    Show only resolved errors"
    echo "  --terminal    Show only terminal errors"
    echo "  --python      Show only Python errors"
    echo "  --vscode      Show only VS Code errors"
    echo "  --system      Show only system errors"
    echo "  --database    Show only database errors"
    echo "  --summary     Show summary statistics only"
    echo "  --help        Show this help message"
}

list_errors() {
    local filter_status="$1"
    local filter_env="$2"
    
    if [[ ! -d "$ERROR_LOG_DIR" ]]; then
        echo "${YELLOW}No error logs directory found. Run log-error.sh first.${NC}"
        return
    fi
    
    local files=()
    if [[ -n "$filter_env" ]]; then
        if [[ -f "${ERROR_LOG_DIR}/${filter_env}-errors.txt" ]]; then
            files=("${ERROR_LOG_DIR}/${filter_env}-errors.txt")
        fi
    else
        files=($(find "$ERROR_LOG_DIR" -name "*-errors.txt" 2>/dev/null))
    fi
    
    if [[ ${#files[@]} -eq 0 ]]; then
        echo "${YELLOW}No error files found.${NC}"
        return
    fi
    
    local total_count=0
    
    for file in "${files[@]}"; do
        if [[ ! -f "$file" ]]; then continue; fi
        
        local env=$(basename "$file" | sed 's/-errors.txt//')
        echo "${BLUE}=== ${env^^} ENVIRONMENT ERRORS ===${NC}"
        
        local count=0
        while IFS= read -r line; do
            if [[ "$line" =~ ^ERROR\ ([^:]+):\ (.+)$ ]]; then
                local error_id="${match[1]}"
                local description="${match[2]}"
                
                # Read ahead to find status
                local status="UNKNOWN"
                local temp_file=$(mktemp)
                local found_error=false
                local in_error=false
                
                while IFS= read -r status_line; do
                    if [[ "$status_line" =~ ^ERROR\ $error_id: ]]; then
                        in_error=true
                    elif [[ "$status_line" =~ ^ERROR\ .*: ]] && [[ "$in_error" == true ]]; then
                        break
                    elif [[ "$status_line" =~ ^STATUS:\ (.+)$ ]] && [[ "$in_error" == true ]]; then
                        status="${match[1]}"
                        found_error=true
                        break
                    fi
                done < "$file"
                
                # Apply status filter
                if [[ -n "$filter_status" ]]; then
                    if [[ "$filter_status" == "ongoing" && "$status" != "ONGOING" ]]; then
                        continue
                    elif [[ "$filter_status" == "resolved" && "$status" != "RESOLVED" ]]; then
                        continue
                    fi
                fi
                
                # Display error
                local status_color=""
                case "$status" in
                    "ONGOING") status_color="$RED" ;;
                    "RESOLVED") status_color="$GREEN" ;;
                    *) status_color="$YELLOW" ;;
                esac
                
                printf "  ${status_color}%-8s${NC} %s: %s\n" "$status" "$error_id" "$description"
                ((count++))
                ((total_count++))
            fi
        done < "$file"
        
        if [[ $count -eq 0 ]]; then
            echo "  ${YELLOW}No errors found${NC}"
        else
            echo "  ${BLUE}Total: $count errors${NC}"
        fi
        echo ""
    done
    
    echo "${BLUE}Overall Total: $total_count errors${NC}"
}

show_summary() {
    if [[ ! -d "$ERROR_LOG_DIR" ]]; then
        echo "${YELLOW}No error logs found.${NC}"
        return
    fi
    
    echo "${BLUE}ERROR DOCUMENTATION SUMMARY${NC}"
    echo "==========================="
    
    local total_errors=0
    local resolved_errors=0
    local ongoing_errors=0
    
    for file in "${ERROR_LOG_DIR}"/*-errors.txt; do
        if [[ -f "$file" ]]; then
            local env=$(basename "$file" | sed 's/-errors.txt//')
            local env_total=$(grep -c "^ERROR.*:" "$file" 2>/dev/null || echo "0")
            local env_resolved=$(grep -c "STATUS: RESOLVED" "$file" 2>/dev/null || echo "0")
            local env_ongoing=$((env_total - env_resolved))
            
            total_errors=$((total_errors + env_total))
            resolved_errors=$((resolved_errors + env_resolved))
            ongoing_errors=$((ongoing_errors + env_ongoing))
            
            if [[ $env_total -gt 0 ]]; then
                printf "%-10s: %2d total, %2d resolved, %2d ongoing\n" \
                       "${env^^}" "$env_total" "$env_resolved" "$env_ongoing"
            fi
        fi
    done
    
    echo "------------------------"
    printf "%-10s: %2d total, %2d resolved, %2d ongoing\n" \
           "OVERALL" "$total_errors" "$resolved_errors" "$ongoing_errors"
}

# Main script logic
case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --summary)
        show_summary
        ;;
    --all)
        list_errors "" ""
        ;;
    --ongoing)
        list_errors "ongoing" ""
        ;;
    --resolved)
        list_errors "resolved" ""
        ;;
    --terminal)
        list_errors "" "terminal"
        ;;
    --python)
        list_errors "" "python"
        ;;
    --vscode)
        list_errors "" "vscode"
        ;;
    --system)
        list_errors "" "system"
        ;;
    --database)
        list_errors "" "database"
        ;;
    "")
        list_errors "" ""
        ;;
    *)
        echo "${RED}Unknown option: $1${NC}"
        show_help
        exit 1
        ;;
esac