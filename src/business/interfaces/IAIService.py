# File: src/business/interfaces/IAIInterface.py

import abc
from typing import Any, Dict, List, Optional

class IAIInterface(abc.ABC):
    """
    Interface for Artificial Intelligence (AI) service implementations.
    Defines the contract for interacting with various AI models or APIs,
    focusing on computational and generative tasks.
    """

    @abc.abstractmethod
    def process_text(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        Abstract method to process text using the AI service.
        Returns a dictionary containing the processed output and potentially metadata.
        """
        pass

    @abc.abstractmethod
    def generate_image(self, prompt: str, **kwargs) -> bytes:
        """
        Abstract method to generate an image from a prompt.
        Returns the image data as bytes.
        """
        pass

    @abc.abstractmethod
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """
        Abstract method to generate a numerical embedding for text.
        Returns a list of floats representing the embedding.
        """
        pass

    # Add other common AI operations as abstract methods here