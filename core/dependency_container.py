# File: core/dependency_container.py (within your existing DependencyContainer class)

import inspect
from typing import Type, TypeVar, Dict, Callable, Any, Union, get_origin, get_args, Optional, List
from loguru import logger
import os

# --- New/Updated Imports needed for the configuration ---
from config.loguru_setup import get_logger
from src.business.ai.gemini_api import GeminiAPIService
from src.business.ai.logging_ai_decorator import LoggingAIDecorator
from src.business.interfaces.IAIService import IAIInterface
from src.data.interfaces.ICrudRepository import ICrudRepository # Still needed for composition

# Define a TypeVar for the interface type for cleaner type hinting
I = TypeVar('I')

class DependencyContainer:
    def resolve(self, interface):
        """
        Resolves and returns the instance registered for the given interface.
        Raises KeyError if the interface is not registered.
        """
        if interface in self._singletons:
            return self._singletons[interface]
        if interface in self._registrations:
            # If not a singleton, create a new instance from the registration
            return self._registrations[interface]()
        raise KeyError(f"No registration found for interface: {interface}")
    # Your existing __init__, _get_key, register, register_singleton, register_instance, resolve, reset methods go here.
    # ... (existing methods as provided in your prompt) ...

    # This is the primary method to update for configuring your application's dependencies
    def configure_application_dependencies(self):
        """
        Configures the application's dependencies by registering interfaces
        with their concrete implementations and applying decorators.
        This method is called once during application startup.
        """
        logger.info("INFO - Configuring application dependencies...")

        # 1. Get the shared logger instance configured by loguru_setup.py
        #    It's good practice to bind a top-level component context to your logger.
        shared_app_logger = get_logger().bind(app_context="jennai-inception")
        self.register_instance(logger.__class__, shared_app_logger) # Register the bound logger if you want to inject it


        # 2. Configure ICrudRepository (example: using a mock or concrete implementation with its own decorator)
        #    You would replace MockCrudRepository with your actual database implementation
        #    (e.g., SqliteRepository, wrapped with a LoggingCrudRepository if you create one).
        class MockCrudRepository(ICrudRepository): # This is a conceptual mock for DI demonstration
            def create(self, entity: Any) -> Any:
                shared_app_logger.debug("MockCrudRepository: Creating entity.")
                return entity
            def read(self, entity_id: Any) -> Optional[Any]:
                shared_app_logger.debug(f"MockCrudRepository: Reading entity with ID: {entity_id}.")
                return {"id": entity_id, "data": "mock_data"}
            def update(self, entity: Any) -> Any:
                shared_app_logger.debug("MockCrudRepository: Updating entity.")
                return entity
            def delete(self, entity_id: Any):
                shared_app_logger.debug(f"MockCrudRepository: Deleting entity with ID: {entity_id}.")
            def list_all(self) -> List[Any]:
                shared_app_logger.debug("MockCrudRepository: Listing all entities.")
                return []
            def read_all(self) -> list:
                shared_app_logger.debug("MockCrudRepository: Reading all entities.")
                return []
            def read_by_id(self, entity_id: Any) -> Optional[Any]:
                shared_app_logger.debug(f"MockCrudRepository: Reading entity by ID: {entity_id}.")
                return {"id": entity_id, "data": "mock_data"}

        # Register ICrudRepository as a singleton, potentially wrapped with logging/validation
        self.register_singleton(ICrudRepository, MockCrudRepository) # Registering the mock as a singleton


        # 3. Configure IAIInterface: Apply the Decorator Pattern for logging
        logger.info("INFO - Registering IAIInterface with logging decorator...")

        # Instantiate the concrete AI service (e.g., GeminiAPIService)
        # It may compose ICrudRepository if needed for its internal operations
        gemini_concrete = GeminiAPIService(
            api_key=os.getenv("GEMINI_API_KEY"), # Get API key from environment variables
            data_repository=self.resolve(ICrudRepository) # Injecting the configured ICrudRepository
        )

        # Wrap the concrete AI service with the logging decorator
        # Pass the shared logger instance (optionally bind with AI-specific context for logs)
        gemini_logged_decorated = LoggingAIDecorator(
            gemini_concrete,
            shared_app_logger.bind(component="AI_Service_Gemini") # More granular logging context
        )

        # Register the decorated AI service with the container as the default IAIInterface
        # Now, any client requesting IAIInterface will get the logging-enabled version
        self.register_singleton(IAIInterface, lambda: gemini_logged_decorated) # Using lambda for lazy singleton creation of decorated service

        # Example for registering an alternative AI service, if needed (e.g., OpenAI)
        # from src.business.ai.openai_api import OpenAIService # Hypothetical OpenAI implementation
        # openai_concrete = OpenAIService(
        #     api_key=os.getenv("OPENAI_API_KEY"),
        #     data_repository=self.resolve(ICrudRepository)
        # )
        # openai_logged_decorated = LoggingAIInterface(
        #     openai_concrete,
        #     shared_app_logger.bind(component="AI_Service_OpenAI")
        # )
        # self.register("IAIInterface_OpenAI", lambda: openai_logged_decorated) # Register by a unique name if you need to choose at runtime


        logger.info("INFO - Application dependencies configured.")

    # Your existing __init__, _get_key, register, register_singleton, register_instance, resolve, reset methods go here.
    # Make sure _configure_application_dependencies() is called from your __init__
    def __init__(self):
        self._registrations: Dict[Any, Any] = {}
        self._singletons: Dict[Any, Any] = {}
        logger.debug("DEBUG - DependencyContainer initialized.")
        self.configure_application_dependencies() # Call the new configuration method here
        
    def register_instance(self, interface, instance):
        self._singletons[interface] = instance

    def register_singleton(self, interface, implementation_or_factory):
        """
        Registers a singleton for the given interface.
        If a class is provided, it will be instantiated once.
        If a factory (callable) is provided, it will be called once to create the instance.
        """
        if callable(implementation_or_factory):
            # Assume it's a factory function or class
            instance = implementation_or_factory()
        else:
            # Assume it's a class type, instantiate it
            instance = implementation_or_factory()
        self._singletons[interface] = instance

    def register_singleton(self, interface, implementation_or_factory):
        """
        Registers a singleton for the given interface. Accepts either a class (which will be instantiated)
        or a factory function/lambda (which will be called to produce the singleton instance).
        """
        if callable(implementation_or_factory) and not isinstance(implementation_or_factory, type):
            # It's a factory function or lambda
            instance = implementation_or_factory()
        else:
            # It's a class/type
            instance = implementation_or_factory()
        self._singletons[interface] = instance