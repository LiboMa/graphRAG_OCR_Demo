#!/usr/bin/env python3
"""
Management CLI for Bedrock Agent Chat Interface
Provides command-line interface for managing the application and configurations.
"""

import argparse
import json
import sys
from pathlib import Path
from config_loader import ConfigLoader
from process_manager import ProcessManager

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Bedrock Agent Chat Interface Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s app start --port 8502
  %(prog)s app stop
  %(prog)s app status
  %(prog)s config list
  %(prog)s config add "My Agent" --id AGENT123 --region us-east-1
  %(prog)s config remove "My Agent"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # App management commands
    app_parser = subparsers.add_parser('app', help='Application management')
    app_subparsers = app_parser.add_subparsers(dest='app_action', help='App actions')
    
    # App start
    start_parser = app_subparsers.add_parser('start', help='Start the application')
    start_parser.add_argument('--port', type=int, default=8501, help='Port number')
    start_parser.add_argument('--host', default='0.0.0.0', help='Host address')
    start_parser.add_argument('--app', default='app.py', help='App file')
    start_parser.add_argument('--foreground', action='store_true', help='Run in foreground')
    
    # App stop
    app_subparsers.add_parser('stop', help='Stop the application')
    
    # App restart
    restart_parser = app_subparsers.add_parser('restart', help='Restart the application')
    restart_parser.add_argument('--port', type=int, default=8501, help='Port number')
    restart_parser.add_argument('--host', default='0.0.0.0', help='Host address')
    restart_parser.add_argument('--app', default='app.py', help='App file')
    restart_parser.add_argument('--foreground', action='store_true', help='Run in foreground')
    
    # App status
    app_subparsers.add_parser('status', help='Show application status')
    
    # App logs
    logs_parser = app_subparsers.add_parser('logs', help='Show application logs')
    logs_parser.add_argument('--type', choices=['stdout', 'stderr'], default='stdout',
                           help='Log type')
    logs_parser.add_argument('--lines', type=int, default=50, help='Number of lines')
    
    # Config management commands
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_subparsers = config_parser.add_subparsers(dest='config_action', help='Config actions')
    
    # Config list
    config_subparsers.add_parser('list', help='List agent configurations')
    
    # Config show
    show_parser = config_subparsers.add_parser('show', help='Show specific agent config')
    show_parser.add_argument('name', help='Agent name')
    
    # Config add
    add_parser = config_subparsers.add_parser('add', help='Add agent configuration')
    add_parser.add_argument('name', help='Agent name')
    add_parser.add_argument('--id', required=True, help='Agent ID')
    add_parser.add_argument('--alias', default='TSTALIASID', help='Agent alias')
    add_parser.add_argument('--description', help='Agent description')
    add_parser.add_argument('--region', default='us-west-2', help='AWS region')
    add_parser.add_argument('--capabilities', nargs='*', default=[], help='Agent capabilities')
    
    # Config remove
    remove_parser = config_subparsers.add_parser('remove', help='Remove agent configuration')
    remove_parser.add_argument('name', help='Agent name')
    
    # Config set-default
    default_parser = config_subparsers.add_parser('set-default', help='Set default agent')
    default_parser.add_argument('name', help='Agent name')
    
    # Config validate
    config_subparsers.add_parser('validate', help='Validate configuration file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Handle app commands
    if args.command == 'app':
        return handle_app_commands(args)
    
    # Handle config commands
    elif args.command == 'config':
        return handle_config_commands(args)
    
    else:
        parser.print_help()
        return 1

def handle_app_commands(args):
    """Handle application management commands."""
    manager = ProcessManager()
    
    if args.app_action == 'start':
        success, message = manager.start_streamlit(
            app_file=args.app,
            port=args.port,
            host=args.host,
            background=not args.foreground
        )
        print(message)
        if success and not args.foreground:
            print(f"Access the application at: http://{args.host}:{args.port}")
        return 0 if success else 1
    
    elif args.app_action == 'stop':
        success, message = manager.stop_streamlit()
        print(message)
        return 0 if success else 1
    
    elif args.app_action == 'restart':
        success, message = manager.restart_streamlit(
            app_file=args.app,
            port=args.port,
            host=args.host,
            background=not args.foreground
        )
        print(message)
        if success and not args.foreground:
            print(f"Access the application at: http://{args.host}:{args.port}")
        return 0 if success else 1
    
    elif args.app_action == 'status':
        status = manager.get_status()
        print(json.dumps(status, indent=2))
        return 0
    
    elif args.app_action == 'logs':
        logs = manager.get_logs(log_type=args.type, lines=args.lines)
        for line in logs:
            print(line)
        return 0
    
    else:
        print("Unknown app action")
        return 1

def handle_config_commands(args):
    """Handle configuration management commands."""
    config_loader = ConfigLoader()
    
    if args.config_action == 'list':
        config = config_loader.load_config()
        agents = config.get('agents', {})
        default_agent = config.get('default_agent', '')
        
        print("Available Agents:")
        print("================")
        for name, agent_config in agents.items():
            marker = " (default)" if name == default_agent else ""
            print(f"• {name}{marker}")
            print(f"  ID: {agent_config.get('id', 'N/A')}")
            print(f"  Region: {agent_config.get('region', 'N/A')}")
            print(f"  Description: {agent_config.get('description', 'N/A')}")
            if agent_config.get('capabilities'):
                print(f"  Capabilities: {', '.join(agent_config['capabilities'])}")
            print()
        
        return 0
    
    elif args.config_action == 'show':
        agent_config = config_loader.get_agent_config(args.name)
        if agent_config:
            print(f"Agent Configuration: {args.name}")
            print("=" * (len(args.name) + 21))
            print(json.dumps(agent_config, indent=2))
        else:
            print(f"Agent '{args.name}' not found")
            return 1
        return 0
    
    elif args.config_action == 'add':
        agent_config = {
            'id': args.id,
            'alias': args.alias,
            'description': args.description or f"Agent: {args.name}",
            'region': args.region,
            'capabilities': args.capabilities
        }
        
        success = config_loader.add_agent(args.name, agent_config)
        if success:
            print(f"Agent '{args.name}' added successfully")
        else:
            print(f"Failed to add agent '{args.name}'")
            return 1
        return 0
    
    elif args.config_action == 'remove':
        success = config_loader.remove_agent(args.name)
        if success:
            print(f"Agent '{args.name}' removed successfully")
        else:
            print(f"Failed to remove agent '{args.name}'")
            return 1
        return 0
    
    elif args.config_action == 'set-default':
        config = config_loader.load_config()
        if args.name in config.get('agents', {}):
            config['default_agent'] = args.name
            success = config_loader.save_config(config)
            if success:
                print(f"Default agent set to '{args.name}'")
            else:
                print("Failed to update default agent")
                return 1
        else:
            print(f"Agent '{args.name}' not found")
            return 1
        return 0
    
    elif args.config_action == 'validate':
        try:
            config = config_loader.load_config(force_reload=True)
            print("✅ Configuration is valid")
            print(f"Found {len(config.get('agents', {}))} agents")
            print(f"Default agent: {config.get('default_agent', 'None')}")
        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            return 1
        return 0
    
    else:
        print("Unknown config action")
        return 1

if __name__ == "__main__":
    sys.exit(main())
