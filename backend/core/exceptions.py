class NyayaAIException(Exception):
    """Base exception for Nyaya AI."""
    pass


class SourceFetchError(NyayaAIException):
    """Raised when source/API fetch fails."""
    pass


class DocumentExtractionError(NyayaAIException):
    """Raised when document extraction fails."""
    pass


class GuardrailError(NyayaAIException):
    """Raised when guardrail validation fails."""
    pass


class LLMError(NyayaAIException):
    """Raised when LLM generation fails."""
    pass


class UsageLimitError(NyayaAIException):
    """Raised when user exceeds usage limits."""
    pass