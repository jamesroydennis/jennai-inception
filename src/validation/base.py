"""
Base validation interface and example implementation for JennAI.
This module is designed for dependency injection and cross-cutting concerns (logging, etc).
"""
from abc import ABC, abstractmethod
from typing import Any

class ValidationError(Exception):
    pass

class BaseValidator(ABC):
    def __init__(self, logger):
        self.logger = logger

    def validate(self, data: Any) -> bool:
        self.logger.info(f"Starting validation with {self.__class__.__name__}")
        try:
            result = self._validate(data)
            self.logger.info(f"Validation succeeded: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            raise ValidationError(str(e)) from e

    @abstractmethod
    def _validate(self, data: Any) -> bool:
        """Implement concrete validation logic here."""
        pass

# Example concrete validator
class RoleValidator(BaseValidator):
    def __init__(self, logger, valid_roles):
        super().__init__(logger)
        self.valid_roles = valid_roles

    def _validate(self, role: str) -> bool:
        if role not in self.valid_roles:
            raise ValueError(f"Role '{role}' is not valid. Allowed: {self.valid_roles}")
        return True
