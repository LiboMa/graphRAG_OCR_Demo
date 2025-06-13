import streamlit as st
import boto3
import os
import uuid
import asyncio
import time
from datetime import datetime

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
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "selected_agent" not in st.session_state:
        st.session_state.selected_agent = DEFAULT_AGENT_CONFIG
    if "agent_id" not in st.session_state:
        st.session_state.agent_id = AGENT_CONFIGS[DEFAULT_AGENT_CONFIG]["id"]
    if "agent_alias" not in st.session_state:
        st.session_state.agent_alias = AGENT_CONFIGS[DEFAULT_AGENT_CONFIG]["alias"]
    if "region" not in st.session_state:
        st.session_state.region = AGENT_CONFIGS[DEFAULT_AGENT_CONFIG]["region"]
    if "custom_agent_id" not in st.session_state:
        st.session_state.custom_agent_id = ""
    if "agent_status" not in st.session_state:
        st.session_state.agent_status = "🔄 Checking..."
    if "last_agent_check" not in st.session_state:
        st.session_state.last_agent_check = None
    if "auto_check_enabled" not in st.session_state:
        st.session_state.auto_check_enabled = True  # 默认启用自动检查
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
    """Automatically check agent status if enabled and needed."""
    if (st.session_state.auto_check_enabled and 
        st.session_state.agent_id and 
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
        st.session_state.status_checking = False
        return True
    return False

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
    st.session_state.agent_status = "🔄 Checking..." if st.session_state.auto_check_enabled else "Unknown"
    st.session_state.last_agent_check = None
    st.session_state.status_checking = False

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
            if st.session_state.auto_check_enabled:
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
                if st.session_state.auto_check_enabled:
                    st.rerun()
        
        with col2:
            st.write("**Current Config:**")
            st.code(f"ID: {st.session_state.agent_id or 'Not set'}")
            st.code(f"Region: {st.session_state.region}")

def render_sidebar():
    """Render the sidebar with session management."""
    with st.sidebar:
        st.header("💬 Session Management")
        
        # Auto-check toggle
        st.subheader("🔧 Auto-Check Settings")
        auto_check = st.checkbox(
            "🔄 Auto-check agent status",
            value=st.session_state.auto_check_enabled,
            key="auto_check_toggle",
            help="Automatically check agent status when switching or launching"
        )
        if auto_check != st.session_state.auto_check_enabled:
            st.session_state.auto_check_enabled = auto_check
            if auto_check and st.session_state.agent_status == "Unknown":
                st.session_state.agent_status = "🔄 Checking..."
                st.rerun()
        
        if st.session_state.auto_check_enabled:
            st.caption("✅ Status will be checked automatically")
        else:
            st.caption("⚠️ Manual status check required")
        
        st.divider()
        
        # Current configuration
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
        
        st.divider()
        
        # Session info
        st.subheader("🔧 Session Info")
        st.write(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
        st.write(f"**Messages:** {len(st.session_state.messages)}")
        
        # Session controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear", key="clear_chat", help="Clear all messages"):
                st.session_state.messages = []
                st.success("Chat cleared!")
                st.rerun()
        
        with col2:
            if st.button("🔄 New", key="new_session", help="Start new session"):
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.messages = []
                st.success("New session!")
                st.rerun()

def main():
    """Main function to run the Streamlit app."""
    initialize_session_state()

    st.title("🤖 Bedrock Agent Chat Interface")
    st.markdown("*Select an agent and start chatting - status checked automatically*")
    
    # Auto-check on first launch
    if not st.session_state.app_initialized:
        st.session_state.app_initialized = True
        if st.session_state.auto_check_enabled:
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
    st.markdown(
        "💡 **Tips:** "
        "Agent status is checked automatically • "
        "Use dropdown to switch agents instantly • "
        "Toggle auto-check in sidebar if needed"
    )

if __name__ == "__main__":
    main()
