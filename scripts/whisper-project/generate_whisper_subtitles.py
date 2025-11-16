#!/usr/bin/env python3

import whisper
import os
import sys
from pathlib import Path

def generate_subtitles(video_path, output_path, language='sk', translate=False):
    """
    Generate subtitles from video using Whisper
    If translate=True, translates from Slovak to English
    """
    print(f"🎬 Loading Whisper model...")
    
    # Load the base model (good quality, faster processing)
    model = whisper.load_model("medium")
    
    if translate:
        print(f"🌍 Transcribing and translating video: {video_path}")
        task = "translate"
        target_language = "en"
        initial_prompt = ""
    else:
        print(f"🎬 Transcribing video: {video_path}")
        task = "transcribe"
        target_language = language
        initial_prompt = "Slovenský text o teológii a kresťanstve."
    
    # Transcribe the video with optimized parameters
    result = model.transcribe(
        video_path, 
        language=language,  # Source language (Slovak)
        task=task,         # "transcribe" or "translate"
        word_timestamps=True,  # Better timing
        temperature=0.0,       # More deterministic
        best_of=3,            # Fewer attempts for speed
        beam_size=5,          # Better beam search
        patience=1.0,         # Patience for better quality
        length_penalty=1.0,   # Balanced length penalty
        suppress_tokens=[-1], # Suppress special tokens
        initial_prompt=initial_prompt  # Context hint
    )
    
    print(f"✅ Transcription completed!")
    
    # Generate SRT format with cleaned text
    srt_content = ""
    for i, segment in enumerate(result["segments"], 1):
        start_time = format_time(segment["start"])
        end_time = format_time(segment["end"])
        text = segment["text"].strip()
        
        srt_content += f"{i}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{text}\n\n"
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    print(f"📁 Subtitles saved to: {output_path}")
    print(f"\n📝 Generated subtitles:")
    print(srt_content)
    
    return srt_content


def generate_english_subtitles(video_path, output_path):
    """
    Generate English subtitles by translating from Slovak using Whisper
    """
    return generate_subtitles(video_path, output_path, language='sk', translate=True)


def format_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

if __name__ == "__main__":
    # Get the script directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Define paths (go up two levels from whisper-project to project root)
    project_root = script_dir.parent.parent
    video_path = project_root / "public" / "assets" / "Piano.mp4"
    
    # Check if video exists
    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)
    
    # Check command line arguments for language choice
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['en', 'english']:
        # Generate English subtitles (translated from Slovak)
        output_path = project_root / "public" / "subtitles_en.srt"
        try:
            generate_english_subtitles(str(video_path), str(output_path))
            print("✅ English subtitles generated successfully!")
        except Exception as e:
            print(f"❌ Error generating English subtitles: {e}")
            sys.exit(1)
    else:
        # Generate Slovak subtitles (default)
        output_path = project_root / "public" / "subtitles.srt"
        try:
            generate_subtitles(str(video_path), str(output_path), language='sk')
            print("✅ Slovak subtitles generated successfully!")
        except Exception as e:
            print(f"❌ Error generating Slovak subtitles: {e}")
            sys.exit(1)