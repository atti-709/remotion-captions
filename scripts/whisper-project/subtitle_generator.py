#!/usr/bin/env python3
"""
Advanced Slovak Subtitle Generator using Whisper AI
Optimized for high-quality Slovak transcription with customizable parameters.
"""

import whisper
import os
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

class SlovakSubtitleGenerator:
    def __init__(self, model_size: str = "large-v3"):
        """Initialize the subtitle generator with specified Whisper model."""
        self.model_size = model_size
        self.model = None
        
    def load_model(self) -> None:
        """Load the Whisper model."""
        print(f"🎬 Loading Whisper {self.model_size} model...")
        self.model = whisper.load_model(self.model_size)
        print("✅ Model loaded successfully!")
        
    def generate_subtitles(
        self, 
        video_path: str, 
        output_path: str,
        language: str = 'sk',
        **kwargs
    ) -> str:
        """
        Generate Slovak subtitles from video.
        
        Args:
            video_path: Path to input video file
            output_path: Path to output SRT file
            language: Language code (default: 'sk' for Slovak)
            **kwargs: Additional Whisper parameters
            
        Returns:
            Generated SRT content
        """
        if not self.model:
            self.load_model()
            
        print(f"🎬 Transcribing video: {video_path}")
        
        # Default parameters optimized for Slovak
        default_params = {
            'language': language,
            'word_timestamps': True,
            'temperature': 0.0,
            'best_of': 3,
            'beam_size': 5,
            'patience': 1.0,
            'length_penalty': 1.0,
            'suppress_tokens': [-1],
            'initial_prompt': "Slovenský text o teológii a kresťanstve."
        }
        
        # Merge with user parameters
        params = {**default_params, **kwargs}
        
        # Transcribe the video
        result = self.model.transcribe(video_path, **params)
        
        print("✅ Transcription completed!")
        
        # Generate SRT format
        srt_content = self._format_srt(result["segments"])
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
            
        print(f"📁 Subtitles saved to: {output_path}")
        return srt_content
        
    def _format_srt(self, segments: list) -> str:
        """Format Whisper segments into SRT format."""
        srt_content = ""
        for i, segment in enumerate(segments, 1):
            start_time = self._format_time(segment["start"])
            end_time = self._format_time(segment["end"])
            text = segment["text"].strip()
            
            srt_content += f"{i}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{text}\n\n"
            
        return srt_content
        
    def _format_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def main():
    parser = argparse.ArgumentParser(description="Generate Slovak subtitles using Whisper AI")
    parser.add_argument("video_path", help="Path to input video file")
    parser.add_argument("-o", "--output", help="Output SRT file path", default="subtitles.srt")
    parser.add_argument("-m", "--model", help="Whisper model size", 
                       choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
                       default="large-v3")
    parser.add_argument("-l", "--language", help="Language code", default="sk")
    parser.add_argument("--temperature", type=float, help="Temperature for sampling", default=0.0)
    parser.add_argument("--best-of", type=int, help="Number of candidates", default=3)
    
    args = parser.parse_args()
    
    # Get the script directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    # Define paths
    video_path = project_root / "public" / "assets" / args.video_path
    output_path = project_root / "public" / args.output
    
    # Check if video exists
    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)
    
    try:
        generator = SlovakSubtitleGenerator(model_size=args.model)
        srt_content = generator.generate_subtitles(
            str(video_path), 
            str(output_path),
            language=args.language,
            temperature=args.temperature,
            best_of=args.best_of
        )
        
        print("\n📝 Generated subtitles:")
        print(srt_content)
        print("✅ Slovak subtitles generated successfully!")
        
    except Exception as e:
        print(f"❌ Error generating subtitles: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()