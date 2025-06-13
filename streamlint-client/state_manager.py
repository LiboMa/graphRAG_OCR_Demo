import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class StateManager:
    """Manages saving and loading application state to/from local files."""
    
    def __init__(self, state_dir: str = "app_state"):
        """Initialize state manager with specified directory."""
        self.state_dir = state_dir
        self.state_file = os.path.join(state_dir, "app_state.json")
        self.agent_status_file = os.path.join(state_dir, "agent_status.json")
        self.session_file = os.path.join(state_dir, "session_data.json")
        
        # Create state directory if it doesn't exist
        os.makedirs(state_dir, exist_ok=True)
    
    def save_agent_status(self, agent_id: str, status: str, timestamp: Optional[datetime] = None) -> bool:
        """Save agent status to file."""
        try:
            # Load existing status data
            status_data = self.load_agent_status_data()
            
            # Update with new status
            if timestamp is None:
                timestamp = datetime.now()
            
            status_data[agent_id] = {
                "status": status,
                "last_checked": timestamp.isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Save to file
            with open(self.agent_status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving agent status: {e}")
            return False
    
    def load_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load agent status from file."""
        try:
            status_data = self.load_agent_status_data()
            return status_data.get(agent_id)
        except Exception as e:
            print(f"Error loading agent status: {e}")
            return None
    
    def load_agent_status_data(self) -> Dict[str, Any]:
        """Load all agent status data."""
        try:
            if os.path.exists(self.agent_status_file):
                with open(self.agent_status_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}
    
    def save_session_state(self, session_data: Dict[str, Any]) -> bool:
        """Save session state to file."""
        try:
            # Add timestamp
            session_data["saved_at"] = datetime.now().isoformat()
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving session state: {e}")
            return False
    
    def load_session_state(self) -> Optional[Dict[str, Any]]:
        """Load session state from file."""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading session state: {e}")
            return None
    
    def save_app_state(self, state_data: Dict[str, Any]) -> bool:
        """Save general application state."""
        try:
            state_data["saved_at"] = datetime.now().isoformat()
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving app state: {e}")
            return False
    
    def load_app_state(self) -> Optional[Dict[str, Any]]:
        """Load general application state."""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading app state: {e}")
            return None
    
    def clear_state(self) -> bool:
        """Clear all saved state files."""
        try:
            files_to_remove = [self.state_file, self.agent_status_file, self.session_file]
            
            for file_path in files_to_remove:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            return True
        except Exception as e:
            print(f"Error clearing state: {e}")
            return False
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get information about saved state files."""
        info = {
            "state_directory": self.state_dir,
            "files": {}
        }
        
        files_to_check = {
            "app_state": self.state_file,
            "agent_status": self.agent_status_file,
            "session_data": self.session_file
        }
        
        for name, file_path in files_to_check.items():
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                info["files"][name] = {
                    "exists": True,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
            else:
                info["files"][name] = {"exists": False}
        
        return info
