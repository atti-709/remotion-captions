import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

interface SlovakCaptionProps {
  text: string;
  startFrame: number;
  endFrame: number;
  position?: 'top' | 'center' | 'bottom';
  fontSize?: number;
  color?: string;
  backgroundColor?: string;
  padding?: number;
}

export const SlovakCaption: React.FC<SlovakCaptionProps> = ({
  text,
  startFrame,
  endFrame,
  position = 'bottom',
  fontSize = 48,
  color = '#ffffff',
  backgroundColor = 'rgba(0, 0, 0, 0.8)',
  padding = 20,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Calculate opacity based on frame timing
  const opacity = interpolate(
    frame,
    [startFrame, startFrame + fps * 0.5, endFrame - fps * 0.5, endFrame],
    [0, 1, 1, 0],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }
  );

  // Calculate position based on prop
  const getPosition = () => {
    switch (position) {
      case 'top':
        return { top: 50, bottom: 'auto' };
      case 'center':
        return { top: '50%', bottom: 'auto', transform: 'translateY(-50%)' };
      case 'bottom':
      default:
        return { top: 'auto', bottom: 50 };
    }
  };

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        ...getPosition(),
      }}
    >
      <div
        style={{
          fontSize: `${fontSize}px`,
          color,
          backgroundColor,
          padding: `${padding}px`,
          borderRadius: '8px',
          textAlign: 'center',
          fontFamily: 'Arial, sans-serif',
          fontWeight: 'bold',
          opacity,
          maxWidth: '80%',
          lineHeight: 1.2,
          textShadow: '2px 2px 4px rgba(0, 0, 0, 0.8)',
          border: '2px solid rgba(255, 255, 255, 0.3)',
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};