# Enhanced Features - Agent Configuration & Process Management

This document describes the enhanced features added to the Bedrock Agent Chat Interface, including dynamic agent configuration loading and background process management.

## 🔧 New Features

### 1. Dynamic Agent Configuration Loading
- **Configuration File**: `agent_config.json` is now dynamically loaded
- **Hot Reload**: Configuration changes are detected automatically
- **Validation**: Built-in configuration validation and error handling
- **Fallback**: Graceful fallback to default configuration if file is invalid

### 2. Background Process Management
- **Background Execution**: Run Streamlit in the background as a daemon
- **Process Control**: Start, stop, restart, and monitor the application
- **Log Management**: Separate stdout/stderr logs with rotation
- **Status Monitoring**: Real-time process status and resource usage

### 3. Enhanced Management Tools
- **CLI Management**: Command-line interface for all operations
- **Configuration Management**: Add, remove, and modify agent configurations
- **Process Monitoring**: Detailed process information and logs

## 🚀 Usage

### Quick Start with Enhanced Script

```bash
# Start in background (default)
./run_app_enhanced.sh start

# Start in foreground
./run_app_enhanced.sh start --foreground

# Start on different port
./run_app_enhanced.sh start --port 8502

# Stop the application
./run_app_enhanced.sh stop

# Check status
./run_app_enhanced.sh status

# View logs
./run_app_enhanced.sh logs
```

### Using the Management CLI

```bash
# Application management
python3 manage.py app start --port 8501
python3 manage.py app stop
python3 manage.py app restart
python3 manage.py app status
python3 manage.py app logs --lines 100

# Configuration management
python3 manage.py config list
python3 manage.py config show "GraphRAG+Neptune"
python3 manage.py config add "My Agent" --id AGENT123 --region us-east-1
python3 manage.py config remove "My Agent"
python3 manage.py config set-default "GraphRAG+Neptune"
python3 manage.py config validate
```

### Direct Process Management

```python
from process_manager import ProcessManager

pm = ProcessManager()

# Start application
success, message = pm.start_streamlit(
    app_file="app.py",
    port=8501,
    host="0.0.0.0",
    background=True
)

# Check status
status = pm.get_status()
print(f"Status: {status['status']}")
print(f"PID: {status.get('pid', 'N/A')}")

# Stop application
success, message = pm.stop_streamlit()
```

### Dynamic Configuration Loading

```python
from config_loader import ConfigLoader

loader = ConfigLoader()

# Load configuration
config = loader.load_config()
agents = config["agents"]

# Get specific agent
agent_config = loader.get_agent_config("GraphRAG+Neptune")

# Add new agent
new_agent = {
    "id": "NEWAGENT123",
    "alias": "PROD",
    "description": "Production agent",
    "region": "us-east-1",
    "capabilities": ["Production", "Support"]
}
loader.add_agent("Production Agent", new_agent)
```

## 📁 New File Structure

```
streamlint-client/
├── config_loader.py          # Dynamic configuration loading
├── process_manager.py         # Background process management
├── manage.py                  # CLI management tool
├── run_app_enhanced.sh        # Enhanced launch script
├── logs/                      # Log directory (auto-created)
│   ├── process_manager.log    # Process manager logs
│   ├── streamlit_stdout_*.log # Application stdout logs
│   └── streamlit_stderr_*.log # Application stderr logs
├── streamlit.pid              # Process ID file (auto-created)
└── ENHANCED_FEATURES.md       # This documentation
```

## 🔧 Configuration Management

### Agent Configuration Structure

```json
{
  "agents": {
    "Agent Name": {
      "id": "AGENT_ID",
      "alias": "AGENT_ALIAS",
      "description": "Agent description",
      "region": "us-west-2",
      "capabilities": ["Feature1", "Feature2"]
    }
  },
  "default_agent": "Agent Name",
  "default_region": "us-west-2"
}
```

### Adding New Agents

1. **Via CLI**:
   ```bash
   python3 manage.py config add "My New Agent" \
     --id MYNEWAGENT123 \
     --region us-east-1 \
     --description "My custom agent" \
     --capabilities "Feature1" "Feature2"
   ```

2. **Via JSON file**: Edit `agent_config.json` directly

3. **Programmatically**:
   ```python
   from config_loader import config_loader
   
   agent_config = {
       "id": "AGENT123",
       "alias": "PROD",
       "description": "Production agent",
       "region": "us-east-1",
       "capabilities": ["Production"]
   }
   config_loader.add_agent("Production Agent", agent_config)
   ```

## 🔍 Process Monitoring

### Status Information

The process manager provides detailed status information:

```json
{
  "status": "running",
  "pid": 12345,
  "started_at": "2024-07-22T09:00:00",
  "port": 8501,
  "host": "0.0.0.0",
  "app_file": "app.py",
  "cpu_percent": 2.5,
  "memory_info": {
    "rss": 125829120,
    "vms": 234567890
  },
  "create_time": "2024-07-22T09:00:00",
  "stdout_log": "logs/streamlit_stdout_20240722_090000.log",
  "stderr_log": "logs/streamlit_stderr_20240722_090000.log"
}
```

### Log Management

- **Automatic Rotation**: New log files created for each session
- **Separate Streams**: stdout and stderr logged separately
- **Timestamped**: Log files include timestamp in filename
- **Configurable**: Number of log lines to display is configurable

## 🛠️ Advanced Usage

### Custom Configuration Files

```python
# Use custom configuration file
from config_loader import ConfigLoader

loader = ConfigLoader("my_custom_config.json")
config = loader.load_config()
```

### Custom Log Directory

```python
# Use custom log directory
from process_manager import ProcessManager

pm = ProcessManager(log_dir="my_logs")
```

### Environment-Specific Configurations

You can maintain different configuration files for different environments:

```bash
# Development
cp agent_config.json agent_config.dev.json

# Production
cp agent_config.json agent_config.prod.json

# Use specific config
CONFIG_FILE=agent_config.prod.json python3 app.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Configuration Loading Errors**:
   ```bash
   python3 manage.py config validate
   ```

2. **Process Management Issues**:
   ```bash
   python3 manage.py app status
   python3 manage.py app logs --type stderr
   ```

3. **Permission Issues**:
   ```bash
   chmod +x run_app_enhanced.sh
   chmod +x manage.py
   ```

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export PYTHONPATH=.
export LOG_LEVEL=DEBUG
python3 manage.py app start
```

## 🔒 Security Considerations

- **Process Isolation**: Background processes run with appropriate permissions
- **Log Security**: Sensitive information is not logged
- **Configuration Validation**: Input validation prevents malicious configurations
- **PID File Security**: Process ID files are created with restricted permissions

## 📈 Performance Benefits

- **Resource Efficiency**: Background mode uses fewer system resources
- **Better Monitoring**: Real-time process monitoring and resource usage
- **Log Management**: Efficient log rotation and storage
- **Configuration Caching**: Configuration is cached for better performance

## 🔄 Migration from Original Version

The enhanced version is fully backward compatible. To migrate:

1. **Keep existing files**: All existing files continue to work
2. **Use new features**: Start using `run_app_enhanced.sh` for new features
3. **Gradual adoption**: You can use both old and new scripts simultaneously

## 🤝 Contributing

When contributing to the enhanced features:

1. **Test both modes**: Ensure foreground and background modes work
2. **Validate configurations**: Test with various agent configurations
3. **Check process management**: Verify start/stop/restart functionality
4. **Update documentation**: Keep this file updated with new features
