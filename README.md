# Remotion Slovak Captions

A Remotion project for generating videos with Slovak captions and subtitles.

## Features

- 🎬 Automatic Slovak subtitle generation using Whisper AI
- ⏱️ Precise timing control for each caption
- 🎨 Flexible styling options (colors, fonts, positions)
- 📱 Responsive design for different video dimensions
- 🚀 Easy to customize and extend
- 🧠 High-quality AI transcription using Whisper large-v3 model
- ⚡ Fast and clean dependency management with `uv`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Generate Slovak subtitles from your video:
```bash
npm run generate-subtitles
```

3. Start the Remotion Studio:
```bash
npm start
```

## Usage

### Basic Usage

The project includes a sample composition called `CaptionVideo` with:
- A welcome title in Slovak
- A subtitle explaining the purpose
- A thank you message

### Customizing Captions

Edit `src/CaptionVideo.tsx` to modify the captions:

```typescript
const captions = [
  {
    text: 'Váš vlastný text',
    startFrame: 0,
    endFrame: fps * 3, // 3 seconds
    position: 'center' as const,
    fontSize: 64,
  },
  // Add more captions...
];
```

### Caption Properties

- `text`: The Slovak text to display
- `startFrame`: Frame when caption appears
- `endFrame`: Frame when caption disappears
- `position`: 'top', 'center', or 'bottom'
- `fontSize`: Size of the text in pixels

### Rendering Video

To render your video:

```bash
npm run build
```

## Project Structure

```
src/
├── Root.tsx                    # Main composition registration
├── CaptionVideo.tsx            # Main video component
├── components/                 # Reusable UI components
│   ├── WordByWordCaptions.tsx  # Advanced word-by-word captions
│   ├── SlovakCaption.tsx       # Basic caption component
│   └── index.ts               # Component exports
├── types/                      # TypeScript type definitions
│   ├── subtitles.ts           # Subtitle-related types
│   ├── video.ts               # Video-related types
│   └── index.ts               # Type exports
├── hooks/                      # Custom React hooks
│   └── useSubtitles.ts        # Subtitle loading hook
├── utils/                      # Utility functions
│   └── srtParser.ts           # SRT file parsing
├── config/                     # Configuration files
│   ├── captionStyles.ts       # Predefined caption styles
│   └── index.ts               # Config exports
└── scripts/                    # Subtitle generation scripts
    └── whisper-project/        # Whisper AI integration
        └── subtitle_generator.py
```

## Customization

### Colors and Styling

#### Using Predefined Styles

Import and use predefined caption styles from `src/config/captionStyles.ts`:

```typescript
import { tiktokStyle, youtubeStyle, instagramStyle } from './config/captionStyles';

// Use TikTok-style captions
<WordByWordCaptions
  srtPath={staticFile('subtitles.srt')}
  {...tiktokStyle}
  {...defaultCaptionConfig}
/>
```

#### Custom Styling

Modify the default props in `src/Root.tsx`:

```typescript
defaultProps={{
  title: 'Váš titulok',
  subtitle: 'Váš podtitulok',
  backgroundColor: '#1a1a1a',
  textColor: '#ffffff',
}}
```

#### Advanced Caption Configuration

Customize caption behavior in `src/CaptionVideo.tsx`:

```typescript
<WordByWordCaptions
  srtPath={staticFile('subtitles.srt')}
  fontSize={52}
  wordsPerLine={4}
  highlightColor="#ff6b6b"
  backgroundColor="rgba(0, 0, 0, 0.7)"
  position="center"
  fadeInDuration={0.2}
  highlightScale={1.1}
/>
```

### Adding More Captions

Create additional caption sequences by adding more objects to the `captions` array in `CaptionVideo.tsx`.

### Different Video Dimensions

Update the composition settings in `src/Root.tsx`:

```typescript
width={1920}
height={1080}
```

## Slovak Text Examples

Here are some common Slovak phrases you might want to use:

- "Vitajte v našom videu" - Welcome to our video
- "Ďakujeme za pozornosť" - Thank you for your attention
- "Pokračujte v sledovaní" - Continue watching
- "Nezabudnite sa prihlásiť" - Don't forget to subscribe
- "Lajkujte ak sa vám páči" - Like if you enjoy it

## Tips

1. **Timing**: Use `fps * seconds` to convert time to frames
2. **Readability**: Ensure sufficient contrast between text and background
3. **Duration**: Keep captions on screen long enough to be read comfortably
4. **Positioning**: Use 'center' for important messages, 'bottom' for subtitles

## Next Steps

- Add background video support
- Implement subtitle file (.srt) parsing
- Add animation effects for captions
- Create multiple composition templates