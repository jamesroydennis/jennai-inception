from typing import Any, Dict, List, Optional
from loguru import logger
from src.business.interfaces.IAIService import IAIInterface

class LoggingAIDecorator(IAIInterface):
    """
    A decorator for IAIInterface that adds logging to all AI operations.
    It ensures consistent logging without modifying the concrete AI service implementations.
    """
    def __init__(self, wrapped_ai_service: IAIInterface, logger_instance: Optional[Any] = None):
        if not isinstance(wrapped_ai_service, IAIInterface):
            raise TypeError("wrapped_ai_service must be an instance of IAIInterface")
        self._wrapped_ai_service: IAIInterface = wrapped_ai_service
        self._logger = logger_instance if logger_instance is not None else logger.bind(component="AI")

    def process_text(self, text: str, **kwargs) -> Dict[str, Any]:
        request_id = kwargs.get('request_id', 'N/A')
        self._logger.info(f"[Request ID: {request_id}] AI: Initiating text processing. Input summary: {text[:75]}...")
        try:
            result = self._wrapped_ai_service.process_text(text, **kwargs)
            self._logger.info(f"[Request ID: {request_id}] AI: Text processing successful. Output summary: {str(result)[:75]}...")
            return result
        except Exception as e:
            self._logger.error(f"[Request ID: {request_id}] AI: Error during text processing: {e}", exc_info=True)
            raise

    def generate_image(self, prompt: str, **kwargs) -> bytes:
        request_id = kwargs.get('request_id', 'N/A')
        self._logger.info(f"[Request ID: {request_id}] AI: Initiating image generation for prompt: {prompt[:75]}...")
        try:
            result = self._wrapped_ai_service.generate_image(prompt, **kwargs)
            self._logger.info(f"[Request ID: {request_id}] AI: Image generation successful for prompt: {prompt[:75]}")
            return result
        except Exception as e:
            self._logger.error(f"[Request ID: {request_id}] AI: Error during image generation: {e}", exc_info=True)
            raise

    def embed_text(self, text: str, **kwargs) -> List[float]:
        request_id = kwargs.get('request_id', 'N/A')
        self._logger.info(f"[Request ID: {request_id}] AI: Initiating text embedding for input: {text[:75]}...")
        try:
            result = self._wrapped_ai_service.embed_text(text, **kwargs)
            self._logger.info(f"[Request ID: {request_id}] AI: Text embedding successful for input: {text[:75]}")
            return result
        except Exception as e:
            self._logger.error(f"[Request ID: {request_id}] AI: Error during text embedding: {e}", exc_info=True)
            raise
