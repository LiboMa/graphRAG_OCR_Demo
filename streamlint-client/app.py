import streamlit as st
import boto3
import os
import uuid
from datetime import datetime
from state_manager import StateManager

# Initialize state manager
state_manager = StateManager()

# Set page configuration
st.set_page_config(
    page_title="Bedrock Agent Chat",
    page_icon="🤖",
    layout="wide"
)

# Predefined Agent Configurations
AGENT_CONFIGS = {
    "GraphRAG+Neptune": {
        "id": "WN79XAAFL6",
        "alias": "TSTALIASID",
        "description": "GraphRAG with Neptune - Advanced knowledge graph analysis and document processing",
        "region": "us-west-2"
    },
    "Normal RAG+OpenSearch": {
        "id": "ZUJPK3HE6I", 
        "alias": "TSTALIASID",
        "description": "Traditional RAG with OpenSearch - Standard document retrieval and Q&A",
        "region": "us-west-2"
    },
    "Custom Agent": {
        "id": "",
        "alias": "TSTALIASID",
        "description": "Custom agent configuration - Enter your own Agent ID",
        "region": "us-west-2"
    }
}

# Default configuration
DEFAULT_AGENT_CONFIG = "Normal RAG+OpenSearch"

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    # Load saved app state if available
    saved_state = state_manager.load_app_state()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "selected_agent" not in st.session_state:
        # Try to load from saved state, otherwise use default
        st.session_state.selected_agent = (
            saved_state.get("selected_agent", DEFAULT_AGENT_CONFIG) 
            if saved_state else DEFAULT_AGENT_CONFIG
        )
    if "agent_id" not in st.session_state:
        st.session_state.agent_id = AGENT_CONFIGS[st.session_state.selected_agent]["id"]
    if "agent_alias" not in st.session_state:
        st.session_state.agent_alias = AGENT_CONFIGS[st.session_state.selected_agent]["alias"]
    if "region" not in st.session_state:
        st.session_state.region = AGENT_CONFIGS[st.session_state.selected_agent]["region"]
    if "custom_agent_id" not in st.session_state:
        st.session_state.custom_agent_id = (
            saved_state.get("custom_agent_id", "") 
            if saved_state else ""
        )
    if "agent_status" not in st.session_state:
        # Try to load cached status
        cached_status = state_manager.load_agent_status(st.session_state.agent_id)
        if cached_status:
            st.session_state.agent_status = cached_status["status"]
            # Parse the timestamp
            try:
                st.session_state.last_agent_check = datetime.fromisoformat(cached_status["last_checked"])
            except:
                st.session_state.last_agent_check = None
        else:
            st.session_state.agent_status = "🔄 Checking..."
            st.session_state.last_agent_check = None
    if "last_agent_check" not in st.session_state:
        st.session_state.last_agent_check = None
    if "app_initialized" not in st.session_state:
        st.session_state.app_initialized = False
    if "status_checking" not in st.session_state:
        st.session_state.status_checking = False

def get_bedrock_client(region):
    """Create and return a Bedrock Runtime client."""
    try:
        return boto3.client("bedrock-agent-runtime", region_name=region)
    except Exception as e:
        st.error(f"Error creating Bedrock client: {str(e)}")
        return None

def check_agent_status(client, agent_id, agent_alias, show_spinner=True):
    """Check if the agent is available and return status."""
    if not agent_id:
        return "❌ No Agent ID"
    
    try:
        if show_spinner:
            with st.spinner("🔍 Checking agent status..."):
                test_response = client.invoke_agent(
                    agentId=agent_id,
                    agentAliasId=agent_alias,
                    inputText="Hello",
                    sessionId=str(uuid.uuid4()),
                    enableTrace=False
                )
        else:
            test_response = client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias,
                inputText="Hello",
                sessionId=str(uuid.uuid4()),
                enableTrace=False
            )
        return "✅ Available"
    except Exception as e:
        error_msg = str(e)
        if "ValidationException" in error_msg:
            return "❌ Invalid Configuration"
        elif "AccessDeniedException" in error_msg:
            return "🔒 Access Denied"
        elif "ResourceNotFoundException" in error_msg:
            return "❌ Agent Not Found"
        else:
            return f"❌ Error: {error_msg[:50]}..."

def auto_check_agent_status():
    """Automatically check agent status when needed."""
    if (st.session_state.agent_id and 
        st.session_state.agent_status in ["Unknown", "🔄 Checking..."] and
        not st.session_state.status_checking):
        
        st.session_state.status_checking = True
        client = get_bedrock_client(st.session_state.region)
        if client:
            status = check_agent_status(
                client, 
                st.session_state.agent_id, 
                st.session_state.agent_alias,
                show_spinner=False
            )
            st.session_state.agent_status = status
            st.session_state.last_agent_check = datetime.now()
            
            # Save status to file
            state_manager.save_agent_status(
                st.session_state.agent_id, 
                status, 
                st.session_state.last_agent_check
            )
            
        st.session_state.status_checking = False
        return True
    return False

