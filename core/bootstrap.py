# File: core/bootstrap.py

from core.dependency_container import DependencyContainer
from loguru import logger # Assuming loguru is configured by main.py already

def get_configured_container() -> DependencyContainer:
    """
    Initializes and configures the global DependencyContainer.
    All application dependencies are wired here.
    """
    logger.info("INFO - Bootstrapping: Initializing and configuring DependencyContainer.")
    # The DependencyContainer's __init__ will automatically call configure_application_dependencies()
    container = DependencyContainer()
    logger.success("SUCCESS - DependencyContainer fully configured.")
    return container

# You can remove the old configure_project_..._dependencies functions if they existed here
# For example:
# def configure_project_business_dependencies(container: DependencyContainer):
#     pass # This logic is now inside DependencyContainer.configure_application_dependencies
# ... and so on for data and presentation