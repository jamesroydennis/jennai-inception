# File: C:\Users\jarde\Projects\JennAI\main.py

import sys
import os
from pathlib import Path
from dotenv import load_dotenv # Import load_dotenv

# --- Root Project Path Setup (CRITICAL for Monorepo Imports) ---
# This block ensures the main /JennAI project root is always on Python's sys.path.
# This allows all sub-projects (project/data, project/business, etc.)
# and centralized modules (config, core) to be imported using absolute paths.
jennai_root = Path(__file__).resolve().parent
if str(jennai_root) not in sys.path:
    sys.path.append(str(jennai_root))

# Load environment variables from .env file (if it exists)
load_dotenv(dotenv_path=jennai_root / ".env")

# --- Centralized Core Imports ---
# These modules are now directly discoverable from the JennAI root
from config.loguru_setup import setup_logging
from config.config import DEBUG_MODE
from core.bootstrap import get_configured_container # <-- Import the new simplified bootstrap function

# --- Global Setup (Orchestrated by main.py) ---
setup_logging(debug_mode=DEBUG_MODE) # Initialize Loguru for the entire monorepo
from loguru import logger # Import the configured logger instance

logger.info(f"INFO - JennAI Monorepo Main: Orchestration initialized.")
logger.info(f"INFO - Python interpreter: {sys.executable}")
logger.info(f"INFO - Current working directory: {os.getcwd()}")
logger.info(f"INFO - JennAI project root added to PATH: {jennai_root}")
logger.info(f"INFO - Running in DEBUG_MODE: {DEBUG_MODE}")

# --- Main Application Execution Block ---
if __name__ == '__main__':
    logger.info("INFO - JennAI Starting...")

    # Get the fully configured global container from bootstrap
    global_container = get_configured_container()

    flask_app_instance = None # Initialize to None

    # Resolve your main Flask app instance from the container
    try:
        # Example: if your Flask app is registered under a specific key or type
        # For instance, if you registered your Flask app instance in configure_application_dependencies
        # using register_instance(Flask, my_app_instance) or register_singleton(Flask, create_app_factory)
        # you would resolve it here.
        # Example assuming you registered it as "FlaskAppInstance" string key:
        # flask_app_instance = global_container.resolve("FlaskAppInstance")
        
        # For now, we just log a warning as we haven't concretely defined
        # how the Flask app itself is registered in the container yet.
        logger.warning("WARNING - Assuming Flask app instance will be resolved from the container later.")

    except Exception as e:
        logger.error(f"ERROR - Failed to resolve Flask app instance from container: {e}", exc_info=True)
        sys.exit(1) # Exit if core app cannot be initialized


    logger.info("INFO - JennAI STARTUP COMPLETE. Dependencies wired via IoC.")

    # You would typically run your Flask app here, e.g.:
    # if flask_app_instance:
    #    flask_app_instance.run(debug=DEBUG_MODE)
    # else:
    #    logger.warning("WARNING - Flask app instance not available to run.")
    