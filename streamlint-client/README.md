# 🤖 Bedrock Agent Chat Interface

A Streamlit-based chat interface for interacting with Amazon Bedrock Agents with real-time agent switching capabilities.

## ✨ Features

### 🔄 Real-time Agent Switching
- Switch between different Bedrock agents without restarting the application
- Predefined agent configurations for easy selection
- Custom agent ID support for flexibility
- Automatic session management when switching agents

### 🎯 Agent Management
- **Predefined Agents**: Quick selection from configured agents
- **Custom Agents**: Enter your own agent ID for testing
- **Agent Status Check**: Verify agent availability before chatting
- **Dropdown Interface**: Clean, intuitive agent selection

### 💬 Enhanced Chat Experience
- Persistent chat history within sessions
- Session management with clear/new session options
- Real-time status indicators
- Responsive UI with detailed configuration display

### 🔧 Simple Configuration
- No .env files needed - uses AWS default credentials
- JSON-based agent configuration for easy maintenance
- Flexible region and alias configuration

## 🚀 Quick Start

### Option 1: Using the Launch Script (Recommended)
```bash
cd streamlint-client
./run_app.sh
```

### Option 2: Manual Setup
```bash
cd streamlint-client

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (if not already done)
aws configure

# Run the application
streamlit run app.py
```

## 📋 Configuration

### Agent Configuration
Edit `agent_config.json` to add or modify agent configurations:

```json
{
  "agents": {
    "Your Agent Name": {
      "id": "YOUR_AGENT_ID",
      "alias": "AGENT_ALIAS",
      "description": "Description of your agent",
      "region": "us-west-2",
      "capabilities": ["Feature1", "Feature2"]
    }
  },
  "default_agent": "Your Agent Name",
  "default_region": "us-west-2"
}
```

### AWS Credentials
Configure your AWS credentials using one of these methods:

1. **AWS CLI** (Recommended):
   ```bash
   aws configure
   ```

2. **Environment Variables**:
   ```bash
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   export AWS_DEFAULT_REGION=us-west-2
   ```

3. **IAM Roles** (if running on EC2)

## 🎮 Usage

### Switching Agents
1. **Select from Dropdown**: Use the dropdown menu at the top of the page
2. **Custom Agent**: Select "Custom Agent" and enter your agent ID
3. **Real-time Effect**: Changes take effect immediately without restart

### Agent Status
- **Manual Check**: Click "🔄" button to verify agent availability
- **Status Indicators**:
  - ✅ Available: Agent is ready to use
  - ❌ Agent Not Found: Invalid agent ID
  - 🔒 Access Denied: Permission issues
  - ❌ Invalid Configuration: Configuration errors

### Session Management
- **Clear Chat**: Remove all messages but keep the session
- **New Session**: Start a fresh session with new session ID
- **Auto Session Reset**: New session created when switching agents

## 📁 File Structure

```
streamlint-client/
├── app.py                 # Main application (dropdown interface)
├── app_enhanced.py        # Enhanced version (sidebar interface)
├── app_dropdown.py        # Full-featured dropdown version
├── app_simple.py          # Minimal version
├── agent_config.json      # Agent configuration file
├── requirements.txt       # Python dependencies (no dotenv needed)
├── run_app.sh            # Launch script
├── test_config.py        # Configuration test script
└── README.md             # This file
```

## 🔧 Advanced Features

### Custom Agent Configuration
You can add new agents to `agent_config.json`:

```json
{
  "agents": {
    "My Custom Agent": {
      "id": "ABCDEF1234",
      "alias": "PROD",
      "description": "Production agent for customer service",
      "region": "us-east-1",
      "capabilities": ["Customer Service", "FAQ", "Support"]
    }
  }
}
```

### Multiple AWS Profiles
If you have multiple AWS profiles:

```bash
# Set the profile before running
export AWS_PROFILE=bedrock-dev
streamlit run app.py

# Or use aws configure with profile
aws configure --profile bedrock-dev
export AWS_PROFILE=bedrock-dev
```

## 🐛 Troubleshooting

### Common Issues

1. **Agent Not Found**
   - Verify the agent ID is correct
   - Check if the agent exists in your AWS account
   - Ensure you're using the correct region

2. **Access Denied**
   - Check AWS credentials: `aws sts get-caller-identity`
   - Verify IAM permissions for Bedrock
   - Ensure the agent alias is correct

3. **Connection Issues**
   - Verify internet connectivity
   - Check AWS service status
   - Confirm region availability

### Debug Steps
1. Run the configuration test:
   ```bash
   python test_config.py
   ```

2. Check AWS credentials:
   ```bash
   aws sts get-caller-identity
   ```

3. Verify Bedrock permissions:
   ```bash
   aws bedrock list-foundation-models --region us-west-2
   ```

## 📝 Requirements

- Python 3.8+
- AWS Account with Bedrock access
- Valid Bedrock Agent IDs
- Appropriate IAM permissions

## 🎯 Key Improvements

### No More .env Files!
- Uses AWS default credential chain
- Supports AWS CLI, environment variables, IAM roles
- Simpler setup and deployment
- Better security practices

### Cleaner Dependencies
- Removed `python-dotenv` dependency
- Only requires `streamlit` and `boto3`
- Faster installation and startup

### Better Error Handling
- Clear credential configuration guidance
- Helpful error messages
- Step-by-step troubleshooting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Run `python test_config.py` for diagnostics
3. Review AWS Bedrock documentation
4. Check AWS service status
