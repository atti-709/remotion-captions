export interface SubtitleEntry {
  id: number;
  startTime: number;
  endTime: number;
  text: string;
}

export interface CaptionStyle {
  fontSize?: number;
  color?: string;
  fontFamily?: string;
  fontWeight?: string;
  textShadow?: string;
  backgroundColor?: string;
  highlightColor?: string;
  padding?: number;
  borderRadius?: number;
  boxShadow?: string;
}

export interface CaptionConfig {
  position?: 'top' | 'center' | 'bottom';
  wordsPerLine?: number;
  fadeInDuration?: number;
  fadeOutDuration?: number;
  highlightScale?: number;
  gap?: number;
}