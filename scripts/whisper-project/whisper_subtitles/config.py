"""
Configuration module for Whisper subtitle generation.
"""

from dataclasses import dataclass, field


@dataclass
class WhisperConfig:
    """Configuration for Whisper transcription parameters."""

    # Model settings
    model_size: str = "turbo"

    # Language settings
    language: str = "sk"
    task: str = "transcribe"  # "transcribe" or "translate"

    # Transcription parameters
    word_timestamps: bool = True
    temperature: float = 0.0
    best_of: int = 3
    beam_size: int = 5
    patience: float = 1.0
    length_penalty: float = 1.0
    suppress_tokens: list[int] = field(default_factory=lambda: [-1])
    
    # Anti-hallucination parameters
    condition_on_previous_text: bool = False  # Prevents repetition
    compression_ratio_threshold: float = 2.4  # Detects repetitive text
    logprob_threshold: float = -1.0  # Detects low-confidence segments
    no_speech_threshold: float = 0.6  # Detects silence/music

    # Language-specific prompts
    initial_prompt: str | None = None

    def __post_init__(self):
        """Set language-specific defaults after initialization."""
        if self.initial_prompt is None and self.language == "sk":
            self.initial_prompt = "Slovenský text o teológii a kresťanstve."

    def to_whisper_params(self) -> dict:
        """Convert config to Whisper transcribe parameters."""
        return {
            'language': self.language,
            'task': self.task,
            'word_timestamps': self.word_timestamps,
            'temperature': self.temperature,
            'best_of': self.best_of,
            'beam_size': self.beam_size,
            'patience': self.patience,
            'length_penalty': self.length_penalty,
            'suppress_tokens': self.suppress_tokens,
            'initial_prompt': self.initial_prompt or "",
            'condition_on_previous_text': self.condition_on_previous_text,
            'compression_ratio_threshold': self.compression_ratio_threshold,
            'logprob_threshold': self.logprob_threshold,
            'no_speech_threshold': self.no_speech_threshold
        }


# Default configurations for common use cases
DEFAULT_CONFIG = WhisperConfig()

SLOVAK_CONFIG = WhisperConfig(
    language="sk",
    task="transcribe",
    initial_prompt="Slovenský text o teológii a kresťanstve."
)

TRANSLATE_TO_ENGLISH_CONFIG = WhisperConfig(
    language="sk",
    task="translate",
    initial_prompt=""
)

ENGLISH_CONFIG = WhisperConfig(
    language="en",
    task="transcribe",
    initial_prompt=""
)

