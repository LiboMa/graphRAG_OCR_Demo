#!/usr/bin/env python3
"""
Process Manager for Bedrock Agent Chat Interface
Handles background process management for Streamlit applications.
"""

import os
import sys
import signal
import subprocess
import psutil
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class ProcessManager:
    """Manages background Streamlit processes."""
    
    def __init__(self, pid_file: str = "streamlit.pid", log_dir: str = "logs"):
        """
        Initialize the process manager.
        
        Args:
            pid_file: Path to store process ID file
            log_dir: Directory to store log files
        """
        self.pid_file = Path(pid_file)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # Create file handler
        log_file = self.log_dir / "process_manager.log"
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        if not logger.handlers:
            logger.addHandler(handler)
        
        return logger
    
    def start_streamlit(self, 
                       app_file: str = "app.py",
                       port: int = 8501,
                       host: str = "0.0.0.0",
                       background: bool = True,
                       additional_args: List[str] = None) -> Tuple[bool, str]:
        """
        Start Streamlit application.
        
        Args:
            app_file: Path to the Streamlit app file
            port: Port to run the application on
            host: Host address to bind to
            background: Whether to run in background
            additional_args: Additional command line arguments
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Check if already running
            if self.is_running():
                return False, "Streamlit is already running"
            
            # Prepare command
            cmd = [
                sys.executable, "-m", "streamlit", "run", app_file,
                "--server.port", str(port),
                "--server.address", host,
                "--server.headless", "true"
            ]
            
            if additional_args:
                cmd.extend(additional_args)
            
            # Setup log files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stdout_log = self.log_dir / f"streamlit_stdout_{timestamp}.log"
            stderr_log = self.log_dir / f"streamlit_stderr_{timestamp}.log"
            
            # Start process
            if background:
                with open(stdout_log, 'w') as stdout_f, open(stderr_log, 'w') as stderr_f:
                    process = subprocess.Popen(
                        cmd,
                        stdout=stdout_f,
                        stderr=stderr_f,
                        preexec_fn=os.setsid if os.name != 'nt' else None
                    )
                
                # Save PID
                self._save_pid(process.pid, {
                    'command': ' '.join(cmd),
                    'port': port,
                    'host': host,
                    'app_file': app_file,
                    'started_at': datetime.now().isoformat(),
                    'stdout_log': str(stdout_log),
                    'stderr_log': str(stderr_log)
                })
                
                # Wait a moment to check if process started successfully
                time.sleep(2)
                if process.poll() is None:
                    self.logger.info(f"Streamlit started successfully on {host}:{port} (PID: {process.pid})")
                    return True, f"Streamlit started successfully on {host}:{port} (PID: {process.pid})"
                else:
                    return False, "Streamlit failed to start - check logs"
            else:
                # Run in foreground
                process = subprocess.run(cmd)
                return True, "Streamlit finished"
                
        except Exception as e:
            self.logger.error(f"Error starting Streamlit: {e}")
            return False, f"Error starting Streamlit: {e}"
    
    def stop_streamlit(self) -> Tuple[bool, str]:
        """
        Stop the running Streamlit application.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            pid_info = self._load_pid()
            if not pid_info:
                return False, "No running Streamlit process found"
            
            pid = pid_info.get('pid')
            if not pid:
                return False, "Invalid PID information"
            
            # Check if process exists
            if not psutil.pid_exists(pid):
                self._cleanup_pid_file()
                return False, "Process no longer exists"
            
            # Get process
            process = psutil.Process(pid)
            
            # Terminate process gracefully
            if os.name != 'nt':
                # Unix-like systems
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            else:
                # Windows
                process.terminate()
            
            # Wait for process to terminate
            try:
                process.wait(timeout=10)
            except psutil.TimeoutExpired:
                # Force kill if it doesn't terminate gracefully
                if os.name != 'nt':
                    os.killpg(os.getpgid(pid), signal.SIGKILL)
                else:
                    process.kill()
                process.wait(timeout=5)
            
            self._cleanup_pid_file()
            self.logger.info(f"Streamlit process stopped (PID: {pid})")
            return True, f"Streamlit process stopped (PID: {pid})"
            
        except Exception as e:
            self.logger.error(f"Error stopping Streamlit: {e}")
            return False, f"Error stopping Streamlit: {e}"
    
    def restart_streamlit(self, **kwargs) -> Tuple[bool, str]:
        """
        Restart the Streamlit application.
        
        Args:
            **kwargs: Arguments to pass to start_streamlit
            
        Returns:
            Tuple of (success, message)
        """
        # Stop if running
        if self.is_running():
            success, message = self.stop_streamlit()
            if not success:
                return False, f"Failed to stop: {message}"
            
            # Wait a moment
            time.sleep(1)
        
        # Start again
        return self.start_streamlit(**kwargs)
    
    def is_running(self) -> bool:
        """
        Check if Streamlit is currently running.
        
        Returns:
            True if running, False otherwise
        """
        pid_info = self._load_pid()
        if not pid_info:
            return False
        
        pid = pid_info.get('pid')
        if not pid:
            return False
        
        try:
            # Check if process exists and is actually Streamlit
            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                cmdline = ' '.join(process.cmdline())
                if 'streamlit' in cmdline.lower():
                    return True
            
            # Clean up stale PID file
            self._cleanup_pid_file()
            return False
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            self._cleanup_pid_file()
            return False
    
    def get_status(self) -> Dict:
        """
        Get detailed status of the Streamlit process.
        
        Returns:
            Dictionary with status information
        """
        pid_info = self._load_pid()
        if not pid_info:
            return {'status': 'stopped', 'message': 'No process information found'}
        
        pid = pid_info.get('pid')
        if not pid:
            return {'status': 'error', 'message': 'Invalid PID information'}
        
        try:
            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                
                # Get process information
                info = {
                    'status': 'running',
                    'pid': pid,
                    'started_at': pid_info.get('started_at'),
                    'port': pid_info.get('port'),
                    'host': pid_info.get('host'),
                    'app_file': pid_info.get('app_file'),
                    'cpu_percent': process.cpu_percent(),
                    'memory_info': process.memory_info()._asdict(),
                    'create_time': datetime.fromtimestamp(process.create_time()).isoformat(),
                    'stdout_log': pid_info.get('stdout_log'),
                    'stderr_log': pid_info.get('stderr_log')
                }
                
                return info
            else:
                self._cleanup_pid_file()
                return {'status': 'stopped', 'message': 'Process no longer exists'}
                
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            self._cleanup_pid_file()
            return {'status': 'error', 'message': f'Error accessing process: {e}'}
    
    def get_logs(self, log_type: str = 'stdout', lines: int = 50) -> List[str]:
        """
        Get recent log lines.
        
        Args:
            log_type: Type of log ('stdout' or 'stderr')
            lines: Number of recent lines to return
            
        Returns:
            List of log lines
        """
        try:
            pid_info = self._load_pid()
            if not pid_info:
                return []
            
            log_file = pid_info.get(f'{log_type}_log')
            if not log_file or not Path(log_file).exists():
                return []
            
            with open(log_file, 'r') as f:
                all_lines = f.readlines()
                return [line.rstrip() for line in all_lines[-lines:]]
                
        except Exception as e:
            self.logger.error(f"Error reading logs: {e}")
            return []
    
    def _save_pid(self, pid: int, info: Dict):
        """Save PID and process information to file."""
        try:
            data = {'pid': pid, **info}
            with open(self.pid_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving PID file: {e}")
    
    def _load_pid(self) -> Optional[Dict]:
        """Load PID and process information from file."""
        try:
            if self.pid_file.exists():
                with open(self.pid_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading PID file: {e}")
        return None
    
    def _cleanup_pid_file(self):
        """Remove PID file."""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
        except Exception as e:
            self.logger.error(f"Error cleaning up PID file: {e}")


def main():
    """Command line interface for process management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Streamlit Process Manager")
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status', 'logs'],
                       help='Action to perform')
    parser.add_argument('--app', default='app.py', help='Streamlit app file')
    parser.add_argument('--port', type=int, default=8501, help='Port number')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--foreground', action='store_true', help='Run in foreground')
    parser.add_argument('--log-type', choices=['stdout', 'stderr'], default='stdout',
                       help='Log type to display')
    parser.add_argument('--lines', type=int, default=50, help='Number of log lines')
    
    args = parser.parse_args()
    
    manager = ProcessManager()
    
    if args.action == 'start':
        success, message = manager.start_streamlit(
            app_file=args.app,
            port=args.port,
            host=args.host,
            background=not args.foreground
        )
        print(message)
        sys.exit(0 if success else 1)
        
    elif args.action == 'stop':
        success, message = manager.stop_streamlit()
        print(message)
        sys.exit(0 if success else 1)
        
    elif args.action == 'restart':
        success, message = manager.restart_streamlit(
            app_file=args.app,
            port=args.port,
            host=args.host,
            background=not args.foreground
        )
        print(message)
        sys.exit(0 if success else 1)
        
    elif args.action == 'status':
        status = manager.get_status()
        print(json.dumps(status, indent=2))
        
    elif args.action == 'logs':
        logs = manager.get_logs(log_type=args.log_type, lines=args.lines)
        for line in logs:
            print(line)


if __name__ == "__main__":
    main()
