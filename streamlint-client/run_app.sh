#!/bin/bash

# Secure Bedrock Agent Chat Interface Launch Script
echo "🔐 Starting Secure Bedrock Agent Chat Interface..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check AWS credentials
echo "🔍 Checking AWS credentials..."
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "⚠️  AWS credentials not configured!"
    echo "Please run: aws configure"
    echo "Or set environment variables:"
    echo "  export AWS_ACCESS_KEY_ID=your_key"
    echo "  export AWS_SECRET_ACCESS_KEY=your_secret"
    echo "  export AWS_DEFAULT_REGION=us-west-2"
    exit 1
fi

echo "✅ AWS credentials configured"

# Create auth config if it doesn't exist
if [ ! -f "auth_config.json" ]; then
    echo "🔐 Creating default authentication configuration..."
    echo "Default users will be created:"
    echo "  - admin / bedrock2024 (Admin)"
    echo "  - user1 / demo123 (User)"
fi

# Launch the secure application
echo "🚀 Launching Secure Bedrock Agent Chat Interface..."
echo "📱 The app will open in your browser automatically"
echo "🔐 Login required - see terminal for default credentials"
echo ""
echo "Default Login Credentials:"
echo "  Username: admin    | Password: bedrock2024 (Admin)"
echo "  Username: user1    | Password: demo123     (User)"
echo ""
echo "Press Ctrl+C to stop the application"
echo "----------------------------------------"

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