def save_current_state():
    """Save current application state to file."""
    state_data = {
        "selected_agent": st.session_state.selected_agent,
        "custom_agent_id": st.session_state.custom_agent_id,
        "session_id": st.session_state.session_id,
        "messages_count": len(st.session_state.messages)
    }
    return state_manager.save_app_state(state_data)

def update_agent_configuration(selected_agent, custom_id=None):
    """Update agent configuration based on selection."""
    if selected_agent == "Custom Agent" and custom_id:
        st.session_state.agent_id = custom_id
        st.session_state.agent_alias = AGENT_CONFIGS["Custom Agent"]["alias"]
        st.session_state.region = AGENT_CONFIGS["Custom Agent"]["region"]
    elif selected_agent in AGENT_CONFIGS:
        config = AGENT_CONFIGS[selected_agent]
        st.session_state.agent_id = config["id"]
        st.session_state.agent_alias = config["alias"]
        st.session_state.region = config["region"]
    
    # Reset session and status when agent changes
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.agent_status = "🔄 Checking..."  # Always auto-check
    st.session_state.last_agent_check = None
    st.session_state.status_checking = False
    
    # Save current state
    save_current_state()

def invoke_agent(client, prompt, session_id, agent_id, agent_alias):
    """Invoke the Bedrock agent with the given prompt."""
    try:
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias,
            inputText=prompt,
            sessionId=session_id,
            enableTrace=True
        )

        session_id = response.get("sessionId")

        response_text = ""
        for event in response.get("completion"):
            chunk = event.get("chunk", {}).get("bytes")
            if chunk:
                chunk_text = chunk.decode("utf-8")
                response_text += chunk_text

        return response_text, session_id
    except Exception as e:
        error_msg = f"Error invoking Bedrock agent: {str(e)}"
        st.error(error_msg)
        return error_msg, session_id

def render_agent_selector():
    """Render the agent selection dropdown."""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        selected_agent = st.selectbox(
            "🤖 Select Bedrock Agent:",
            options=list(AGENT_CONFIGS.keys()),
            index=list(AGENT_CONFIGS.keys()).index(st.session_state.selected_agent),
            key="agent_dropdown",
            help="Choose an agent to chat with. Status will be checked automatically."
        )
        
        # Handle agent change
        if selected_agent != st.session_state.selected_agent:
            st.session_state.selected_agent = selected_agent
            if selected_agent == "Custom Agent":
                update_agent_configuration(selected_agent, st.session_state.custom_agent_id)
            else:
                update_agent_configuration(selected_agent)
            st.success(f"✅ Switched to {selected_agent}")
            # Trigger auto-check after switch
            st.rerun()
    
    with col2:
        col2a, col2b = st.columns([3, 1])
        with col2a:
            # Show status with loading indicator if checking
            if st.session_state.status_checking:
                st.write("**Status:** 🔄 Checking...")
            else:
                st.write(f"**Status:** {st.session_state.agent_status}")
        with col2b:
            if st.button("🔄", key="refresh_status", help="Manual status check"):
                if st.session_state.agent_id:
                    st.session_state.status_checking = True
                    client = get_bedrock_client(st.session_state.region)
                    if client:
                        status = check_agent_status(
                            client, 
                            st.session_state.agent_id, 
                            st.session_state.agent_alias,
                            show_spinner=True
                        )
                        st.session_state.agent_status = status
                        st.session_state.last_agent_check = datetime.now()
                        
                        # Save status to file
                        state_manager.save_agent_status(
                            st.session_state.agent_id, 
                            status, 
                            st.session_state.last_agent_check
                        )
                        
                    st.session_state.status_checking = False
                    st.rerun()
    
    with col3:
        st.write(f"**Messages:** {len(st.session_state.messages)}")

def render_agent_info():
    """Render agent information and custom input if needed."""
    current_config = AGENT_CONFIGS.get(st.session_state.selected_agent, {})
    
    if current_config.get("description"):
        st.info(f"ℹ️ {current_config['description']}")
    
    if st.session_state.selected_agent == "Custom Agent":
        col1, col2 = st.columns([3, 1])
        
        with col1:
            custom_id = st.text_input(
                "Enter your Agent ID:",
                value=st.session_state.custom_agent_id,
                placeholder="e.g., ABCDEF1234",
                key="custom_agent_input",
                help="Enter the ID of your custom Bedrock agent"
            )
            
            if custom_id != st.session_state.custom_agent_id:
                st.session_state.custom_agent_id = custom_id
                update_agent_configuration("Custom Agent", custom_id)
                st.success("✅ Custom agent ID updated")
                # Trigger auto-check after custom ID change
                st.rerun()
        
        with col2:
            st.write("**Current Config:**")
            st.code(f"ID: {st.session_state.agent_id or 'Not set'}")
            st.code(f"Region: {st.session_state.region}")

