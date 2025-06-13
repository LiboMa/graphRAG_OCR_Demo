# 💾 State Management Feature

## Overview
The application now includes persistent state management that saves your preferences, agent status, and session information to local files in the current folder.

## 📁 State Files Structure
```
streamlint-client/
├── app_state/                    # State directory
│   ├── app_state.json           # General app preferences
│   ├── agent_status.json        # Agent status cache
│   └── session_data.json        # Session information
├── app.py
├── state_manager.py             # State management module
└── ...
```

## 🔧 Features

### 1. Agent Status Caching
- **Automatic saving**: Agent status is saved after each check
- **Fast loading**: Cached status loads instantly on startup
- **Timestamp tracking**: Knows when each agent was last checked

### 2. Application Preferences
- **Selected agent**: Remembers your last selected agent
- **Custom agent ID**: Saves custom agent configurations
- **Session continuity**: Maintains session context

### 3. Manual State Control
- **Save button**: Manually save current state
- **Clear state**: Remove all saved state files
- **State info**: View information about saved files

## 🎯 How It Works

### Automatic State Saving
```python
# Status is automatically saved when:
- Agent status is checked (auto or manual)
- Agent is switched
- Custom agent ID is entered
- Chat is cleared or new session started
```

### State Loading
```python
# State is automatically loaded when:
- Application starts
- Cached agent status is restored
- Previous agent selection is restored
- Custom agent ID is restored
```

## 📋 State File Contents

### app_state.json
```json
{
  "selected_agent": "GraphRAG+Neptune",
  "custom_agent_id": "",
  "session_id": "abc123def456",
  "messages_count": 5,
  "saved_at": "2024-06-12T14:30:25.123456"
}
```

### agent_status.json
```json
{
  "WN79XAAFL6": {
    "status": "✅ Available",
    "last_checked": "2024-06-12T14:30:20.123456",
    "updated_at": "2024-06-12T14:30:25.123456"
  },
  "ZUJPK3HE6I": {
    "status": "✅ Available",
    "last_checked": "2024-06-12T14:25:15.123456",
    "updated_at": "2024-06-12T14:25:20.123456"
  }
}
```

## 🎮 User Interface

### Sidebar Controls
```
💾 State Management
├── [💾 Save]     - Manually save current state
├── [🗑️ Clear State] - Remove all saved files
└── 📁 State Files Info
    ├── app_state: ✅ 245 bytes
    ├── agent_status: ✅ 312 bytes
    └── session_data: ❌ Not found
```

### Status Indicators
- **✅ Available**: Status loaded from cache
- **🔄 Checking...**: Status being verified
- **💾 Saved**: State successfully saved
- **❌ Error**: Failed to save/load

## 🔧 Technical Implementation

### StateManager Class
```python
from state_manager import StateManager

# Initialize
state_manager = StateManager()

# Save agent status
state_manager.save_agent_status("AGENT_ID", "✅ Available")

# Load agent status
status = state_manager.load_agent_status("AGENT_ID")

# Save app state
state_manager.save_app_state({"selected_agent": "GraphRAG+Neptune"})

# Load app state
state = state_manager.load_app_state()
```

### Integration Points
```python
# Auto-save on status check
def auto_check_agent_status():
    # ... check logic ...
    state_manager.save_agent_status(agent_id, status, timestamp)

# Auto-save on agent switch
def update_agent_configuration():
    # ... update logic ...
    save_current_state()

# Load on startup
def initialize_session_state():
    saved_state = state_manager.load_app_state()
    # ... use saved_state to restore preferences ...
```

## 🚀 Benefits

### 1. Faster Startup
- **Cached status**: No need to re-check agent status
- **Restored preferences**: Continues where you left off
- **Instant feedback**: Shows last known status immediately

### 2. Better User Experience
- **Persistent settings**: Remembers your preferences
- **Session continuity**: Maintains context across restarts
- **Offline capability**: Works with cached data

### 3. Debugging & Monitoring
- **Status history**: Track agent availability over time
- **State inspection**: View saved state files
- **Manual control**: Save/clear state as needed

## 🛠️ Usage Examples

### Example 1: Check Saved Status
```bash
cd streamlint-client
python state_example.py
```

### Example 2: Manual State Management
```python
# In the app sidebar:
1. Click "💾 Save" to save current state
2. Click "🗑️ Clear State" to remove saved files
3. Expand "📁 State Files Info" to view file details
```

### Example 3: Programmatic Access
```python
from state_manager import StateManager

state_manager = StateManager()

# Get all state info
info = state_manager.get_state_info()
print(f"State directory: {info['state_directory']}")

# Clear all state
state_manager.clear_state()
```

## 🔍 Troubleshooting

### Common Issues

1. **State not saving**
   - Check file permissions in current directory
   - Ensure `app_state/` directory can be created
   - Look for error messages in console

2. **State not loading**
   - Verify state files exist in `app_state/` directory
   - Check JSON file format is valid
   - Clear state and restart if corrupted

3. **Performance issues**
   - State files are small and shouldn't impact performance
   - Clear old state files if they become too large
   - Check disk space availability

### Debug Commands
```bash
# Check state files
ls -la app_state/

# View state content
cat app_state/app_state.json
cat app_state/agent_status.json

# Remove state files
rm -rf app_state/
```

## 📝 Configuration

### Custom State Directory
```python
# Use custom directory
state_manager = StateManager("my_custom_state")
```

### Disable State Management
```python
# To disable, simply don't call save functions
# The app will work normally without persistence
```

## 🔒 Security Notes

- State files contain agent IDs and preferences (no sensitive data)
- Files are stored locally in the application directory
- No network transmission of state data
- Clear state files before sharing the application folder

## 🎉 Summary

The state management feature provides:
- **Persistent agent status caching**
- **Automatic preference saving**
- **Manual state control**
- **Fast application startup**
- **Better user experience**

All state is saved locally in the `app_state/` directory and can be managed through the sidebar interface or programmatically using the StateManager class.
