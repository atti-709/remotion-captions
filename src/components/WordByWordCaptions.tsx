import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { CaptionStyle, CaptionConfig } from '../types/subtitles';
import { useSubtitles } from '../hooks/useSubtitles';
import { loadFont } from '@remotion/google-fonts/PlayfairDisplay';

interface WordByWordCaptionsProps extends CaptionStyle, CaptionConfig {
  srtPath: string;
}

export const WordByWordCaptions: React.FC<WordByWordCaptionsProps> = ({
  srtPath,
  fontSize = 48,
  color = '#ffffff',
  wordsPerLine = 4,
  highlightColor = '#ff6b6b',
  backgroundColor = 'rgba(0, 0, 0, 0.8)',
  position = 'bottom',
  fadeInDuration = 0.1,
  fadeOutDuration = 0.1,
  highlightScale = 1.05,
  gap = 8,
  fontFamily,
  fontWeight = 'normal',
  textShadow = 'none',
  padding = 4,
  borderRadius = 6,
  boxShadow = '0 4px 8px rgba(0, 0, 0, 0.3)',
}) => {
  const { fontFamily: playfairFontFamily } = loadFont('normal', {
    weights: ['400', '700'],
    subsets: ['latin', 'latin-ext'],
  });
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { subtitles, loading, error } = useSubtitles(srtPath);

  if (loading || error) {
    return null;
  }

  // Find the current subtitle based on frame
  const currentSubtitle = subtitles.find(
    (subtitle) => frame >= subtitle.startTime * fps && frame <= subtitle.endTime * fps
  );

  if (!currentSubtitle) {
    return null;
  }

  // Split subtitle into words
  const words = currentSubtitle.text.split(' ');
  
  // Calculate which word to highlight based on time progression
  const subtitleProgress = (frame - currentSubtitle.startTime * fps) / ((currentSubtitle.endTime - currentSubtitle.startTime) * fps);
  const currentWordIndex = Math.min(Math.floor(subtitleProgress * words.length), words.length - 1);
  
  // Create word chunks for display
  const chunks = [];
  for (let i = 0; i < words.length; i += wordsPerLine) {
    chunks.push(words.slice(i, i + wordsPerLine));
  }
  
  // Find which chunk contains the current word
  const currentChunkIndex = Math.floor(currentWordIndex / wordsPerLine);
  const currentChunk = chunks[currentChunkIndex] || chunks[0];

  // Calculate opacity for fade in/out
  const fadeInFrames = fps * fadeInDuration;
  const fadeOutFrames = fps * fadeOutDuration;
  const opacity = interpolate(
    frame,
    [
      currentSubtitle.startTime * fps,
      currentSubtitle.startTime * fps + fadeInFrames,
      currentSubtitle.endTime * fps - fadeOutFrames,
      currentSubtitle.endTime * fps,
    ],
    [0, 1, 1, 0],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }
  );

  // Calculate position styles
  const getPositionStyles = () => {
    switch (position) {
      case 'top':
        return { top: 100, bottom: 'auto' };
      case 'center':
        return { top: '50%', bottom: 'auto', transform: 'translateY(-50%)' };
      case 'bottom':
      default:
        // Position in the lower third of the screen
        return { top: '20%' };
    }
  };

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        ...getPositionStyles(),
      }}
    >
      <div
        style={{
          fontSize: `${fontSize}px`,
          color,
          textAlign: 'center',
          fontFamily: fontFamily || playfairFontFamily,
          fontWeight,
          opacity,
          textShadow,
          lineHeight: 1.2,
          maxWidth: '80%',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: `${gap}px`,
        }}
      >
        {currentChunk.map((word, index) => {
          const globalWordIndex = currentChunkIndex * wordsPerLine + index;
          
          return (
            <span
              key={`${currentSubtitle.id}-${globalWordIndex}`}
            >
              {word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};