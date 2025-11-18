#!/usr/bin/env python3
"""
Example usage of the refactored whisper_subtitles package.
This demonstrates the clean API and various use cases.
"""

from pathlib import Path

from whisper_subtitles import SubtitleGenerator, WhisperConfig
from whisper_subtitles.config import SLOVAK_CONFIG, TRANSLATE_TO_ENGLISH_CONFIG

# Get project root
project_root = Path(__file__).parent.parent.parent
video_path = project_root / "public" / "assets" / "Guitar.mp4"


def example_1_basic_usage():
    """Example 1: Basic subtitle generation"""
    print("=" * 60)
    print("Example 1: Basic Slovak Subtitle Generation")
    print("=" * 60)

    generator = SubtitleGenerator()  # Uses 'turbo' by default
    output_path = project_root / "public" / "subtitles_example.srt"

    # This will load the model, transcribe, and save
    srt_content = generator.generate(
        str(video_path),
        str(output_path),
        language="sk"
    )

    print(f"✅ Generated {len(srt_content)} characters of subtitles\n")


def example_2_translation():
    """Example 2: Translation to English"""
    print("=" * 60)
    print("Example 2: Translation to English")
    print("=" * 60)

    generator = SubtitleGenerator()  # Uses 'turbo' by default
    output_path = project_root / "public" / "subtitles_en_example.srt"

    # Translate Slovak to English
    srt_content = generator.generate_translated(
        str(video_path),
        str(output_path),
        source_language="sk"
    )

    print(f"✅ Generated {len(srt_content)} characters of translated subtitles\n")


def example_3_custom_config():
    """Example 3: Using custom configuration"""
    print("=" * 60)
    print("Example 3: Custom Configuration")
    print("=" * 60)

    # Create custom configuration
    config = WhisperConfig(
        language="sk",
        temperature=0.2,
        beam_size=7,
        initial_prompt="Slovenský text o hudbe a gitare."
    )

    generator = SubtitleGenerator(model_size="medium", config=config)
    output_path = project_root / "public" / "subtitles_custom.srt"

    srt_content = generator.generate(str(video_path), str(output_path))

    print(f"✅ Generated with custom config: {len(srt_content)} characters\n")


def example_4_predefined_configs():
    """Example 4: Using predefined configurations"""
    print("=" * 60)
    print("Example 4: Predefined Configurations")
    print("=" * 60)

    # Slovak transcription
    SubtitleGenerator(model_size="medium", config=SLOVAK_CONFIG)

    # English translation
    SubtitleGenerator(model_size="medium", config=TRANSLATE_TO_ENGLISH_CONFIG)

    print("✅ Generators configured with predefined configs\n")


def example_5_direct_api():
    """Example 5: Using the API programmatically"""
    print("=" * 60)
    print("Example 5: Direct API Usage")
    print("=" * 60)

    from whisper_subtitles.formatter import format_srt, preview_srt, save_srt

    generator = SubtitleGenerator()  # Uses 'turbo' by default

    # Just transcribe, don't save yet
    result = generator.transcribe(str(video_path), language="sk")

    # Format the result
    srt_content = format_srt(result["segments"])

    # Preview first
    preview = preview_srt(srt_content, max_lines=10)
    print("Preview:")
    print(preview)

    # Save when ready
    output_path = project_root / "public" / "subtitles_api.srt"
    save_srt(srt_content, str(output_path))

    print("\n✅ API usage complete\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("WHISPER SUBTITLES PACKAGE - USAGE EXAMPLES")
    print("=" * 60 + "\n")

    print("This demonstrates the refactored package structure.")
    print("Uncomment the examples you want to run.\n")

    # Uncomment to run examples:
    # example_1_basic_usage()
    # example_2_translation()
    # example_3_custom_config()
    # example_4_predefined_configs()
    # example_5_direct_api()

    print("\nNote: These examples require the video file to exist.")
    print(f"Expected location: {video_path}")
    print("\nTo run, uncomment the example functions above.")

