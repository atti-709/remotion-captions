# Migration Guide: Old Scripts → New Package

This guide helps migrate from the old duplicate scripts to the new refactored package structure.

## What Changed?

### Old Structure (Removed)
```
whisper-project/
├── generate_whisper_subtitles.py  ❌ REMOVED (duplicate logic)
├── subtitle_generator.py          ❌ REMOVED (duplicate logic)
└── main.py                         (was a placeholder)
```

### New Structure
```
whisper-project/
├── whisper_subtitles/              ✅ NEW PACKAGE
│   ├── __init__.py                 (clean exports)
│   ├── cli.py                      (command-line interface)
│   ├── config.py                   (configuration management)
│   ├── formatter.py                (SRT formatting)
│   └── generator.py                (core logic)
├── main.py                          ✅ UPDATED (new entry point)
├── example_usage.py                 ✅ NEW (usage examples)
├── pyproject.toml                   ✅ UPDATED (proper dependencies)
└── README.md                        ✅ UPDATED (comprehensive docs)
```

## Benefits of the Refactor

1. **No Code Duplication**: Unified logic in one place
2. **Better Organization**: Clear separation of concerns
3. **Easier to Test**: Modular design
4. **Better API**: Clean Python API + CLI
5. **More Maintainable**: Single source of truth
6. **Proper Package**: Can be installed and imported
7. **Better Docs**: Comprehensive README and examples

## Migration Examples

### Old Way → New Way

#### Example 1: Basic Usage

**Old (generate_whisper_subtitles.py):**
```python
# Had to run the script directly
python generate_whisper_subtitles.py
```

**New:**
```bash
# CLI with clear options
python main.py Guitar.mp4

# Or with options
python main.py Guitar.mp4 --model large-v3 --preview
```

#### Example 2: English Translation

**Old:**
```bash
python generate_whisper_subtitles.py en
```

**New:**
```bash
python main.py Guitar.mp4 --translate --language sk -o subtitles_en.srt
```

#### Example 3: Python API

**Old (subtitle_generator.py):**
```python
from subtitle_generator import SlovakSubtitleGenerator

generator = SlovakSubtitleGenerator(model_size="large-v3")
generator.generate_subtitles(video_path, output_path, language='sk')
```

**New:**
```python
from whisper_subtitles import SubtitleGenerator

generator = SubtitleGenerator(model_size="large-v3")
generator.generate(video_path, output_path, language='sk')
```

#### Example 4: Custom Configuration

**Old:**
```python
# Parameters passed directly to transcribe
result = model.transcribe(
    video_path,
    language='sk',
    word_timestamps=True,
    temperature=0.0,
    # ... many parameters
)
```

**New:**
```python
from whisper_subtitles import SubtitleGenerator, WhisperConfig

config = WhisperConfig(
    language='sk',
    temperature=0.0,
    beam_size=7
)

generator = SubtitleGenerator(model_size="medium", config=config)
generator.generate(video_path, output_path)
```

## Common Use Cases

### Use Case 1: Generate Slovak Subtitles

```bash
# Old
python generate_whisper_subtitles.py

# New
python main.py Guitar.mp4
```

### Use Case 2: Translate to English

```bash
# Old
python generate_whisper_subtitles.py en

# New
python main.py Guitar.mp4 --translate
```

### Use Case 3: Custom Video File

```bash
# Old (had to modify the script)
# Edit the script and change video_path variable

# New (pass as argument)
python main.py Piano.mp4
```

### Use Case 4: Different Model Size

```bash
# Old (had to modify the script)
# Edit: model = whisper.load_model("medium")

# New (command-line flag)
python main.py Guitar.mp4 --model large-v3
```

## Python API Changes

### Import Changes

```python
# Old
from generate_whisper_subtitles import generate_subtitles
from subtitle_generator import SlovakSubtitleGenerator

# New
from whisper_subtitles import SubtitleGenerator, WhisperConfig
```

### Class/Function Changes

| Old                            | New                                         | Notes               |
| ------------------------------ | ------------------------------------------- | ------------------- |
| `generate_subtitles()`         | `SubtitleGenerator.generate()`              | Now a method        |
| `generate_english_subtitles()` | `SubtitleGenerator.generate_translated()`   | Clearer name        |
| `SlovakSubtitleGenerator`      | `SubtitleGenerator`                         | More general        |
| `format_time()`                | `whisper_subtitles.formatter.format_time()` | In formatter module |

## Advanced Features

### New Features Not in Old Version

1. **Predefined Configurations**
```python
from whisper_subtitles.config import SLOVAK_CONFIG, TRANSLATE_TO_ENGLISH_CONFIG

generator = SubtitleGenerator(config=SLOVAK_CONFIG)
```

2. **Preview Function**
```python
from whisper_subtitles.formatter import preview_srt

preview = preview_srt(srt_content, max_lines=20)
print(preview)
```

3. **Separate Formatting**
```python
from whisper_subtitles.formatter import format_srt, save_srt

result = generator.transcribe(video_path)
srt = format_srt(result["segments"])
save_srt(srt, output_path)
```

4. **Better CLI**
```bash
python main.py --help  # See all options
python main.py Guitar.mp4 --preview  # Show preview
python main.py Guitar.mp4 --quiet  # Suppress output
```

## Installation

### Old Way
```bash
# No proper installation, just run scripts
```

### New Way
```bash
# Install as a package
uv pip install -e .

# Or with pip
pip install -e .

# Then use anywhere
whisper-subtitles Guitar.mp4
```

## Testing the New Package

See `example_usage.py` for comprehensive examples:

```bash
# View the examples
cat example_usage.py

# Edit and run
python example_usage.py
```

## Need Help?

- Read `README.md` for comprehensive documentation
- Check `example_usage.py` for code examples
- Run `python main.py --help` for CLI help

## Summary

The refactored package provides:
- ✅ Same functionality as old scripts
- ✅ Better organization and maintainability
- ✅ Cleaner API (both CLI and Python)
- ✅ No code duplication
- ✅ More features (preview, batch processing, etc.)
- ✅ Better documentation
- ✅ Proper package structure

All the features from the old scripts are preserved and enhanced!

