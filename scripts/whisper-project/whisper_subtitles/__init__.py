"""
Whisper Subtitles Package
~~~~~~~~~~~~~~~~~~~~~~~~~

A package for generating subtitles from video files using OpenAI's Whisper model.

Usage:
    from whisper_subtitles import SubtitleGenerator

    generator = SubtitleGenerator(model_size="turbo")
    generator.generate("video.mp4", "output.srt", language="sk")
"""

from .config import DEFAULT_CONFIG, WhisperConfig
from .generator import SubtitleGenerator

__version__ = "0.2.0"
__all__ = ["SubtitleGenerator", "WhisperConfig", "DEFAULT_CONFIG"]

