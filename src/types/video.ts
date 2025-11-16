export interface VideoCompositionProps {
  title: string;
  subtitle: string;
  backgroundColor: string;
  textColor: string;
  videoSrc: string;
}

export interface VideoConfig {
  width: number;
  height: number;
  fps: number;
  durationInFrames: number;
}