import { useEffect, useState } from 'react';
import { SubtitleEntry } from '../types/subtitles';
import { parseSRT } from '../utils/srtParser';

export function useSubtitles(srtPath: string) {
  const [subtitles, setSubtitles] = useState<SubtitleEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadSubtitles = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(srtPath);
        if (!response.ok) {
          throw new Error(`Failed to load subtitles: ${response.statusText}`);
        }
        
        const srtContent = await response.text();
        const parsedSubtitles = parseSRT(srtContent);
        
        setSubtitles(parsedSubtitles);
      } catch (err) {
        console.error('Error loading subtitles:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
        setSubtitles([]);
      } finally {
        setLoading(false);
      }
    };

    loadSubtitles();
  }, [srtPath]);

  return { subtitles, loading, error };
}