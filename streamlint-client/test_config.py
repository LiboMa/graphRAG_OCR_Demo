#!/usr/bin/env python3
"""
Configuration Test Script for Bedrock Agent Chat Interface
"""

import json
import os
import boto3

def load_agent_config():
    """Load and validate agent configuration."""
    try:
        config_path = os.path.join(os.path.dirname(__file__), "agent_config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("✅ Agent configuration loaded successfully")
        return config
    except FileNotFoundError:
        print("❌ agent_config.json not found")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in agent_config.json: {e}")
        return None

def test_aws_credentials():
    """Test AWS credentials configuration."""
    try:
        # Try to create a session using default credentials
        session = boto3.Session()
        
        # Test STS to verify credentials
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        
        print("✅ AWS credentials are valid")
        print(f"   Account: {identity.get('Account')}")
        print(f"   User/Role: {identity.get('Arn', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"❌ AWS credentials error: {e}")
        print("💡 Configure credentials using:")
        print("   • aws configure")
        print("   • export AWS_ACCESS_KEY_ID=your_key")
        print("   • export AWS_SECRET_ACCESS_KEY=your_secret")
        print("   • Use IAM roles (if running on EC2)")
        return False

def test_bedrock_access(config):
    """Test Bedrock service access."""
    if not config:
        return False
    
    try:
        # Test each configured agent
        for agent_name, agent_config in config["agents"].items():
            if agent_config["id"]:  # Skip empty IDs
                print(f"\n🧪 Testing agent: {agent_name}")
                print(f"   ID: {agent_config['id']}")
                print(f"   Alias: {agent_config['alias']}")
                print(f"   Region: {agent_config['region']}")
                
                try:
                    # Create client for agent's region
                    bedrock = boto3.client("bedrock-agent-runtime", region_name=agent_config["region"])
                    
                    # Try a simple test call
                    response = bedrock.invoke_agent(
                        agentId=agent_config["id"],
                        agentAliasId=agent_config["alias"],
                        inputText="Hello",
                        sessionId="test-session-123",
                        enableTrace=False
                    )
                    
                    print(f"   ✅ Agent {agent_name} is accessible")
                    
                except Exception as e:
                    error_msg = str(e)
                    if "ValidationException" in error_msg:
                        print(f"   ❌ Agent {agent_name}: Invalid configuration")
                    elif "AccessDeniedException" in error_msg:
                        print(f"   🔒 Agent {agent_name}: Access denied")
                    elif "ResourceNotFoundException" in error_msg:
                        print(f"   ❌ Agent {agent_name}: Not found")
                    else:
                        print(f"   ❌ Agent {agent_name}: {error_msg[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Bedrock access error: {e}")
        return False

def main():
    """Run all configuration tests."""
    print("🧪 Bedrock Agent Chat Interface - Configuration Test")
    print("=" * 60)
    
    # Test 1: Load configuration
    print("\n1. Testing configuration file...")
    config = load_agent_config()
    
    if config:
        print(f"   Found {len(config['agents'])} agent configurations")
        print(f"   Default agent: {config.get('default_agent', 'Not set')}")
        print(f"   Default region: {config.get('default_region', 'Not set')}")
    
    # Test 2: AWS credentials
    print("\n2. Testing AWS credentials...")
    aws_ok = test_aws_credentials()
    
    # Test 3: Bedrock access
    print("\n3. Testing Bedrock access...")
    if aws_ok and config:
        bedrock_ok = test_bedrock_access(config)
    else:
        print("❌ Skipping Bedrock test due to previous failures")
        bedrock_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print(f"   Configuration: {'✅ OK' if config else '❌ FAIL'}")
    print(f"   AWS Credentials: {'✅ OK' if aws_ok else '❌ FAIL'}")
    print(f"   Bedrock Access: {'✅ OK' if bedrock_ok else '❌ FAIL'}")
    
    if config and aws_ok and bedrock_ok:
        print("\n🎉 All tests passed! You're ready to use the chat interface.")
        print("   Run: ./run_app.sh or streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
        print("   1. Verify agent_config.json exists and is valid")
        print("   2. Check AWS credentials configuration")
        print("   3. Ensure you have Bedrock permissions")

if __name__ == "__main__":
    main()
