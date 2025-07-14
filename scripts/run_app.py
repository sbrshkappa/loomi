#!/usr/bin/env python3
"""
Script to run the AI Storyteller application.
This script provides a convenient way to start either the chat interface or API server.
"""

import argparse
import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))

def run_chat_interface():
    """Run the Chainlit chat interface."""
    try:
        import chainlit as cl
        from main import app
        cl.run(app)
    except ImportError as e:
        print(f"Error: {e}")
        print("Make sure chainlit is installed: pip install chainlit")
        sys.exit(1)

def run_api_server(host="0.0.0.0", port=8000, reload=False):
    """Run the FastAPI server."""
    try:
        from api.app import app
        uvicorn.run(
            "api.app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except ImportError as e:
        print(f"Error: {e}")
        print("Make sure fastapi and uvicorn are installed: pip install fastapi uvicorn")
        sys.exit(1)

def check_environment():
    """Check if required environment variables are set."""
    required_vars = [
        "OPENAI_API_KEY",
        "OPENAI_ENDPOINT"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Warning: The following environment variables are not set:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        print("You can copy env.example to .env and configure it.")
        return False
    
    return True

def main():
    """Main function to parse arguments and run the application."""
    parser = argparse.ArgumentParser(
        description="AI Storyteller Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_app.py chat          # Run chat interface
  python scripts/run_app.py api           # Run API server
  python scripts/run_app.py api --port 8080  # Run API on port 8080
  python scripts/run_app.py api --reload  # Run API with auto-reload
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Chat interface command
    chat_parser = subparsers.add_parser("chat", help="Run the chat interface")
    
    # API server command
    api_parser = subparsers.add_parser("api", help="Run the API server")
    api_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    api_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    api_parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Check environment variables
    if not check_environment():
        response = input("\nDo you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Run the appropriate command
    if args.command == "chat":
        print("Starting AI Storyteller Chat Interface...")
        run_chat_interface()
    elif args.command == "api":
        print(f"Starting AI Storyteller API Server on {args.host}:{args.port}...")
        run_api_server(args.host, args.port, args.reload)

if __name__ == "__main__":
    main() 