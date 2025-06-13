#!/bin/bash


init()  {
#Bedrock Agent Chat Application Launcher
echo "🤖 Starting Bedrock Agent Chat Interface..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if aws sts get-caller-identity >/dev/null 2>&1; then
    echo "✅ AWS credentials are configured"
else
    echo "⚠️  AWS credentials not found. Please configure using one of:"
    echo "   • aws configure"
    echo "   • export AWS_ACCESS_KEY_ID=your_key"
    echo "   • export AWS_SECRET_ACCESS_KEY=your_secret"
    echo "   • Use IAM roles (if running on EC2)"
fi

# Start the Streamlit app
echo "🚀 Starting Streamlit application..."
echo "📱 The app will open in your browser automatically."
echo "🔗 If it doesn't open, go to: http://localhost:8501"
echo ""
echo "✨ New Features:"
echo "   • 🔄 Auto-check agent status on launch"
echo "   • 🔄 Auto-check when switching agents"
echo "   • 🔄 Auto-check for custom agent IDs"
echo "   • 🎛️ Toggle auto-check in sidebar"
echo "   • 📊 Real-time status indicators"
echo "   • 🚫 No .env file needed - uses AWS default credentials"
echo ""
}
#

# Use the main app.py (now with auto-check functionality)
streamlit run app.py --server.port 8501 --server.address localhost
