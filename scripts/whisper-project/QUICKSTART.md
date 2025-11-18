# Quick Start Guide (uv)

Quick guide for getting started with the refactored whisper-subtitles package using `uv`.

## Installation

```bash
cd scripts/whisper-project

# Install the package in development mode
uv pip install -e .
```

## Basic Usage

### 1. Generate Slovak Subtitles

```bash
uv run main.py Guitar.mp4
```

This will:
- Look for `Guitar.mp4` in `public/assets/`
- Generate Slovak subtitles
- Save to `public/subtitles.srt`

### 2. Translate to English

```bash
uv run main.py Guitar.mp4 --translate
```

Saves to `public/subtitles_en.srt` by default.

### 3. Specify Output File

```bash
uv run main.py Piano.mp4 -o my_subtitles.srt
```

### 4. Use Different Model

```bash
# Faster but less accurate
uv run main.py Guitar.mp4 --model small

# Best quality (slower)
uv run main.py Guitar.mp4 --model large-v3
```

### 5. See All Options

```bash
uv run main.py --help
```

## Python API

```python
from whisper_subtitles import SubtitleGenerator

# Create generator (uses 'turbo' by default for speed and accuracy)
generator = SubtitleGenerator()

# Generate subtitles
generator.generate(
    "path/to/video.mp4",
    "output.srt",
    language="sk"
)
```

## Using with uv run

The `uv run` command automatically manages dependencies:

```bash
cd scripts/whisper-project

# uv run handles dependencies automatically
uv run main.py Guitar.mp4

# No need to manually install or activate venv!
```

## Troubleshooting

### Missing whisper module

If you get `ModuleNotFoundError: No module named 'whisper'`:

```bash
cd scripts/whisper-project
uv pip install -e .
```

### Video not found

Make sure your video is in `public/assets/` or provide the full path:

```bash
python main.py /full/path/to/video.mp4
```

## Examples

See `example_usage.py` for comprehensive Python API examples:

```bash
uv run example_usage.py
```

## Next Steps

- Read `README.md` for full documentation
- Check `MIGRATION.md` if upgrading from old scripts
- Explore `example_usage.py` for API examples

## Package Structure

```
whisper-project/
├── whisper_subtitles/     # The main package
│   ├── __init__.py       # Exports: SubtitleGenerator, WhisperConfig
│   ├── cli.py            # Command-line interface
│   ├── config.py         # Configuration classes
│   ├── formatter.py      # SRT formatting utilities
│   └── generator.py      # Core subtitle generation
├── main.py               # CLI entry point
├── example_usage.py      # Usage examples
└── pyproject.toml        # Package configuration
```

## Common Commands

```bash
# Generate Slovak subtitles
uv run main.py Guitar.mp4

# Translate to English
uv run main.py Guitar.mp4 --translate

# Custom output
uv run main.py Piano.mp4 -o piano_subs.srt

# Different model
uv run main.py Guitar.mp4 --model large-v3

# Show preview
uv run main.py Guitar.mp4 --preview

# All at once
uv run main.py Guitar.mp4 --translate --model large-v3 --preview -o result.srt
```

