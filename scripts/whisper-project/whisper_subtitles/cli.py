"""
Command-line interface for subtitle generation.
"""

import argparse
import sys
from pathlib import Path

from .config import WhisperConfig
from .formatter import preview_srt
from .generator import SubtitleGenerator


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate subtitles from video using OpenAI Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Slovak subtitles from video
  %(prog)s Guitar.mp4

  # Generate English subtitles by translating from Slovak
  %(prog)s Guitar.mp4 --translate --language sk

  # Specify output file and model
  %(prog)s Guitar.mp4 -o output.srt --model large-v3

  # Generate with custom parameters
  %(prog)s Piano.mp4 --language en --temperature 0.2 --beam-size 7
        """
    )

    # Required arguments
    parser.add_argument(
        "video",
        help="Video filename (in public/assets/) or full path"
    )

    # Output options
    parser.add_argument(
        "-o",
        "--output",
        help="Output SRT file path (default: public/subtitles.srt or subtitles_en.srt)",
    )

    # Model options
    parser.add_argument(
        "-m", "--model",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3", "turbo"],
        default="medium",
        help="Whisper model size (default: turbo)"
    )

    # Language options
    parser.add_argument(
        "-l", "--language",
        default="sk",
        help="Source language code (default: sk)"
    )

    parser.add_argument(
        "--translate",
        action="store_true",
        help="Translate to English (Whisper only supports translation to English)",
        default=False
    )

    # Advanced Whisper parameters
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Temperature for sampling (default: 0.0 for deterministic)"
    )

    parser.add_argument(
        "--best-of",
        type=int,
        default=3,
        help="Number of candidates to generate (default: 3)"
    )

    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Beam size for beam search (default: 5)"
    )

    parser.add_argument(
        "--initial-prompt",
        help="Initial prompt to guide transcription"
    )

    # Anti-hallucination parameters
    parser.add_argument(
        "--condition-on-previous-text",
        action="store_true",
        help="Condition on previous text (can cause repetition, default: False)"
    )

    parser.add_argument(
        "--compression-ratio-threshold",
        type=float,
        default=2.4,
        help="Compression ratio threshold to detect repetitive text (default: 2.4)"
    )

    parser.add_argument(
        "--logprob-threshold",
        type=float,
        default=-1.0,
        help="Log probability threshold to detect low-confidence segments (default: -1.0)"
    )

    parser.add_argument(
        "--no-speech-threshold",
        type=float,
        default=0.6,
        help="No-speech threshold to detect silence/music (default: 0.6)"
    )

    # Display options
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show preview of generated subtitles"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )

    return parser.parse_args()


def resolve_paths(
    video_arg: str,
    output_arg: str | None,
    translate: bool
) -> tuple[Path, Path]:
    """
    Resolve video and output paths.

    Args:
        video_arg: Video filename or path from command line
        output_arg: Output path from command line (or None)
        translate: Whether translation mode is enabled

    Returns:
        Tuple of (video_path, output_path)
    """
    # Get project root: whisper_subtitles/ -> whisper-project/ -> scripts/ -> root
    script_dir = Path(__file__).parent  # whisper_subtitles/
    whisper_project = script_dir.parent  # whisper-project/
    scripts_dir = whisper_project.parent  # scripts/
    project_root = scripts_dir.parent  # remotion-captions/

    # Resolve video path
    video_path = Path(video_arg)
    if not video_path.is_absolute():
        # Check if it's in public/assets/
        assets_path = project_root / "public" / "assets" / video_arg
        if assets_path.exists():
            video_path = assets_path
        else:
            # Try as relative to current directory
            if not video_path.exists():
                print(f"❌ Video file not found: {video_arg}")
                print(f"   Searched in: {assets_path}")
                print(f"   And: {video_path.absolute()}")
                sys.exit(1)

    # Resolve output path
    if output_arg:
        output_path = Path(output_arg)
        if not output_path.is_absolute():
            # If path has directory components (e.g., ../foo, dir/file), resolve from CWD
            # Otherwise, it's just a filename - put it in project_root/public
            if output_path.parent != Path("."):
                output_path = output_path.resolve()
            else:
                output_path = project_root / "public" / output_arg
    else:
        # Default output path
        if translate:
            output_path = project_root / "public" / "subtitles_en.srt"
        else:
            output_path = project_root / "public" / "subtitles.srt"

    return video_path, output_path


def run_cli():
    """Main CLI entry point."""
    args = parse_args()

    try:
        # Resolve paths
        video_path, output_path = resolve_paths(
            args.video,
            args.output,
            args.translate
        )

        print(f"📹 Video: {video_path}")
        print(f"📄 Output: {output_path}")
        print()

        # Create configuration
        config = WhisperConfig(
            model_size=args.model,
            language=args.language,
            task="translate" if args.translate else "transcribe",
            temperature=args.temperature,
            best_of=args.best_of,
            beam_size=args.beam_size,
            initial_prompt=args.initial_prompt,
            condition_on_previous_text=args.condition_on_previous_text,
            compression_ratio_threshold=args.compression_ratio_threshold,
            logprob_threshold=args.logprob_threshold,
            no_speech_threshold=args.no_speech_threshold
        )

        # Create generator
        generator = SubtitleGenerator(model_size=args.model, config=config)

        # Generate subtitles
        srt_content = generator.generate(
            str(video_path),
            str(output_path),
            translate=args.translate
        )

        # Show preview if requested
        if args.preview:
            print("\n📝 Preview of generated subtitles:")
            print("=" * 60)
            print(preview_srt(srt_content, max_lines=30))
            print("=" * 60)

        print("\n✅ Subtitles generated successfully!")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating subtitles: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_cli()

