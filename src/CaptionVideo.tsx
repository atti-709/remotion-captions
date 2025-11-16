import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';
import { WordByWordCaptions } from './components/WordByWordCaptions';
import { VideoCompositionProps } from './types/video';
import { defaultCaptionStyle, defaultCaptionConfig } from './config/captionStyles';

interface CaptionVideoProps extends VideoCompositionProps {}

export const CaptionVideo: React.FC<CaptionVideoProps> = ({
  title,
  subtitle,
  backgroundColor,
  textColor,
  videoSrc,
}) => {

  return (
    <AbsoluteFill>
      {/* Source video as background */}
      <OffthreadVideo
        src={videoSrc}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
      />
      
      {/* Dark overlay for better text readability */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.3)',
        }}
      />

      {/* Render word-by-word captions with highlighting */}
      <WordByWordCaptions
        srtPath={staticFile('subtitles_en.srt')}
        {...defaultCaptionStyle}
        {...defaultCaptionConfig}
        color={textColor}
      />
    </AbsoluteFill>
  );
};