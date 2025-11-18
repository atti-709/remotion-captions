# Whisper Subtitles Generator

A Python package for generating high-quality subtitles from video files using OpenAI's Whisper model.

## Features

- 🎯 **Multi-language support**: Transcribe in any language Whisper supports
- 🌍 **Translation**: Translate subtitles to English (Whisper's only translation target)
- 🎬 **Multiple model sizes**: Choose from tiny to large-v3 based on your accuracy/speed needs
- 📝 **SRT format**: Generates standard SRT subtitle files
- ⚙️ **Configurable**: Fine-tune transcription parameters
- 🏗️ **Well-structured**: Clean, modular, and maintainable codebase

## Installation

```bash
# Using uv (recommended)
cd scripts/whisper-project
uv pip install -e .

# Or using pip
pip install -e .
```

## Quick Start

### Command Line Usage

```bash
# Generate Slovak subtitles from a video
uv run main.py Guitar.mp4

# Generate English subtitles by translating from Slovak
uv run main.py Guitar.mp4 --translate --language sk -o subtitles_en.srt

# Use a specific model size
uv run main.py Piano.mp4 --model large-v3

# Show preview of generated subtitles
uv run main.py Guitar.mp4 --preview

# Get help
uv run main.py --help
```

### Python API Usage

```python
from whisper_subtitles import SubtitleGenerator, WhisperConfig

# Basic usage (uses 'turbo' by default)
generator = SubtitleGenerator()
generator.generate("video.mp4", "output.srt", language="sk")

# With custom configuration
config = WhisperConfig(
    language="sk",
    temperature=0.2,
    beam_size=7,
    initial_prompt="Slovenský text o teológii."
)
generator = SubtitleGenerator(model_size="large-v3", config=config)
generator.generate("video.mp4", "output.srt")

# Translation mode
generator.generate_translated(
    "video.mp4",
    "output_en.srt",
    source_language="sk"
)
```

## Project Structure

```
whisper-project/
├── whisper_subtitles/          # Main package
│   ├── __init__.py            # Package exports
│   ├── cli.py                 # Command-line interface
│   ├── config.py              # Configuration management
│   ├── formatter.py           # SRT formatting utilities
│   └── generator.py           # Core subtitle generation
├── main.py                     # Entry point script
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## Architecture

The package is organized into focused modules:

- **`generator.py`**: Core `SubtitleGenerator` class for video transcription
- **`config.py`**: `WhisperConfig` dataclass for managing Whisper parameters
- **`formatter.py`**: SRT formatting utilities (time formatting, segment formatting)
- **`cli.py`**: Command-line interface with argument parsing
- **`main.py`**: Simple entry point that delegates to CLI

## Configuration

### Model Sizes

| Model    | Parameters | English-only | Multilingual | Speed | Accuracy  |
| -------- | ---------- | ------------ | ------------ | ----- | --------- |
| tiny     | 39 M       | ✓            | ✓            | ~32x  | Lower     |
| base     | 74 M       | ✓            | ✓            | ~16x  | Low       |
| small    | 244 M      | ✓            | ✓            | ~6x   | Medium    |
| medium   | 769 M      | ✓            | ✓            | ~2x   | Good      |
| large    | 1550 M     | -            | ✓            | 1x    | Best      |
| large-v2 | 1550 M     | -            | ✓            | 1x    | Best      |
| large-v3 | 1550 M     | -            | ✓            | 1x    | Best      |
| turbo    | 809 M      | -            | ✓            | ~8x   | Very Good |

**Default: turbo** - Optimized for speed with very good accuracy

### Common Languages

- `sk` - Slovak
- `en` - English
- `de` - German
- `fr` - French
- `es` - Spanish
- `it` - Italian
- `cs` - Czech
- `pl` - Polish

See [Whisper documentation](https://github.com/openai/whisper) for full language list.

## Advanced Usage

### Custom Whisper Parameters

```python
from whisper_subtitles import SubtitleGenerator

generator = SubtitleGenerator(model_size="large-v3")

# Pass custom parameters directly to transcribe
result = generator.generate(
    "video.mp4",
    "output.srt",
    language="sk",
    temperature=0.2,
    beam_size=7,
    patience=2.0,
    initial_prompt="Špecifický kontext pre lepšiu presnosť."
)
```

### Using Pre-defined Configs

```python
from whisper_subtitles import SubtitleGenerator
from whisper_subtitles.config import (
    SLOVAK_CONFIG,
    ENGLISH_CONFIG,
    TRANSLATE_TO_ENGLISH_CONFIG
)

# Slovak transcription
generator = SubtitleGenerator(config=SLOVAK_CONFIG)
generator.generate("video.mp4", "slovak.srt")

# Translation to English
generator = SubtitleGenerator(config=TRANSLATE_TO_ENGLISH_CONFIG)
generator.generate("video.mp4", "english.srt")
```

## Examples

### Example 1: Batch Processing

```python
from pathlib import Path
from whisper_subtitles import SubtitleGenerator

generator = SubtitleGenerator(model_size="medium")

video_dir = Path("videos")
for video_file in video_dir.glob("*.mp4"):
    output_file = video_file.with_suffix(".srt")
    print(f"Processing {video_file}...")
    generator.generate(str(video_file), str(output_file))
```

### Example 2: Multiple Languages

```python
from whisper_subtitles import SubtitleGenerator

generator = SubtitleGenerator(model_size="large-v3")

# Generate Slovak version
generator.generate("video.mp4", "subtitles_sk.srt", language="sk")

# Generate English translation
generator.generate("video.mp4", "subtitles_en.srt", language="sk", translate=True)
```

## CLI Reference

```
usage: main.py [-h] [-o OUTPUT] [-m MODEL] [-l LANGUAGE] [--translate]
               [--temperature TEMPERATURE] [--best-of BEST_OF]
               [--beam-size BEAM_SIZE] [--initial-prompt INITIAL_PROMPT]
               [--preview] [--quiet]
               video

positional arguments:
  video                 Video filename (in public/assets/) or full path

options:
  -h, --help            Show help message and exit
  -o, --output          Output SRT file path
  -m, --model           Whisper model size (default: medium)
  -l, --language        Source language code (default: sk)
  --translate           Translate to English
  --temperature         Temperature for sampling (default: 0.0)
  --best-of             Number of candidates (default: 3)
  --beam-size           Beam size for search (default: 5)
  --initial-prompt      Initial prompt to guide transcription
  --preview             Show preview of generated subtitles
  --quiet               Suppress progress output
```

## Development

### Setup Development Environment

```bash
# Install package with dev dependencies
uv pip install -e ".[dev]"
```

### Code Quality

The project uses **ruff** for linting and formatting:

```bash
# Check for linting issues
ruff check whisper_subtitles/

# Auto-fix linting issues
ruff check --fix whisper_subtitles/

# Format code
ruff format whisper_subtitles/
```

### Running Tests

```bash
# Run tests (when available)
pytest
```

## Requirements

- Python 3.10+
- openai-whisper
- torch
- numpy

## Tips for Best Results

1. **Use larger models for better accuracy**: `large-v3` gives best results but is slower
2. **Provide context in initial_prompt**: Helps Whisper understand domain-specific terminology
3. **Use temperature=0.0 for deterministic results**: Good for consistency
4. **Adjust beam_size**: Higher values (7-10) can improve quality but are slower
5. **For noisy audio**: Try increasing `patience` parameter

## Troubleshooting

### Out of Memory

If you get CUDA out of memory errors, try:
- Using a smaller model (`small` or `medium`)
- Processing shorter video segments
- Running on CPU (slower but uses system RAM)

### Incorrect Transcription

Try:
- Using a larger model (`large-v3`)
- Providing a relevant `initial_prompt`
- Adjusting `temperature` (try 0.2-0.5)
- Increasing `beam_size` (try 7-10)

## License

This project uses OpenAI's Whisper model. See Whisper's license for details.

## Credits

Built on [OpenAI Whisper](https://github.com/openai/whisper)

