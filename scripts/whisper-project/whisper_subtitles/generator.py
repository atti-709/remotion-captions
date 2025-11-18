"""
Core subtitle generation module using OpenAI Whisper.
"""

from pathlib import Path
from typing import Any

import whisper

from .config import DEFAULT_CONFIG, WhisperConfig
from .formatter import format_srt, save_srt


class SubtitleGenerator:
    """
    Generate subtitles from video files using OpenAI's Whisper model.

    This class handles model loading, transcription, and SRT generation
    with support for multiple languages and translation.

    Example:
        >>> generator = SubtitleGenerator(model_size="turbo")
        >>> generator.generate("video.mp4", "output.srt", language="sk")
    """

    def __init__(self, model_size: str = "turbo", config: WhisperConfig | None = None):
        """
        Initialize the subtitle generator.

        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium",
                       "large", "large-v2", "large-v3", "turbo")
            config: WhisperConfig instance with transcription parameters
        """
        self.model_size = model_size
        self.config = config or DEFAULT_CONFIG
        self.model = None

    def load_model(self) -> None:
        """Load the Whisper model if not already loaded."""
        if self.model is None:
            print(f"🎬 Loading Whisper {self.model_size} model...")
            self.model = whisper.load_model(self.model_size)
            print("✅ Model loaded successfully!")

    def transcribe(self, video_path: str, **kwargs) -> dict[str, Any]:
        """
        Transcribe video file using Whisper.

        Args:
            video_path: Path to video file
            **kwargs: Additional Whisper parameters to override config

        Returns:
            Whisper transcription result dictionary

        Raises:
            FileNotFoundError: If video file doesn't exist
        """
        # Ensure model is loaded
        self.load_model()

        # Validate video path
        video_file = Path(video_path)
        if not video_file.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        print(f"🎬 Transcribing video: {video_path}")

        # Merge config with kwargs
        params = {**self.config.to_whisper_params(), **kwargs}

        # Display transcription mode
        if params.get('task') == 'translate':
            print(f"🌍 Translating from {params['language']} to English...")
        else:
            print(f"📝 Transcribing in {params['language']}...")

        # Transcribe
        result = self.model.transcribe(str(video_path), **params)

        print("✅ Transcription completed!")
        return result

    def generate(
        self,
        video_path: str,
        output_path: str,
        language: str | None = None,
        translate: bool = False,
        **kwargs
    ) -> str:
        """
        Generate subtitles from video and save to SRT file.

        Args:
            video_path: Path to video file
            output_path: Path to output SRT file
            language: Language code (overrides config if provided)
            translate: If True, translate to English (Whisper only supports translation to English)
            **kwargs: Additional Whisper parameters

        Returns:
            Generated SRT content

        Raises:
            FileNotFoundError: If video file doesn't exist
        """
        # Update config if language specified
        if language:
            kwargs['language'] = language

        # Set task based on translate flag
        if translate:
            kwargs['task'] = 'translate'

        # Transcribe the video
        result = self.transcribe(video_path, **kwargs)

        # Format as SRT
        srt_content = format_srt(result["segments"])

        # Save to file
        save_srt(srt_content, output_path)

        print(f"📁 Subtitles saved to: {output_path}")
        return srt_content

    def generate_translated(
        self,
        video_path: str,
        output_path: str,
        source_language: str = "sk",
        **kwargs
    ) -> str:
        """
        Generate English subtitles by translating from source language.

        Note: Whisper can only translate TO English.

        Args:
            video_path: Path to video file
            output_path: Path to output SRT file
            source_language: Source language code
            **kwargs: Additional Whisper parameters

        Returns:
            Generated SRT content
        """
        return self.generate(
            video_path,
            output_path,
            language=source_language,
            translate=True,
            **kwargs
        )

    def update_config(self, **kwargs) -> None:
        """
        Update the configuration parameters.

        Args:
            **kwargs: Configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

