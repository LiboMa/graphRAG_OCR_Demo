# 🔐 Authentication Setup Guide

This guide explains how to use the secure version of the Bedrock Agent Chat Interface with user authentication.

## 🚀 Quick Start

### Launch the Secure App
```bash
./run_secure_app.sh
```

### Default Login Credentials
- **Admin User:**
  - Username: `admin`
  - Password: `bedrock2024`
  - Role: Administrator (can manage users)

- **Regular User:**
  - Username: `user1`
  - Password: `demo123`
  - Role: User (chat access only)

## 🛡️ Security Features

### Authentication
- **Login Required:** All users must authenticate before accessing the chat interface
- **Session Management:** Automatic session timeout after 60 minutes of inactivity
- **Failed Attempt Protection:** Account lockout after 3 failed login attempts (15-minute lockout)
- **Role-Based Access:** Different permissions for admin and regular users

### Session Security
- **Auto-Logout:** Sessions expire automatically for security
- **Session Tracking:** Monitor login time and session duration
- **Secure State Management:** User sessions are isolated and secure

## ⚙️ User Management (Admin Only)

### Adding New Users
1. Login as an admin user
2. Open the sidebar "Admin Panel"
3. Fill in the "Add New User" form:
   - Username (unique)
   - Password
   - Role (user/admin)
   - Display Name (optional)
4. Click "➕ Add User"

### Removing Users
1. In the Admin Panel, find the user in the "Current Users" list
2. Click the "🗑️" button next to their name
3. Confirm the deletion

### User Roles
- **Admin:** Can manage users, access all features
- **User:** Can only use the chat interface

## 📁 Configuration Files

### `auth_config.json`
Contains user credentials and security settings:
```json
{
  "users": {
    "username": {
      "password": "plaintext_password",
      "role": "admin|user",
      "name": "Display Name"
    }
  },
  "session_timeout_minutes": 60,
  "max_login_attempts": 3,
  "lockout_duration_minutes": 15
}
```

**Security Note:** In production, passwords should be hashed. This demo uses plain text for simplicity.

## 🔧 Customization

### Changing Default Settings
Edit `auth_config.json` to modify:
- Session timeout duration
- Maximum login attempts
- Lockout duration
- Default users

### Adding Your Own Users
You can manually edit `auth_config.json` or use the admin panel to add users.

## 🚨 Security Best Practices

### For Production Use
1. **Hash Passwords:** Implement proper password hashing
2. **HTTPS Only:** Use SSL/TLS encryption
3. **Strong Passwords:** Enforce password complexity requirements
4. **Regular Updates:** Keep dependencies updated
5. **Audit Logs:** Implement login/activity logging
6. **Environment Variables:** Store sensitive config in environment variables

### Current Security Level
This implementation provides **basic authentication** suitable for:
- Development environments
- Internal team access
- Demo purposes
- Small team deployments

**Not recommended for:**
- Public internet deployment
- Production systems with sensitive data
- High-security requirements

## 🐛 Troubleshooting

### Login Issues
1. **Invalid Credentials:** Check username/password spelling
2. **Account Locked:** Wait 15 minutes or contact admin
3. **Session Expired:** Login again (sessions timeout after 60 minutes)

### Admin Panel Not Visible
- Only admin users can see the admin panel
- Check your user role in the sidebar

### Configuration Issues
1. Check `auth_config.json` syntax (valid JSON)
2. Ensure file permissions allow read/write
3. Restart the application after config changes

## 📝 File Structure

```
streamlint-client/
├── app_authenticated.py    # Secure version of the app
├── auth_manager.py         # Authentication logic
├── auth_config.json        # User credentials & settings
├── run_secure_app.sh       # Launch script for secure app
├── AUTHENTICATION.md       # This guide
└── ... (other files)
```

## 🔄 Migration from Original App

The secure version maintains all original features:
- ✅ Real-time agent switching
- ✅ Chat history and session management
- ✅ Agent status checking
- ✅ State persistence
- ✅ All original functionality

**Plus new security features:**
- 🔐 User authentication
- 👤 User management
- 🛡️ Session security
- ⚙️ Admin controls

## 🆘 Support

For authentication-related issues:
1. Check this guide first
2. Verify `auth_config.json` is valid JSON
3. Try deleting `auth_config.json` to reset to defaults
4. Check file permissions
5. Restart the application

For general app issues, refer to the main README.md file.
