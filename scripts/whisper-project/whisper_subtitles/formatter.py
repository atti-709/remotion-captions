"""
SRT formatting utilities for subtitle generation.
"""

from typing import Any


def format_time(seconds: float) -> str:
    """
    Convert seconds to SRT time format (HH:MM:SS,mmm).

    Args:
        seconds: Time in seconds (can include fractional seconds)

    Returns:
        Formatted time string in SRT format

    Example:
        >>> format_time(65.5)
        '00:01:05,500'
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"


def format_segment(index: int, segment: dict[str, Any]) -> str:
    """
    Format a single Whisper segment into SRT format.

    Args:
        index: Segment number (1-based)
        segment: Whisper segment dictionary with 'start', 'end', and 'text' keys

    Returns:
        Formatted SRT segment string
    """
    start_time = format_time(segment["start"])
    end_time = format_time(segment["end"])
    text = segment["text"].strip()

    return f"{index}\n{start_time} --> {end_time}\n{text}\n\n"


def format_srt(segments: list[dict[str, Any]]) -> str:
    """
    Format Whisper segments into complete SRT content.

    Args:
        segments: List of Whisper segment dictionaries

    Returns:
        Complete SRT formatted string
    """
    srt_content = ""
    for i, segment in enumerate(segments, 1):
        srt_content += format_segment(i, segment)
    return srt_content


def save_srt(content: str, output_path: str) -> None:
    """
    Save SRT content to a file.

    Args:
        content: SRT formatted content
        output_path: Path to output file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def preview_srt(content: str, max_lines: int = 20) -> str:
    """
    Generate a preview of SRT content.

    Args:
        content: SRT formatted content
        max_lines: Maximum number of lines to show

    Returns:
        Preview string
    """
    lines = content.split('\n')
    if len(lines) <= max_lines:
        return content

    preview_lines = lines[:max_lines]
    remaining = len(lines) - max_lines
    return '\n'.join(preview_lines) + f"\n\n... ({remaining} more lines)"

