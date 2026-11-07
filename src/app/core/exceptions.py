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


class DocumentNotFoundError(AppError):
    """A requested document row does not exist."""


class UnsupportedFileTypeError(AppError):
    """No extractor registered for this file extension."""


class TextExtractionError(AppError):
    """Could not extract usable text (empty file / scanned PDF)."""


class FileValidationError(AppError):
    """Uploaded file failed validation (empty, too large, unsupported)."""
