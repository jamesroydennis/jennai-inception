# C:\Users\jarde\Projects\JennAI\main.py

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
from core.dependency_container import DependencyContainer # The container itself is still needed here
from core.bootstrap import (
    configure_project_business_dependencies,
    configure_project_data_dependencies,
    configure_project_presentation_dependencies
)

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
    global_container = DependencyContainer() 

    logger.info("INFO - JennAI Starting...")

    flask_app_instance = None # Initialize to None

    # Call all configuration functions
    configure_project_business_dependencies(global_container)
    configure_project_data_dependencies(global_container)
    flask_app_instance = configure_project_presentation_dependencies(global_container)

    logger.success("SUCCESS - JennAI STARTUP COMPLETE.")
