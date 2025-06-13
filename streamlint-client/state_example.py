#!/usr/bin/env python3
"""
Example script showing how to use the StateManager
"""

from state_manager import StateManager
from datetime import datetime

def main():
    # Initialize state manager
    state_manager = StateManager()
    
    print("🔧 State Manager Example")
    print("=" * 40)
    
    # Example 1: Save agent status
    print("\n1. Saving agent status...")
    agent_id = "WN79XAAFL6"
    status = "✅ Available"
    success = state_manager.save_agent_status(agent_id, status)
    print(f"   Saved: {success}")
    
    # Example 2: Load agent status
    print("\n2. Loading agent status...")
    loaded_status = state_manager.load_agent_status(agent_id)
    if loaded_status:
        print(f"   Agent ID: {agent_id}")
        print(f"   Status: {loaded_status['status']}")
        print(f"   Last checked: {loaded_status['last_checked']}")
    else:
        print("   No status found")
    
    # Example 3: Save app state
    print("\n3. Saving app state...")
    app_state = {
        "selected_agent": "GraphRAG+Neptune",
        "custom_agent_id": "",
        "session_id": "abc123",
        "messages_count": 5
    }
    success = state_manager.save_app_state(app_state)
    print(f"   Saved: {success}")
    
    # Example 4: Load app state
    print("\n4. Loading app state...")
    loaded_state = state_manager.load_app_state()
    if loaded_state:
        print(f"   Selected agent: {loaded_state['selected_agent']}")
        print(f"   Session ID: {loaded_state['session_id']}")
        print(f"   Messages count: {loaded_state['messages_count']}")
        print(f"   Saved at: {loaded_state['saved_at']}")
    else:
        print("   No app state found")
    
    # Example 5: Get state info
    print("\n5. State files information...")
    state_info = state_manager.get_state_info()
    print(f"   State directory: {state_info['state_directory']}")
    
    for file_name, file_info in state_info["files"].items():
        if file_info["exists"]:
            print(f"   {file_name}: ✅ {file_info['size']} bytes")
        else:
            print(f"   {file_name}: ❌ Not found")
    
    print("\n" + "=" * 40)
    print("✅ Example completed!")

if __name__ == "__main__":
    main()
