import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import streamlit as st

class AuthManager:
    """Simple authentication manager for Streamlit app."""
    
    def __init__(self, config_file: str = "auth_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.failed_attempts = {}  # Track failed login attempts
    
    def _load_config(self) -> Dict:
        """Load authentication configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config if file doesn't exist
            default_config = {
                "users": {
                    "admin": {
                        "password": "bedrock2024",
                        "role": "admin",
                        "name": "Administrator"
                    }
                },
                "session_timeout_minutes": 60,
                "max_login_attempts": 3,
                "lockout_duration_minutes": 15
            }
            self._save_config(default_config)
            return default_config
        except json.JSONDecodeError:
            st.error("❌ Invalid authentication configuration file")
            return {"users": {}}
    
    def _save_config(self, config: Dict):
        """Save configuration to JSON file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            st.error(f"❌ Failed to save auth config: {str(e)}")
    
    def _hash_password(self, password: str) -> str:
        """Simple password hashing (for demo purposes)."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _is_locked_out(self, username: str) -> bool:
        """Check if user is locked out due to failed attempts."""
        if username not in self.failed_attempts:
            return False
        
        attempts_data = self.failed_attempts[username]
        if attempts_data["count"] >= self.config.get("max_login_attempts", 3):
            lockout_duration = self.config.get("lockout_duration_minutes", 15)
            lockout_end = attempts_data["last_attempt"] + timedelta(minutes=lockout_duration)
            if datetime.now() < lockout_end:
                return True
            else:
                # Reset attempts after lockout period
                del self.failed_attempts[username]
        
        return False
    
    def _record_failed_attempt(self, username: str):
        """Record a failed login attempt."""
        if username not in self.failed_attempts:
            self.failed_attempts[username] = {"count": 0, "last_attempt": datetime.now()}
        
        self.failed_attempts[username]["count"] += 1
        self.failed_attempts[username]["last_attempt"] = datetime.now()
    
    def _clear_failed_attempts(self, username: str):
        """Clear failed attempts for successful login."""
        if username in self.failed_attempts:
            del self.failed_attempts[username]
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user credentials.
        Returns: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Please enter both username and password"
        
        # Check if user is locked out
        if self._is_locked_out(username):
            lockout_duration = self.config.get("lockout_duration_minutes", 15)
            return False, f"Account locked due to too many failed attempts. Try again in {lockout_duration} minutes."
        
        # Check if user exists
        if username not in self.config["users"]:
            self._record_failed_attempt(username)
            return False, "Invalid username or password"
        
        user_data = self.config["users"][username]
        
        # For demo purposes, we're storing plain text passwords
        # In production, you should hash passwords
        if password == user_data["password"]:
            self._clear_failed_attempts(username)
            return True, f"Welcome, {user_data.get('name', username)}!"
        else:
            self._record_failed_attempt(username)
            remaining_attempts = self.config.get("max_login_attempts", 3) - self.failed_attempts[username]["count"]
            if remaining_attempts > 0:
                return False, f"Invalid username or password. {remaining_attempts} attempts remaining."
            else:
                return False, "Account locked due to too many failed attempts."
    
    def is_session_valid(self) -> bool:
        """Check if current session is valid."""
        if "authenticated" not in st.session_state:
            return False
        
        if not st.session_state.authenticated:
            return False
        
        # Check session timeout
        if "login_time" in st.session_state:
            timeout_minutes = self.config.get("session_timeout_minutes", 60)
            login_time = st.session_state.login_time
            if datetime.now() - login_time > timedelta(minutes=timeout_minutes):
                self.logout()
                return False
        
        return True
    
    def login(self, username: str) -> bool:
        """Set session as authenticated."""
        if username in self.config["users"]:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_role = self.config["users"][username].get("role", "user")
            st.session_state.user_name = self.config["users"][username].get("name", username)
            st.session_state.login_time = datetime.now()
            return True
        return False
    
    def logout(self):
        """Clear authentication session."""
        for key in ["authenticated", "username", "user_role", "user_name", "login_time"]:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user info."""
        if self.is_session_valid():
            return {
                "username": st.session_state.username,
                "role": st.session_state.user_role,
                "name": st.session_state.user_name,
                "login_time": st.session_state.login_time
            }
        return None
    
    def add_user(self, username: str, password: str, role: str = "user", name: str = None) -> bool:
        """Add a new user (admin only)."""
        if username in self.config["users"]:
            return False
        
        self.config["users"][username] = {
            "password": password,  # In production, hash this
            "role": role,
            "name": name or username
        }
        
        self._save_config(self.config)
        return True
    
    def remove_user(self, username: str) -> bool:
        """Remove a user (admin only)."""
        if username in self.config["users"]:
            del self.config["users"][username]
            self._save_config(self.config)
            return True
        return False
    
    def get_all_users(self) -> Dict:
        """Get all users (admin only)."""
        return self.config["users"]
    
    def render_login_form(self):
        """Render the login form."""
        st.markdown("""
        <div style="max-width: 400px; margin: 0 auto; padding: 2rem; 
                    border: 1px solid #ddd; border-radius: 10px; 
                    background-color: #f9f9f9;">
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔐 Login Required")
        st.markdown("Please authenticate to access the Bedrock Agent Chat Interface")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if login_button:
                success, message = self.authenticate(username, password)
                if success:
                    self.login(username)
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Show demo credentials
        with st.expander("🔍 Demo Credentials"):
            st.markdown("""
            **Default Users:**
            - **Username:** `admin` | **Password:** `bedrock2024` (Admin)
            - **Username:** `user1` | **Password:** `demo123` (User)
            
            **Features:**
            - Session timeout: 60 minutes
            - Max login attempts: 3
            - Lockout duration: 15 minutes
            """)
    
    def render_user_info(self):
        """Render current user information in sidebar."""
        user = self.get_current_user()
        if user:
            st.sidebar.markdown("### 👤 User Session")
            st.sidebar.write(f"**Name:** {user['name']}")
            st.sidebar.write(f"**Username:** {user['username']}")
            st.sidebar.write(f"**Role:** {user['role'].title()}")
            
            # Session info
            login_duration = datetime.now() - user['login_time']
            hours, remainder = divmod(int(login_duration.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            st.sidebar.write(f"**Session:** {hours:02d}:{minutes:02d}")
            
            # Logout button
            if st.sidebar.button("🚪 Logout", use_container_width=True):
                self.logout()
                st.rerun()
            
            st.sidebar.divider()
    
    def render_admin_panel(self):
        """Render admin panel for user management."""
        user = self.get_current_user()
        if not user or user["role"] != "admin":
            return
        
        with st.sidebar.expander("⚙️ Admin Panel"):
            st.markdown("**User Management**")
            
            # Add user form
            with st.form("add_user_form"):
                st.markdown("**Add New User:**")
                new_username = st.text_input("Username", key="new_username")
                new_password = st.text_input("Password", type="password", key="new_password")
                new_role = st.selectbox("Role", ["user", "admin"], key="new_role")
                new_name = st.text_input("Display Name", key="new_name")
                
                if st.form_submit_button("➕ Add User"):
                    if new_username and new_password:
                        if self.add_user(new_username, new_password, new_role, new_name):
                            st.success(f"User '{new_username}' added successfully!")
                            st.rerun()
                        else:
                            st.error("User already exists!")
                    else:
                        st.error("Username and password are required!")
            
            # List users
            st.markdown("**Current Users:**")
            users = self.get_all_users()
            for username, user_data in users.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{username}** ({user_data.get('role', 'user')})")
                with col2:
                    if username != st.session_state.username:  # Can't delete self
                        if st.button("🗑️", key=f"delete_{username}", help=f"Delete {username}"):
                            if self.remove_user(username):
                                st.success(f"User '{username}' deleted!")
                                st.rerun()