def render_sidebar():
    """Render the sidebar with session management."""
    with st.sidebar:
        st.header("💬 Session & Status")
        
        # Combined session info and auto-check status
        st.subheader("📋 Current Configuration")
        config_info = {
            "Agent": st.session_state.selected_agent,
            "ID": st.session_state.agent_id or "Not set",
            "Alias": st.session_state.agent_alias,
            "Region": st.session_state.region,
            "Status": st.session_state.agent_status
        }
        
        for key, value in config_info.items():
            st.write(f"**{key}:** {value}")
        
        if st.session_state.last_agent_check:
            st.caption(f"Last checked: {st.session_state.last_agent_check.strftime('%H:%M:%S')}")
        
        # Auto-check status indicator (no checkbox)
        st.caption("🔄 Auto-check: Always enabled")
        
        st.divider()
        
        # Session controls
        st.subheader("🔧 Session Controls")
        st.write(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
        st.write(f"**Messages:** {len(st.session_state.messages)}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear", key="clear_chat", help="Clear all messages"):
                st.session_state.messages = []
                st.success("Chat cleared!")
                save_current_state()  # Save after clearing
                st.rerun()
        
        with col2:
            if st.button("🔄 New", key="new_session", help="Start new session"):
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.messages = []
                st.success("New session!")
                save_current_state()  # Save after new session
                st.rerun()
        
        st.divider()
        
        # State management section
        st.subheader("💾 State Management")
        
        # Show state info
        state_info = state_manager.get_state_info()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", key="save_state", help="Save current state"):
                if save_current_state():
                    st.success("State saved!")
                else:
                    st.error("Failed to save state")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear State", key="clear_state", help="Clear saved state"):
                if state_manager.clear_state():
                    st.success("State cleared!")
                else:
                    st.error("Failed to clear state")
                st.rerun()
        
        # Show state file info
        with st.expander("📁 State Files Info"):
            for file_name, file_info in state_info["files"].items():
                if file_info["exists"]:
                    st.write(f"**{file_name}:** ✅ {file_info['size']} bytes")
                    st.caption(f"Modified: {file_info['modified'][:19]}")
                else:
                    st.write(f"**{file_name}:** ❌ Not found")

def main():
    """Main function to run the Streamlit app."""
    initialize_session_state()

    st.title("🤖 Bedrock Agent Chat Interface")
    st.markdown("*Select an agent and start chatting - status checked automatically*")
    
    # Auto-check on first launch
    if not st.session_state.app_initialized:
        st.session_state.app_initialized = True
        st.session_state.agent_status = "🔄 Checking..."
    
    # Perform auto-check if needed
    if auto_check_agent_status():
        st.rerun()
    
    render_agent_selector()
    render_agent_info()
    render_sidebar()
    
    st.divider()

    if not st.session_state.agent_id:
        st.warning("⚠️ Please configure an Agent ID to start chatting.")
        if st.session_state.selected_agent == "Custom Agent":
            st.info("💡 Enter your custom Agent ID above.")
        else:
            st.info("💡 The selected agent configuration is missing an ID.")
        return

    bedrock_client = get_bedrock_client(st.session_state.region)
    if not bedrock_client:
        st.error("❌ Failed to initialize Bedrock client. Please check your AWS credentials.")
        st.info("💡 Configure AWS credentials via: AWS CLI, environment variables, or IAM roles.")
        return

    # Show warning if agent status is not available
    if st.session_state.agent_status not in ["✅ Available", "🔄 Checking..."]:
        st.warning(f"⚠️ Agent status: {st.session_state.agent_status}")
        st.info("💡 You can still try to chat, but the agent might not respond properly.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 Thinking...")

            session_id = st.session_state.session_id

            response, new_session_id = invoke_agent(
                bedrock_client,
                prompt,
                session_id,
                st.session_state.agent_id,
                st.session_state.agent_alias
            )

            if new_session_id:
                st.session_state.session_id = new_session_id

            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown("---")
    # st.markdown(
    #     "💡 **Tips:** "
    #     "Agent status is checked automatically • "
    #     "Use dropdown to switch agents instantly • "
    #     "Auto-check is always enabled for best experience"
    # )

if __name__ == "__main__":
    main()
