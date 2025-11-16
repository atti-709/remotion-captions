import { CaptionStyle, CaptionConfig } from '../types/subtitles';

export const defaultCaptionStyle: CaptionStyle = {
  fontSize: 48,
  color: '#ffffff',
  fontWeight: 'normal',
  textShadow: 'none',
  backgroundColor: 'rgba(0, 0, 0, 0.6)',
  highlightColor: '#ff6b6b',
  padding: 4,
  borderRadius: 6,
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
};

export const defaultCaptionConfig: CaptionConfig = {
  position: 'bottom',
  wordsPerLine: 3,
  fadeInDuration: 0.1,
  fadeOutDuration: 0.1,
  highlightScale: 1.05,
  gap: 8,
};

export const tiktokStyle: CaptionStyle = {
  ...defaultCaptionStyle,
  fontSize: 52,
  highlightColor: '#ff0050',
  backgroundColor: 'rgba(0, 0, 0, 0.7)',
  borderRadius: 8,
  padding: 6,
};

export const youtubeStyle: CaptionStyle = {
  ...defaultCaptionStyle,
  fontSize: 44,
  highlightColor: '#ff0000',
  backgroundColor: 'rgba(0, 0, 0, 0.8)',
  borderRadius: 4,
  padding: 3,
};

export const instagramStyle: CaptionStyle = {
  ...defaultCaptionStyle,
  fontSize: 46,
  highlightColor: '#E4405F',
  backgroundColor: 'rgba(0, 0, 0, 0.75)',
  borderRadius: 10,
  padding: 5,
};