#!/usr/bin/env python3
"""
Process video: download and capture screenshots
"""
import argparse
import json
import sys
import os
import yt_dlp
from pathlib import Path
import subprocess


def capture_screenshot(video_path, output_path, timestamp="00:00:01"):
    """Capture screenshot from video using ffmpeg"""
    try:
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', timestamp,
            '-vframes', '1',
            '-q:v', '2',
            output_path,
            '-y'
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Screenshot capture failed: {e}", file=sys.stderr)
        return False


def process_video(url, output_dir, cleanup=False):
    """Download video and capture screenshot"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate unique filename
        import hashlib
        import time
        unique_id = hashlib.md5(f"{url}{time.time()}".encode()).hexdigest()[:8]
        
        video_path = os.path.join(output_dir, f"video_{unique_id}.mp4")
        screenshot_path = os.path.join(output_dir, f"screenshot_{unique_id}.jpg")
        
        # Download video
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': video_path,
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        
        # Capture screenshot
        if os.path.exists(video_path):
            capture_screenshot(video_path, screenshot_path)
            
            # Cleanup video if requested
            if cleanup and os.path.exists(video_path):
                os.remove(video_path)
            
            return {
                "status": "success",
                "video_path": video_path if not cleanup else None,
                "screenshot_paths": [screenshot_path] if os.path.exists(screenshot_path) else []
            }
        else:
            return {
                "status": "error",
                "error": "Video file not created"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Download video and capture screenshot')
    parser.add_argument('--url', required=True, help='Video URL')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--cleanup', action='store_true', help='Delete video after screenshot')
    
    args = parser.parse_args()
    
    result = process_video(args.url, args.output_dir, args.cleanup)
    
    # Output JSON
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
