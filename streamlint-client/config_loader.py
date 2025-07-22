#!/usr/bin/env python3
"""
Configuration Loader for Bedrock Agent Chat Interface
Handles loading and validation of agent configurations from JSON files.
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigLoader:
    """Handles loading and validation of agent configurations."""
    
    def __init__(self, config_file: str = "agent_config.json"):
        """
        Initialize the configuration loader.
        
        Args:
            config_file: Path to the agent configuration JSON file
        """
        self.config_file = config_file
        self.config_path = Path(config_file)
        self.logger = logging.getLogger(__name__)
        self._config_cache = None
        self._last_modified = None
        
    def load_config(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        Load agent configuration from JSON file with caching.
        
        Args:
            force_reload: Force reload even if cached version exists
            
        Returns:
            Dictionary containing agent configurations
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
            ValueError: If config structure is invalid
        """
        try:
            # Check if file exists
            if not self.config_path.exists():
                self.logger.error(f"Configuration file not found: {self.config_file}")
                return self._get_default_config()
            
            # Get file modification time
            current_modified = self.config_path.stat().st_mtime
            
            # Return cached config if available and file hasn't changed
            if (not force_reload and 
                self._config_cache is not None and 
                self._last_modified == current_modified):
                return self._config_cache
            
            # Load configuration from file
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate configuration structure
            validated_config = self._validate_config(config)
            
            # Cache the configuration
            self._config_cache = validated_config
            self._last_modified = current_modified
            
            self.logger.info(f"Successfully loaded configuration from {self.config_file}")
            return validated_config
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return self._get_default_config()
    
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the configuration structure and add defaults.
        
        Args:
            config: Raw configuration dictionary
            
        Returns:
            Validated and normalized configuration
            
        Raises:
            ValueError: If configuration structure is invalid
        """
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        # Ensure required top-level keys exist
        if "agents" not in config:
            raise ValueError("Configuration must contain 'agents' key")
        
        if not isinstance(config["agents"], dict):
            raise ValueError("'agents' must be a dictionary")
        
        # Add default values if missing
        config.setdefault("default_agent", list(config["agents"].keys())[0] if config["agents"] else "")
        config.setdefault("default_region", "us-west-2")
        
        # Validate each agent configuration
        for agent_name, agent_config in config["agents"].items():
            if not isinstance(agent_config, dict):
                raise ValueError(f"Agent '{agent_name}' configuration must be a dictionary")
            
            # Ensure required fields exist
            agent_config.setdefault("id", "")
            agent_config.setdefault("alias", "TSTALIASID")
            agent_config.setdefault("description", f"Agent: {agent_name}")
            agent_config.setdefault("region", config["default_region"])
            agent_config.setdefault("capabilities", [])
            
            # Validate field types
            if not isinstance(agent_config["capabilities"], list):
                agent_config["capabilities"] = []
        
        return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration when file loading fails.
        
        Returns:
            Default agent configuration
        """
        return {
            "agents": {
                "GraphRAG+Neptune": {
                    "id": "WN79XAAFL6",
                    "alias": "TSTALIASID",
                    "description": "GraphRAG with Neptune - Advanced knowledge graph analysis and document processing",
                    "region": "us-west-2",
                    "capabilities": ["Knowledge Graph", "Graph Analysis", "Document Processing", "Neptune DB"]
                },
                "Normal RAG+OpenSearch": {
                    "id": "ZUJPK3HE6I",
                    "alias": "TSTALIASID", 
                    "description": "Traditional RAG with OpenSearch - Standard document retrieval and Q&A",
                    "region": "us-west-2",
                    "capabilities": ["Document Retrieval", "Vector Search", "Q&A", "OpenSearch"]
                },
                "Custom Agent": {
                    "id": "",
                    "alias": "TSTALIASID",
                    "description": "Custom agent configuration - Enter your own Agent ID",
                    "region": "us-west-2",
                    "capabilities": ["Custom"]
                }
            },
            "default_agent": "Normal RAG+OpenSearch",
            "default_region": "us-west-2"
        }
    
    def get_agent_config(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Agent configuration dictionary or None if not found
        """
        config = self.load_config()
        return config["agents"].get(agent_name)
    
    def get_agent_names(self) -> list:
        """
        Get list of available agent names.
        
        Returns:
            List of agent names
        """
        config = self.load_config()
        return list(config["agents"].keys())
    
    def get_default_agent(self) -> str:
        """
        Get the default agent name.
        
        Returns:
            Default agent name
        """
        config = self.load_config()
        return config.get("default_agent", "")
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate before saving
            validated_config = self._validate_config(config)
            
            # Write to file with pretty formatting
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(validated_config, f, indent=2, ensure_ascii=False)
            
            # Clear cache to force reload
            self._config_cache = None
            self._last_modified = None
            
            self.logger.info(f"Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False
    
    def add_agent(self, name: str, agent_config: Dict[str, Any]) -> bool:
        """
        Add a new agent to the configuration.
        
        Args:
            name: Agent name
            agent_config: Agent configuration dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            config = self.load_config()
            config["agents"][name] = agent_config
            return self.save_config(config)
        except Exception as e:
            self.logger.error(f"Error adding agent '{name}': {e}")
            return False
    
    def remove_agent(self, name: str) -> bool:
        """
        Remove an agent from the configuration.
        
        Args:
            name: Agent name to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            config = self.load_config()
            if name in config["agents"]:
                del config["agents"][name]
                
                # Update default agent if it was removed
                if config.get("default_agent") == name:
                    remaining_agents = list(config["agents"].keys())
                    config["default_agent"] = remaining_agents[0] if remaining_agents else ""
                
                return self.save_config(config)
            return True
        except Exception as e:
            self.logger.error(f"Error removing agent '{name}': {e}")
            return False


# Global instance for easy access
config_loader = ConfigLoader()

if __name__ == "__main__":
    # Test the configuration loader
    loader = ConfigLoader()
    config = loader.load_config()
    print("Loaded configuration:")
    print(json.dumps(config, indent=2))
    
    print("\nAvailable agents:")
    for name in loader.get_agent_names():
        print(f"  - {name}")
    
    print(f"\nDefault agent: {loader.get_default_agent()}")
