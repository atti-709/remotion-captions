import { SubtitleEntry } from '../types/subtitles';

export function parseSRT(srtContent: string): SubtitleEntry[] {
  const subtitles: SubtitleEntry[] = [];
  const blocks = srtContent.trim().split(/\n\s*\n/);

  for (const block of blocks) {
    const lines = block.trim().split('\n');
    if (lines.length < 3) continue;

    const id = parseInt(lines[0]);
    const timeLine = lines[1];
    const text = lines.slice(2).join('\n');

    // Parse time format: 00:00:00,000 --> 00:00:00,000
    const timeMatch = timeLine.match(/(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})/);
    if (!timeMatch) continue;

    const [, startH, startM, startS, startMs, endH, endM, endS, endMs] = timeMatch;
    
    const startTime = parseInt(startH) * 3600 + parseInt(startM) * 60 + parseInt(startS) + parseInt(startMs) / 1000;
    const endTime = parseInt(endH) * 3600 + parseInt(endM) * 60 + parseInt(endS) + parseInt(endMs) / 1000;

    subtitles.push({
      id,
      startTime,
      endTime,
      text: text.trim(),
    });
  }

  return subtitles;
}

export function formatTime(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  const millisecs = Math.floor((seconds % 1) * 1000);
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${millisecs.toString().padStart(3, '0')}`;
}