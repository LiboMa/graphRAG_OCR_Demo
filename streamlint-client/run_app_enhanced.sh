#!/bin/bash

# Enhanced Bedrock Agent Chat Interface Launch Script with Process Management
# Supports background execution and process management

set -e  # Exit on any error

# Configuration
APP_NAME="Bedrock Agent Chat"
APP_FILE="app.py"
DEFAULT_PORT=8501
DEFAULT_HOST="0.0.0.0"
PID_FILE="streamlit.pid"
LOG_DIR="logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  start     Start the application (default)"
    echo "  stop      Stop the running application"
    echo "  restart   Restart the application"
    echo "  status    Show application status"
    echo "  logs      Show application logs"
    echo "  setup     Setup environment only"
    echo ""
    echo "Options:"
    echo "  --port PORT       Port number (default: 8501)"
    echo "  --host HOST       Host address (default: 0.0.0.0)"
    echo "  --foreground      Run in foreground (default: background)"
    echo "  --app APP_FILE    Streamlit app file (default: app.py)"
    echo "  --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start --port 8502 --foreground"
    echo "  $0 stop"
    echo "  $0 status"
    echo "  $0 logs"
}

# Function to check if virtual environment exists and create if needed
setup_venv() {
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_status "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
}

# Function to activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_status "Virtual environment activated"
}

# Function to install dependencies
install_deps() {
    print_info "Installing/updating dependencies..."
    pip install -r requirements.txt
    
    # Install additional dependencies for process management
    pip install psutil
    
    print_status "Dependencies installed"
}

# Function to check AWS credentials
check_aws_credentials() {
    print_info "Checking AWS credentials..."
    if ! aws sts get-caller-identity > /dev/null 2>&1; then
        print_error "AWS credentials not configured!"
        echo "Please configure AWS credentials using one of these methods:"
        echo "1. Run: aws configure"
        echo "2. Set environment variables:"
        echo "   export AWS_ACCESS_KEY_ID=your_key"
        echo "   export AWS_SECRET_ACCESS_KEY=your_secret"
        echo "   export AWS_DEFAULT_REGION=us-west-2"
        echo "3. Use IAM roles (if running on EC2)"
        exit 1
    fi
    print_status "AWS credentials configured"
}

# Function to setup authentication config
setup_auth_config() {
    if [ ! -f "auth_config.json" ]; then
        print_info "Creating default authentication configuration..."
        print_warning "Default users will be created:"
        echo "  - admin / bedrock2024 (Admin)"
        echo "  - user1 / demo123 (User)"
    fi
}

# Function to check if application is running
is_running() {
    python3 -c "
from process_manager import ProcessManager
pm = ProcessManager()
exit(0 if pm.is_running() else 1)
" 2>/dev/null
}

# Function to start the application
start_app() {
    local port=$1
    local host=$2
    local foreground=$3
    local app_file=$4
    
    print_info "Starting $APP_NAME..."
    
    if is_running; then
        print_warning "$APP_NAME is already running"
        python3 -c "
from process_manager import ProcessManager
pm = ProcessManager()
status = pm.get_status()
print(f\"PID: {status.get('pid', 'N/A')}\")
print(f\"Port: {status.get('port', 'N/A')}\")
print(f\"Started: {status.get('started_at', 'N/A')}\")
"
        return 0
    fi
    
    # Create logs directory
    mkdir -p "$LOG_DIR"
    
    if [ "$foreground" = "true" ]; then
        print_info "Starting in foreground mode..."
        print_info "Press Ctrl+C to stop the application"
        python3 -c "
from process_manager import ProcessManager
pm = ProcessManager()
success, message = pm.start_streamlit(
    app_file='$app_file',
    port=$port,
    host='$host',
    background=False
)
print(message)
exit(0 if success else 1)
"
    else
        print_info "Starting in background mode..."
        python3 -c "
from process_manager import ProcessManager
pm = ProcessManager()
success, message = pm.start_streamlit(
    app_file='$app_file',
    port=$port,
    host='$host',
    background=True
)
print(message)
exit(0 if success else 1)
"
        if [ $? -eq 0 ]; then
            print_status "$APP_NAME started successfully!"
            print_info "Access the application at: http://$host:$port"
            print_info "Use '$0 stop' to stop the application"
            print_info "Use '$0 logs' to view logs"
            print_info "Use '$0 status' to check status"
            
            echo ""
            print_warning "Default Login Credentials:"
            echo "  Username: admin    | Password: bedrock2024 (Admin)"
            echo "  Username: user1    | Password: demo123     (User)"
        fi
    fi
}

# Function to stop the application
stop_app() {
    print_info "Stopping $APP_NAME..."
    python3 -c "
from process_manager import ProcessManager
pm = ProcessManager()
success, message = pm.stop_streamlit()
print(message)
exit(0 if success else 1)
"
}

# Function to restart the application
restart_app() {
    local port=$1
    local host=$2
    local foreground=$3
    local app_file=$4
    
    print_info "Restarting $APP_NAME..."
    python3 -c "
from process_manager import ProcessManager
pm = ProcessManager()
success, message = pm.restart_streamlit(
    app_file='$app_file',
    port=$port,
    host='$host',
    background=$([ '$foreground' = 'true' ] && echo 'False' || echo 'True')
)
print(message)
exit(0 if success else 1)
"
    
    if [ $? -eq 0 ] && [ "$foreground" != "true" ]; then
        print_status "$APP_NAME restarted successfully!"
        print_info "Access the application at: http://$host:$port"
    fi
}

# Function to show application status
show_status() {
    print_info "Checking $APP_NAME status..."
    python3 -c "
import json
from process_manager import ProcessManager
pm = ProcessManager()
status = pm.get_status()
print(json.dumps(status, indent=2))
"
}

# Function to show logs
show_logs() {
    local log_type=${1:-stdout}
    local lines=${2:-50}
    
    print_info "Showing $APP_NAME logs ($log_type, last $lines lines)..."
    python3 -c "
from process_manager import ProcessManager
pm = ProcessManager()
logs = pm.get_logs(log_type='$log_type', lines=$lines)
for line in logs:
    print(line)
"
}

# Function to setup environment
setup_environment() {
    print_info "Setting up environment for $APP_NAME..."
    
    setup_venv
    activate_venv
    install_deps
    check_aws_credentials
    setup_auth_config
    
    print_status "Environment setup completed!"
}

# Parse command line arguments
COMMAND="start"
PORT=$DEFAULT_PORT
HOST=$DEFAULT_HOST
FOREGROUND="false"
APP_FILE_ARG=$APP_FILE

while [[ $# -gt 0 ]]; do
    case $1 in
        start|stop|restart|status|logs|setup)
            COMMAND="$1"
            shift
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --foreground)
            FOREGROUND="true"
            shift
            ;;
        --app)
            APP_FILE_ARG="$2"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
echo "🔐 $APP_NAME - Enhanced Process Manager"
echo "========================================"

case $COMMAND in
    setup)
        setup_environment
        ;;
    start)
        setup_environment
        start_app "$PORT" "$HOST" "$FOREGROUND" "$APP_FILE_ARG"
        ;;
    stop)
        activate_venv
        stop_app
        ;;
    restart)
        activate_venv
        restart_app "$PORT" "$HOST" "$FOREGROUND" "$APP_FILE_ARG"
        ;;
    status)
        activate_venv
        show_status
        ;;
    logs)
        activate_venv
        show_logs
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        show_usage
        exit 1
        ;;
esac
