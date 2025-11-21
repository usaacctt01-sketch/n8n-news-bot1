#!/usr/bin/env python3
"""
Fetch YouTube Shorts from a channel
"""
import argparse
import json
import sys
import yt_dlp


def fetch_shorts(channel_url, max_videos=5):
    """Fetch latest shorts from YouTube channel"""
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract channel info
            result = ydl.extract_info(channel_url, download=False)
            
            if not result:
                return {
                    "status": "error",
                    "error": "Could not fetch channel information"
                }
            
            # Get entries (videos)
            entries = result.get('entries', [])
            
            videos = []
            count = 0
            
            for entry in entries:
                if count >= max_videos:
                    break
                
                # Check if it's a short (typically under 60 seconds)
                duration = entry.get('duration', 0)
                
                # Filter for shorts (duration < 60 seconds)
                if duration and duration < 60:
                    videos.append({
                        'video_id': entry.get('id', ''),
                        'video_url': f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                        'title': entry.get('title', 'Untitled'),
                        'duration': duration
                    })
                    count += 1
            
            return {
                "status": "success",
                "videos": videos,
                "total": len(videos)
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Fetch YouTube Shorts from a channel')
    parser.add_argument('--channel-url', required=True, help='YouTube channel URL')
    parser.add_argument('--max-videos', type=int, default=5, help='Maximum number of videos to fetch')
    
    args = parser.parse_args()
    
    result = fetch_shorts(args.channel_url, args.max_videos)
    
    # Output JSON
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
