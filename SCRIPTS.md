# Available Scripts

This document describes all the available npm scripts for the remotion-captions project.

## Remotion Scripts

### `npm start`
Start the Remotion Studio for live preview and development.

```bash
npm start
```

Opens the Remotion Studio at `http://localhost:3000` where you can preview and edit your video compositions.

### `npm run build`
Render the final video with captions.

```bash
npm run build
```

Renders the `CaptionVideo` composition and outputs to `out/video.mp4`.

### `npm run upgrade`
Upgrade Remotion to the latest version.

```bash
npm run upgrade
```

## Subtitle Generation Scripts

All subtitle generation scripts use the refactored `whisper-project` package with the **turbo** model by default (fast and accurate).

### `npm run subtitles`
Generate Slovak subtitles from `Guitar.mp4`.

```bash
npm run subtitles
```

**Output:** `public/subtitles.srt`

### `npm run subtitles:en`
Generate English subtitles by translating from Slovak.

```bash
npm run subtitles:en
```

**Output:** `public/subtitles_en.srt`

### `npm run subtitles:preview`
Generate subtitles and show a preview in the terminal.

```bash
npm run subtitles:preview
```

Great for checking the output before using it in your video.

### `npm run subtitles:help`
Show all available subtitle generation options.

```bash
npm run subtitles:help
```

## Python Linting Scripts

### `npm run lint:python`
Check Python code quality with ruff.

```bash
npm run lint:python
```

Checks the `whisper_subtitles` package for linting issues.

### `npm run lint:python:fix`
Auto-fix Python linting issues.

```bash
npm run lint:python:fix
```

Automatically fixes most linting issues in the Python codebase.

## Advanced Subtitle Generation

For more control over subtitle generation, you can use the Python CLI directly with `uv run`:

### Custom Video File

```bash
cd scripts/whisper-project
uv run main.py Piano.mp4
```

### Different Model

```bash
# Faster but less accurate
uv run main.py Guitar.mp4 --model small

# Best quality (slower)
uv run main.py Guitar.mp4 --model large-v3
```

### Custom Output Path

```bash
uv run main.py Guitar.mp4 -o custom_output.srt
```

### Custom Parameters

```bash
uv run main.py Guitar.mp4 \
  --model turbo \
  --language sk \
  --temperature 0.2 \
  --beam-size 7 \
  --preview
```

### All Options

```bash
cd scripts/whisper-project
uv run main.py --help
```

## Workflow Examples

### Generate Slovak and English Subtitles

```bash
# Generate Slovak version
npm run subtitles

# Generate English translation
npm run subtitles:en

# Preview both
cat public/subtitles.srt
cat public/subtitles_en.srt
```

### Preview Before Rendering

```bash
# Generate subtitles with preview
npm run subtitles:preview

# Start Remotion Studio
npm start

# Render final video
npm run build
```

### Python Development Workflow

```bash
# Make changes to whisper_subtitles/

# Check for linting issues
npm run lint:python

# Auto-fix issues
npm run lint:python:fix

# Test the changes
cd scripts/whisper-project
uv run main.py Guitar.mp4 --preview
```

## Quick Reference

| Command                     | Description                |
| --------------------------- | -------------------------- |
| `npm start`                 | Start Remotion Studio      |
| `npm run build`             | Render final video         |
| `npm run subtitles`         | Generate Slovak subtitles  |
| `npm run subtitles:en`      | Generate English subtitles |
| `npm run subtitles:preview` | Generate with preview      |
| `npm run subtitles:help`    | Show subtitle options      |
| `npm run lint:python`       | Check Python code          |
| `npm run lint:python:fix`   | Fix Python linting issues  |

## Tips

1. **Model Selection**: The default `turbo` model provides the best balance of speed and accuracy. Use `large-v3` for best quality or `small` for faster processing.

2. **Language Support**: The package supports all languages that Whisper supports. Use `--language` flag to specify.

3. **Translation**: Whisper can only translate TO English. For other target languages, generate subtitles in the source language and use a separate translation service.

4. **Preview First**: Always use `--preview` flag to check output before committing to a long render.

5. **Batch Processing**: For multiple videos, write a simple bash script or use the Python API directly with `uv run`.

## Need Help?

- **Remotion**: See the [main README](README.md)
- **Whisper Subtitles**: See [scripts/whisper-project/README.md](scripts/whisper-project/README.md)
- **Quick Start**: See [scripts/whisper-project/QUICKSTART.md](scripts/whisper-project/QUICKSTART.md)
- **Migration**: See [scripts/whisper-project/MIGRATION.md](scripts/whisper-project/MIGRATION.md)

