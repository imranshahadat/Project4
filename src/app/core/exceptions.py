"""Application exception hierarchy."""


class AppError(Exception):
    """Base class for all application errors."""


class ConfigError(AppError):
    """Invalid or missing configuration."""


class APIKeyMissingError(ConfigError):
    """A required API key is missing or empty."""


class ProviderError(AppError):
    """A provider could not be resolved or initialised."""


class LLMProviderError(ProviderError): ...


class EmbeddingsProviderError(ProviderError): ...


class VectorStoreProviderError(ProviderError): ...


class StorageError(AppError):
    """Object storage failure (missing object, upload error, ...)."""


class StorageProviderError(ProviderError): ...
