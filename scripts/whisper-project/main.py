#!/usr/bin/env python3
"""
Main entry point for Whisper subtitle generation.

This script provides a convenient wrapper around the whisper_subtitles package.
Run with --help for usage information.
"""

from whisper_subtitles.cli import run_cli

if __name__ == "__main__":
    run_cli()
